# Release readiness

Work through these gates before handing out the next playtest build. Keep unfinished work here; remove completed tasks after recording reproducible validation with the frozen build. The player-facing scenarios are in [the playtest checklist](playtest_en.md).

## 1. Reproducible gameplay setup

Use the [isolated scenario harness](gameplay_testing.md) with separate configuration, saves, matching ROMs and temporary servers. Keep source-verified layouts pinned to the ROM hash, record seed/slot/settings and inherited assistance beside checkpoints, and retain inputs, logs, screenshots and server assertions under ignored `dist/`. Preserve frozen packages and player saves.

Test shortcuts may prepare inventory, position the player, enter a boss room, enable invulnerability or reduce enemy health. They must leave the actual chest interaction, transition or final defeat handler to the game. Writing a boss flag, location flag, mailbox packet or server check directly is protocol coverage, not proof of gameplay reporting. If a shortcut skips part of a route, record that limit.

## 2. Actual pickups and delivery

The candidate verifies its native cross-game door, MM opening-song award, bidirectional OoT chest exchange and the remote South Clock Town chest with two running players. Both receipt indices remain stable; the MM chest's recipient has the native Mirror Shield equipped after switching to MM. OoT nut upgrade inventory and refill are covered by the OoT exchange.

The native Kokiri Shop Deku Shield purchase verifies a representative shop and fixed vanilla check. Diagnostic funding supplies 50 rupees; controller input selects the shelf item and confirms its 40-rupee offer. Native inventory changes from shield absent to present and the balance becomes 10. The server records only `OOT Kokiri Shop Item 8` as new, with exactly one local Deku Shield award; receipt index 3 remains stable through 16 successful polls. The exact-ROM checkpoint inherits assisted travel, and a guarded shop transition bypasses the route. This covers vanilla local stock and payment, not remote shop awards, shuffled prices or shield ability use.

The Temple of Time medallion verifies a representative dungeon-reward location. A diagnostic Master Sword supplies the time-travel prerequisite; guarded sword-chamber entry and pedestal positioning skip access and travel. The native child pedestal pickup queues its placed MM heart piece for the other slot, then normal carry input changes Link to adult. The adult pedestal handler awards the locally placed Odolwa's Remains: MM's native quest value changes from 0 to 1 while OoT is active. It remains 1 after native return to child and after the native door into MM, where the active payload, scene and native quest field are asserted. Both source locations produce exactly one server award and no other new checks. The diagnostic grant advances the receipt index from 2 to 3; the local reward does not advance it again, and 16 successful destination polls remain at 3. Guarded Market entry/door positioning skips travel. This is pedestal/reward handling, not a dungeon boss defeat or blue-warp pickup; the queued remote heart piece's receipt is not checked. Candidate song coverage uses the MM opening award.

- [ ] Verify a dungeon boss's blue-warp reward pickup after its native defeat.
- [ ] Verify remote key use at the intended doors, Ganon's boss key and temple fairy rewards. Diagnostic candidate grants already verify the native Fire Temple small-key count/boss-key bit and the Woodfall fairy counter; these are item-application coverage, not actual source pickups or door use.
- [ ] Exercise shared equipment and songs in both games; check upgrades and abilities as well as item messages.

## 3. Recovery and load

Staged two-player gameplay verifies a continuous native OoT-MM-OoT round trip with real source pickups and remote receipt after each switch. Both players start fresh files on their exact ROMs; arrival barriers release each source interaction only after a live destination query. Four checks award exactly one remote item each, and both receipt indices remain at 2 through 16 fresh polls. The OoT nut upgrade persists on return; the MM recipient equips the Mirror Shield. Guarded scene/position setup and bounded health support bypass travel and access requirements.

An exact-ROM native OoT save and cold boot retain the two real remote receipts at index 2, the nut upgrade, song and opened chest without replay. A real own Odd Potion chest collected and saved while disconnected is absent from the disposable server save, then reports exactly once after cold boot in fresh emulator/client/server processes. Its native item and both opened-chest flags persist. Menu save confirmations and SaveRAM files accompany the evidence. This covers one pending reliable check. Separate real Odd Potion chest runs abort the actual socket before delivery and after server acceptance, then reconnect through normal login. Each produces exactly one award, no extra checks and 16 polls at receipt index 2; native inventory is asserted. These controlled send boundaries cover both acceptance outcomes, without byte-level fragmentation or process-crash coverage. Unrestricted offline play and remaining load coverage are still open. Repeat affected gates if the frozen candidate changes.

