/*
 * Builds one player's ROM for an Archipelago seed. Run in OoTMM's generator package (tools/ootmm-build.sh copies
 * this folder to packages/generator/lib/ap/); see "ROM patch" in DEVELOPMENT.md.
 *
 * Usage: tsx lib/ap/ap-patch.ts <player file (.json) or directory> <oot rom> <mm rom> <output folder>
 * Writes the ROM (.z64) and OoTMM's patch file for it (.ootmm), which OoTMM's patch mode builds the ROM from.
 *
 * Runs OoTMM's logic with the player's settings, so everything settings decide (prices, song events, entrances,
 * starting items) is OoTMM's own, then replaces the item at every location with the Archipelago seed's: the
 * player's own items for world 1, other players' items for world 2, a world that doesn't exist, so the game hands
 * them to its multiworld code and the client reports the check.
 */
import type { Hints, Location, PlayerItem } from '@ootmm/logic';

import { promises as fs } from 'fs';
import path from 'path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { Monitor, makeRegion, options, randomInt, resolveMmAgeRequirements, SETTINGS } from '@ootmm/core';
import { solvedWorldState, logicPassCloak, itemByID, ItemGroups, ItemHelpers, makeLocation, makePlayerItem } from '@ootmm/logic';
/* Not exported by the package */
import { logicPassHash } from '../../../logic/src/misc';
import { custom } from '../combo/custom';
import { decompressGames } from '../combo/decompress';
import { pack } from '../combo/pack';
import { buildPatchfiles } from '../combo/patch-build';
import { Patchfile } from '../combo/patch-build/patchfile';
import { makeAddresses } from '../combo/addresses';

/* Written by the world's generate_output (world.py) */
type PlayerFile = {
  version: 1;
  seed: string;
  /* OoTMM settings, keyed and valued as OoTMM's, sets as lists */
  settings: { [k: string]: unknown };
  /* Location to [OoTMM item, true if the item is the player's own] */
  locations: { [k: string]: [string, boolean] };
};

const OUR_WORLD = 0;
const OTHER_WORLD = 1;

/* The checks whose item the game hints at in place (FIXED_HINTS_LOCATIONS in OoTMM's logic/src/hints.ts) */
const FIXED_HINTS_LOCATIONS = [
  'OOT Skulltula House 100 Tokens', 'OOT Skulltula House 10 Tokens', 'OOT Skulltula House 20 Tokens',
  'OOT Skulltula House 30 Tokens', 'OOT Skulltula House 40 Tokens', 'OOT Skulltula House 50 Tokens',
  'OOT Hyrule Field Ocarina of Time', 'OOT Hyrule Field Song of Time', 'MM Laboratory Zora Song',
  'MM Moon Fierce Deity Mask', 'MM Woodfall Great Fairy', 'MM Snowhead Great Fairy', 'MM Great Bay Great Fairy',
  'MM Ikana Great Fairy', 'MM Goron Powder Keg', 'MM Waterfall Rapids Beaver Race 1', 'MM Waterfall Rapids Beaver Race 2',
  'MM Swamp Spider House Mask of Truth', 'MM Ocean Spider House Wallet', 'MM Clock Town Great Fairy',
  'MM Clock Town Great Fairy Alt',
];

function readFileUint8(p: string): Promise<Uint8Array> {
  return fs.readFile(p).then((x) => new Uint8Array(x.buffer, x.byteOffset, x.byteLength));
}

/* Same conversion as OoTMM's CLI (lib/cli.ts): a set setting given as a list is that specific set */
function settingsInput(data: PlayerFile['settings']) {
  const result: { [k: string]: unknown } = {};
  for (const [key, value] of Object.entries(data)) {
    if (['startingItems', 'tricks', 'junkLocations', 'specialConds', 'plando', 'hints'].includes(key)) {
      result[key] = value;
      continue;
    }
    const setting = SETTINGS.find((x) => x.key === key);
    if (!setting) throw new Error(`Unknown OoTMM setting: ${key}`);
    result[key] = (setting.type === 'set' && Array.isArray(value)) ? { type: 'specific', values: value } : value;
  }
  return result;
}

/*
 * OoTMM's hints come from its playthrough analysis, which can't run on half a multiworld. Gossip stones get
 * junk hints; the fixed hints (where the dungeon rewards, Light Arrows, Oath to Order and Ganon's key are, how
 * important the item at a few checks is) are worked out from the placements, as OoTMM does.
 */
