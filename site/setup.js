(() => {
  'use strict';
  const root = document.querySelector('#setup-wizard');
  if (!root) return;
  const key = 'ootxmm-setup-v1';
  const state = {role: 'join', seed: 'new', hosting: 'web', checked: {}};
  let storage = true;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && typeof saved === 'object') {
      for (const name of ['role', 'seed', 'hosting']) {
        const allowed = {role: ['join', 'host', 'solo'], seed: ['new', 'prepared'], hosting: ['web', 'local']};
        if (allowed[name].includes(saved[name])) state[name] = saved[name];
      }
      if (saved.checked && typeof saved.checked === 'object') {
        for (const [id, value] of Object.entries(saved.checked)) if (value === true) state.checked[id] = true;
      }
    }
  } catch { storage = false; }
  function save() {
    try { localStorage.setItem(key, JSON.stringify(state)); } catch { storage = false; }
    document.querySelector('#setup-storage').textContent = storage
      ? 'Checkmarks are saved only in this browser. You can leave and come back.'
      : 'Browser storage is unavailable. Your checklist still works while this page stays open.';
  }
  const detail = (anchor, label = 'Detailed instructions') => `<a href="#${anchor}" data-reference>${label}</a>`;
  const steps = {
    install: ['Get the essentials', 'Install <a href="https://github.com/ArchipelagoMW/Archipelago/releases/tag/0.6.8">Archipelago 0.6.8</a> and <a href="https://github.com/TASEmulators/BizHawk/releases/tag/2.11.1">BizHawk 2.11.1</a>. Have your own Ocarina of Time 1.0 NTSC-U and Majora’s Mask NTSC-U ROMs ready. ROMs are not included.'],
    world: ['Install the matching world package', 'Get <a href="./#world-package">ootxmm.apworld from the player hub</a>. Put it in Archipelago’s <code>custom_worlds</code> folder, then restart the launcher. Everyone must use the same build.'],
    yaml: ['Choose your settings', 'Make a <a href="./#settings">player file on the hub</a>. This downloads a YAML: a small file with your name and game settings. Pick a unique name and keep it; you’ll use it to connect. Send the file to your organizer.'],
    ownyaml: ['Choose everyone’s settings', 'Make your own <a href="./#settings">player YAML on the hub</a> and collect one from each player. A YAML is a small settings file, not a game. Each player name must be unique. Playing solo? You only need your own.'],
    generate: ['Create the game in Archipelago', 'Put the YAML files in Archipelago’s <code>Players</code> folder, then select <strong>Generate</strong> in its launcher. Extract the ZIP in <code>output</code> into a dedicated seed folder. A “seed” is this particular game’s item layout. This does not make playable ROMs yet.'],
    build: ['Build a patch for each player', 'This is the technical part: you need this repository, your original ROMs, and WSL on Windows or Docker on macOS/Linux. Follow '+detail('host-preparation', 'the host build instructions and commands')+'. Check the build succeeds, then give each player their <code>.ootmm</code> file. Keep the generated server file for the next step. Never send ROMs.'],
    web: ['Start a room on archipelago.gg', 'Open <a href="https://archipelago.gg/uploads">Host Game</a> and upload the generated seed ZIP (not your ROMs or repository). On the seed page, select <strong>Create Room</strong>. Share the room link, address and port with the players. Save the room link: reopen it to wake an idle room, and check its current port. Patches still come from your local build.'],
    local: ['Start the server on your computer', 'Select <strong>Host</strong> in the Archipelago launcher and choose the seed ZIP or its <code>.archipelago</code> file. Keep the server window open. On this computer, connect to <code>localhost:38281</code>. Remote friends need your public address and port forwarding: '+detail('start-the-server', 'see server setup')+'. Keep the server save and reuse the same seed to resume.'],
    patch: ['Get your patch and connection details', 'Ask your organizer for your <code>.ootmm</code> patch, your exact slot name, the server address and port, and any password. A slot is your place in the group’s game. Wait for these before continuing.'],
    prepared: ['Get your assigned playtest files', 'Ask your organizer whether you are <strong>Tester1</strong> or <strong>Tester2</strong>. Extract the <a href="./#world-package">prepared playtest ZIP</a> and use that slot’s patch. Your organizer must run the matching private server file and give you its address. The ZIP does not include a running server. Skip the YAML; this game already requires both bosses.'],
    rom: ['Turn your patch into a playable ROM', 'Open <a href="https://ootmm.com/gen/v33.0">OoTMM v33.0</a>, select your two original ROMs, and set <strong>Generator Mode → Patch</strong>. Choose your <code>.ootmm</code> file, then <strong>Generate → Download</strong>. Extract the <code>.z64</code> if needed. Do not generate a new random game on the website: it would not connect to Archipelago. '+detail('build-your-rom')+'.'],
    lua: ['Open BizHawk and load the connector', 'Open the patched <code>.z64</code> in BizHawk. Go to <strong>Tools → Lua Console → Script → Open Script</strong>. In your <em>Archipelago installation</em>, choose <code>data/lua/connector_bizhawk_generic.lua</code>. Leave the script running. '+detail('connect-and-play', 'Where to find the script')+'.'],
    client: ['Connect your game', 'In the Archipelago launcher, open <strong>BizHawk Client</strong>. Look for <code>Connected to BizHawk</code> and <code>Running handler for OOTxMM</code>. Enter just the server address and port in <strong>Server</strong> (for example <code>archipelago.gg:12345</code>). Select <strong>Connect</strong>, then enter your exact slot name and any password when asked.'],
    play: ['Start playing and check your first item', 'Start a new save and enter gameplay; the connection only becomes active after file select. Open your first chest or collect an item and check that the client logs it. Keep the client, Lua script and server connected. Use in-game saves to keep your progress. '+detail('troubleshooting', 'Something not working?')+'.']
  };
  function ids() {
    return ['install', 'world', ...(state.role === 'join'
      ? state.seed === 'prepared' ? ['prepared'] : ['yaml', 'patch']
      : ['ownyaml', 'generate', 'build', state.hosting]), 'rom', 'lua', 'client', 'play'];
  }
  function progress() {
    const active = ids();
    const done = active.filter(id => state.checked[id]).length;
    document.querySelector('#setup-progress').max = active.length;
    document.querySelector('#setup-progress').value = done;
    document.querySelector('#setup-count').textContent = `${done} of ${active.length} steps complete`;
    document.querySelector('#setup-done').hidden = done !== active.length;
    root.querySelectorAll('[data-step]').forEach(input => input.closest('li').classList.toggle('is-complete', input.checked));
  }
  function render() {
    document.querySelector('#setup-seed').hidden = state.role !== 'join';
    document.querySelector('#setup-hosting').hidden = state.role === 'join';
    document.querySelector('#setup-path').textContent = state.role === 'join'
      ? state.seed === 'prepared' ? 'Joining the prepared playtest. Your organizer handles game preparation and the server.' : 'Joining a new game. Your organizer handles game preparation and the server.'
      : `${state.role === 'solo' ? 'Playing solo: you are both organizer and player.' : 'Organizing a group: prepare the game, then follow the player steps too.'} Server: ${state.hosting === 'web' ? 'archipelago.gg' : 'your computer'}.`;
    document.querySelector('#setup-steps').innerHTML = ids().map((id, i) => `<li><label class="setup-step-title"><input type="checkbox" data-step="${id}" ${state.checked[id] ? 'checked' : ''}><span><small>STEP ${i + 1}</small><strong>${steps[id][0]}</strong></span></label><div class="setup-step-body"><p>${steps[id][1]}</p></div></li>`).join('');
    progress();
  }
  root.addEventListener('change', event => {
    const input = event.target;
    if (input.matches('input[type="radio"]')) { state[input.name] = input.value; render(); }
    if (input.matches('[data-step]')) { state.checked[input.dataset.step] = input.checked; progress(); }
    save();
  });
  document.querySelector('#setup-reset').addEventListener('click', () => { state.checked = {}; render(); save(); });
  const reference = document.querySelector('#setup-reference');
  function openReference() {
    if (location.hash && reference.querySelector(`[id="${CSS.escape(location.hash.slice(1))}"]`)) reference.open = true;
  }
  document.addEventListener('click', event => {
    if (event.target.closest('[data-reference]')) reference.open = true;
  });
  window.addEventListener('hashchange', openReference);
  for (const name of ['role', 'seed', 'hosting']) root.querySelector(`input[name="${name}"][value="${state[name]}"]`).checked = true;
  render();
  save();
  root.hidden = false;
  openReference();
})();