Two real remote chests, one in OoT and one in MM, queue while the recipient idles in MM with its socket closed and game connection flag clear. Normal reconnect and controller dismissal of item messages drain both awards; the native Don Gero mask is asserted before continuing, and the OoT nut upgrade/refill is asserted after returning through the native door. The recipient then reports two real source checks to the other game, whose native Mirror Shield is asserted. All four checks award exactly once and both receipt indices remain at 2 through 16 fresh polls. Fresh exact-ROM files, guarded travel/position setup and bounded idle health support retain the route/access limits above; the server stays running during this outage.

An orderly disposable server restart after the first two real awards reloads existing checks and remote queues into a new listener/context. Both clients reconnect at receipt index 1, then switch games and collect a new real remote chest each. Both indices reach 2 and remain stable for 16 fresh polls; every source awards exactly once and native inventory assertions pass. The coordinator process stays running, so abrupt server-process loss remains outside this coverage.
A diagnostic hundred-item server burst queues while the native OoT pause menu is open for 3,000 frames, then drains from receipt index 2 to 102 after normal Start/B input. All 16 subsequent receipt polls remain at 102 with no new source checks. Source-pinned pause-state reads and captures bracket the queue timestamp; sampled ring occupancy accompanies the run. The rupee run is unthrottled throughout. A separate six-item progression queue uses native pause, then blocks on the Bomb Bag message with the bow still absent. Normal B input drains the queue across scripted 100%/400% speed changes; Light Arrows remain pending at the first accelerated-speed transition. Native inventory asserts the bomb bag, bow, hookshot and all three elemental arrows, and all 16 receipt polls remain at index 8. Clock throttling and measured frame/time intervals establish the speed changes; actual accelerated speed can be core-limited. These diagnostic grants verify receipt and native storage, not real source pickups or equipment abilities.

A corresponding MM run queues six progression grants during native pause for 600 frames. Before grants all six native slots are empty; while still paused the Bomb Bag is stored and the remaining five stay absent. After resuming, its message blocks the bow; normal B input and measured 100%/400% speed changes drain all six into their expected native slots. Receipt index 2 reaches 8 and stays there through 16 polls, without new source checks. Sampled ring occupancy peaks at 234 outgoing and 31 incoming bytes of 2047 usable, with no invalid headers. Both progression runs are diagnostic delivery/storage coverage, not real source pickups or ability use.

Three consecutive real OoT Mido chests at requested 400% speed start 2.66 seconds apart with native item dialogue and controller dismissal. The disposable server records exactly three new checks and one award each: local Odd Potion and arrows, plus an MM bow queued for the absent other slot. Native Odd Potion storage is asserted; receipt index 2 remains stable through 16 successful polls. The run has 137 valid header samples, no invalid headers or mailbox rediscovery, and sampled peaks of 1274 outgoing/23 incoming bytes of 2047 usable. Guarded positioning skips movement between chests; this is dialogue-limited chest cadence, not simultaneous non-dialogue pickups or remote bow receipt. The exact-ROM checkpoint inherits the assisted round trip above.

## 4. Boss completion

- [ ] Verify a continuous native both-boss completion and credits sequence. Assisted candidate tests observe real Majora and Ganon packets, preserving Majora's stored progress across a fresh client/server before Ganon and correctly completing the server slot. Compatible pre-boss checkpoints and diagnostic inventory setup skip the continuous route; native combined-game credits are not asserted.
- [ ] Verify the opposite order, Ganon then Majora, in the other slot. The first boss must not finish the both-boss slot; the second must.
- [ ] Check `ganon`, `majora` and `any` goal handling with corresponding real victory events. Reuse compatible checkpoints only within their matching ROM and seed.

## 5. Player installation and hub

- [ ] Rehearse the graphical launcher and v33.0 browser patcher steps. A clean isolated installation loads the packaged world without legacy manifest fallback, generates its full template, reapplies both player patches through CLI Patch mode, then verifies own-item inventory and actual bidirectional exchange from fresh files.
- [ ] Check that a second person needs only the package, their own ROMs and connection details; fix unclear instructions discovered during rehearsal.

## 6. Additional options

- [ ] Port the remaining shared equipment and songs in small coherent groups. For each group compare source and shared pool counts with OoTMM, test logic gates and prefill, generate a two-player seed and build both ROM patches.
- [ ] Prioritize options intended for the group's YAML; verify their gameplay effects before including them in the candidate settings.
- [ ] Assess `itemPool`, `pondFishShuffle` and Triforce goals separately. Each needs its own pool, logic and ROM validation; keep them unavailable until complete. Do not delay core gameplay gates to fit these into the first release.

## 7. Candidate validation and freeze

A frozen candidate includes the current world, receipt-verified patches, guides, checksums and a private validation report. The full regression suite, packaged-world manifest reader, template generation, starter YAML and CLI patch reapplication pass. Re-run affected checks after functional changes; retain the exact ZIP hash and post-freeze evidence.

- [ ] Generate representative two-player seeds with default and intended group settings; build every player's patch and check placement agreement.