function hints(state: any): Hints {
  const world = state.worlds[OUR_WORLD];
  const regionsOf = (ids: string[], count: number) => {
    const wanted = ids.map((id) => makePlayerItem(itemByID(id), OUR_WORLD));
    const regions = [];
    for (const item of wanted) {
      for (let i = 0; i < (state.startingItems.get(item) || 0); ++i) regions.push(makeRegion('POCKET', 0));
    }
    for (const [loc, item] of state.items as Map<Location, PlayerItem>) {
      if (wanted.includes(item)) regions.push(makeRegion(world.regions[loc.split('@')[0]], OUR_WORLD));
    }
    regions.splice(count);
    while (regions.length < count) regions.push(makeRegion('NONE', 0));
    return regions;
  };
  const importance = (locId: string) => {
    const item = state.items.get(makeLocation(locId, OUR_WORLD)) as PlayerItem | undefined;
    if (!item) return 0;
    return ItemHelpers.isItemMajor(item.item) ? 2 : -1;
  };
  const gossip: Hints[number]['gossip'] = {};
  for (const [id, g] of Object.entries(world.gossip as { [k: string]: { game: 'oot' | 'mm' } })) {
    gossip[id] = { game: g.game, type: 'junk', id: randomInt(state.random, 65536) };
  }
  const ganonBossKey = state.settings.ganonBossKey === 'anywhere' ? regionsOf(['OOT_BOSS_KEY_GANON'], 1)[0] : makeRegion('NONE', OUR_WORLD);
  const oathToOrder = state.settings.songs === 'notes'
    ? regionsOf(['MM_SONG_NOTE_ORDER', 'SHARED_SONG_NOTE_ORDER'], 6)
    : [...regionsOf(['MM_SONG_ORDER', 'SHARED_SONG_ORDER'], 1), ...Array(5).fill(makeRegion('NONE', OUR_WORLD))];
  return [{
    foolish: new Map(),
    dungeonRewards: [...ItemGroups.DUNGEON_REWARDS].map((item) => regionsOf([item.id], 1)[0]),
    lightArrow: regionsOf(['OOT_ARROW_LIGHT', 'SHARED_ARROW_LIGHT'], 1)[0],
    oathToOrder,
    ganonBossKey,
    staticHintsImportances: FIXED_HINTS_LOCATIONS.map(importance),
    gossip,
  }];
}

async function buildPlayer(playerPath: string, ootPath: string, mmPath: string, outDir: string) {
  const playerBytes = await fs.readFile(playerPath);
  const player: PlayerFile = JSON.parse(playerBytes.toString('utf-8'));
  if (player.version !== 1) throw new Error(`Unsupported player file version ${player.version}`);

  const monitor = new Monitor({}, false);
  const opts = options({
    seed: player.seed,
    settings: { ...settingsInput(player.settings), mode: 'single', players: 1, teams: 1, generateSpoilerLog: false } as any,
  });
  const roms = await decompressGames(monitor, { oot: await readFileUint8(ootPath), mm: await readFileUint8(mmPath) });
  const addresses = makeAddresses(roms);
  await resolveMmAgeRequirements(opts.settings, opts.seed);

  const patchfile = new Patchfile;
  await custom(monitor, roms, patchfile);

  /* OoTMM's logic up to its fill, then our placements, then the passes that read them (hints) */
  const state = await solvedWorldState(monitor, opts);
  const world = state.worlds[OUR_WORLD];
  for (const locId of world.locations) {
    const placed = player.locations[locId];
    if (!placed) throw new Error(`No item for location ${locId}: the world and OoTMM disagree on the checks`);
    const [itemId, own] = placed;
    state.items.set(makeLocation(locId, OUR_WORLD), makePlayerItem(itemByID(itemId), own ? OUR_WORLD : OTHER_WORLD));
  }
  for (const locId of Object.keys(player.locations)) {
    if (!world.locations.has(locId)) throw new Error(`Location ${locId} is not a check in OoTMM with these settings`);
  }
  const { itemCloaks } = logicPassCloak(state as any);
  const logicResult = {
    worlds: state.worlds,
    startingItems: state.startingItems,
    plandoLocations: state.plandoLocations,
    items: state.items,
    itemCloaks,
    analysis: { spheres: [], required: new Set(), useless: new Set(), unreachable: new Set(), paths: [] },
    hints: hints(state),
    hash: logicPassHash(state as any).hash,
  };

  /* The ROM is a multiworld one: own pickups are reported, items arrive from the client */
  opts.settings.mode = 'multi';
  patchfile.setHash(logicResult.hash);
  const [built] = await buildPatchfiles({ patch: patchfile, monitor, roms, addresses, logic: logicResult as any, settings: opts.settings });
  built.meta['mode'] = opts.settings.mode;
  built.meta['worldId'] = OUR_WORLD + 1;
  const sessionId = crypto.getRandomValues(new Uint8Array(16));
  const sessionSecret = crypto.getRandomValues(new Uint8Array(8));
  built.addSymbolPatch('MULTI_SESSION_ID', sessionId);
  built.addSymbolPatch('MULTI_SESSION_SECRET', sessionSecret);

  /* Reserved N64 header bytes, preserved by OoTMM's browser patch mode. The versioned marker is separate
   * from the two 24-bit RDRAM offsets so the ROM title and cartridge ID remain intact. Exported addresses
   * come from the exact compiled payloads, never from another build's memory layout. */
  const mailboxOffsets = Buffer.alloc(6);
  for (const [index, game] of (['oot', 'mm'] as const).entries()) {
    const symbols = built.symbols[game].get('AP_IPC_MAILBOX');
    if (!symbols || symbols.length !== 1) throw new Error(`Missing unique ${game} mailbox symbol`);
    const address = symbols[0];
    if (address < 0x80000000 || address > 0x807fefd0 || address % 16 !== 0)
      throw new Error(`Invalid ${game} mailbox address: ${address.toString(16)}`);
    mailboxOffsets.writeUIntBE(address - 0x80000000, index * 3, 3);
  }
  built.addPatch('oot/makerom', 0x18, new TextEncoder().encode('APIPC001'));
  built.addPatch('oot/makerom', 0x34, mailboxOffsets);

  await fs.mkdir(outDir, { recursive: true });
  const name = path.basename(playerPath).replace(/\.json$/, '');
  const patchOut = path.join(outDir, `${name}.ootmm`);
  const patchBytes = await built.serialize();
  await fs.writeFile(patchOut, patchBytes);
  const { rom } = await pack({ opts, monitor, roms, patchfile: built, addresses });
  const romOut = path.join(outDir, `${name}.z64`);
  await fs.writeFile(romOut, rom);
  const sha256 = (bytes: Uint8Array) => createHash('sha256').update(bytes).digest('hex');
  const sourceRoot = process.env.OOTMM_AP_SOURCE_ROOT;
  const patchInputs: Record<string, string> = {};
  if (sourceRoot) {
    for (const folder of ['ootmm-ap', 'ootmm-patches']) {
      for (const entry of (await fs.readdir(path.join(sourceRoot, folder))).sort()) {
        const relative = `${folder}/${entry}`;
        if ((await fs.stat(path.join(sourceRoot, relative))).isFile()) {
          patchInputs[relative] = sha256(await fs.readFile(path.join(sourceRoot, relative)));
        }
      }
    }
  }
  const receipt = {
    schema_version: 1,
    seed: player.seed,
    placement: { name: path.basename(playerPath), sha256: sha256(playerBytes) },
    patch: { name: path.basename(patchOut), sha256: sha256(patchBytes) },
    rom: { name: path.basename(romOut), sha256: sha256(rom) },
    builder_sha256: sha256(await fs.readFile(fileURLToPath(import.meta.url))),
    ootmm_revision: execFileSync('git', ['rev-parse', 'HEAD']).toString().trim(),
    ootmm_diff_sha256: await ootmmDiffSha256(),
    patch_inputs: patchInputs,
  };
  await fs.writeFile(path.join(outDir, `${name}.build.json`), JSON.stringify(receipt, null, 2) + '\n');
  console.log(`Wrote ${patchOut}, ${romOut} and build receipt`);
}

// git diff leaves out untracked files, and git apply leaves the files our patches add untracked.
async function ootmmDiffSha256() {
  const git = (...args: string[]) => execFileSync('git', args, { maxBuffer: 64 * 1024 * 1024 });
  const root = git('rev-parse', '--show-toplevel').toString().trim();
  const untracked = git('ls-files', '--others', '--exclude-standard', '--full-name', '--', root).toString().split('\n').filter(Boolean).sort();
  const contents = await Promise.all(untracked.map((file) => fs.readFile(path.join(root, file))));
  const diff = Buffer.concat([git('diff', '--binary', 'HEAD'), ...untracked.flatMap((file, i) => [Buffer.from(`${file}\0`), contents[i]])]);
  return createHash('sha256').update(diff).digest('hex');
}

async function main(args: string[]) {
  if (args.length !== 4) throw new Error('Usage: ap-patch.ts <player file or directory> <oot rom> <mm rom> <output folder>');
  const [input, ootPath, mmPath, outDir] = args;
  const stat = await fs.stat(input);
  const players = stat.isDirectory()
    ? (await fs.readdir(input)).filter((name) => name.endsWith('.ootxmm.json')).sort().map((name) => path.join(input, name))
    : [input];
  if (!players.length) throw new Error(`No .ootxmm.json player files in ${input}`);
  for (const playerPath of players) await buildPlayer(playerPath, ootPath, mmPath, outDir);
}

main(process.argv.slice(2)).catch((e) => {
  console.error(e);
  process.exit(1);
});
