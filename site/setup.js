(() => {
  'use strict';
  const root = document.querySelector('#setup-wizard');
  if (!root) return;
  const key = 'ootxmm-setup-v1';
  const state = {role: 'join', emulator: 'bizhawk', hosting: 'web', checked: {}};
  const choices = {role: ['join', 'host', 'solo'], emulator: ['bizhawk', 'dolphin'], hosting: ['web', 'local']};
  let storage = true;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && typeof saved === 'object') {
      for (const name of Object.keys(choices)) {
        if (choices[name].includes(saved[name])) state[name] = saved[name];
      }
      if (saved.checked && typeof saved.checked === 'object') {
        for (const [id, value] of Object.entries(saved.checked)) if (value === true) state.checked[id] = true;
      }
    }
  } catch { storage = false; }
  function save() {
    try { localStorage.setItem(key, JSON.stringify(state)); } catch { storage = false; }
    const note = document.querySelector('#setup-storage');
    note.textContent = 'Checkmarks cannot be saved in this browser.';
    note.hidden = storage;
  }
  const detail = (anchor, label = 'Details') => `<a href="#${anchor}" data-reference>${label}</a>`;
  const steps = {
    install: ['Install Archipelago', 'Install <a href="https://github.com/ArchipelagoMW/Archipelago/releases/tag/0.6.8">Archipelago 0.6.8</a>. Have your own Ocarina of Time 1.0 NTSC-U and Majora’s Mask NTSC-U ROMs.'],
    bizhawk: ['Install BizHawk', 'Install <a href="https://github.com/TASEmulators/BizHawk/releases/tag/2.11.1">BizHawk 2.11.1</a>.'],
    dolphin: ['Install Dolphin', '<strong>Experimental:</strong> Dolphin is less tested than BizHawk. Use BizHawk for a run you want to finish. Install <a href="https://dolphin-emu.org/download/">Dolphin</a>. Select <strong>Tools → Install WAD to Wii Menu</strong> and choose your own Majora’s Mask NTSC-U Virtual Console WAD.'],
    world: ['Install the world', 'Download <a href="./#world-package">ootxmm.apworld</a> into Archipelago’s <code>custom_worlds</code> folder, then restart the launcher.'],
    yaml: ['Make your player file', 'Make a <a href="./#settings">YAML on the hub</a> and send it to your organizer. You connect with the name you choose.'],
    ownyaml: ['Collect player files', 'Make your <a href="./#settings">YAML on the hub</a> and collect one from each player. Names must be unique.'],
    generate: ['Generate the game', 'Put the YAMLs in Archipelago’s <code>Players</code> folder and select <strong>Generate</strong>. Extract the ZIP from <code>output</code> into a new folder.'],
    build: ['Build the patches', 'Download <a href="https://github.com/Decryptu/ootmm-decrypted/releases/latest/download/ootxmm-host.zip">ootxmm-host.zip</a> and extract it to a short folder such as <code>C:\ootxmm-host</code>. Double-click <strong>Host Setup.cmd</strong> inside it. Select the folder you extracted in step 5, then your ROMs. Answer <strong>Yes</strong> if anyone plays on Dolphin. Send each player their <code>.ootmm</code> file; Dolphin players get theirs from the <code>Dolphin</code> folder. Never send ROMs. Your own ROM is already built: the <code>.z64</code> with your name (Dolphin: the one in the <code>Dolphin</code> folder). '+detail('host-preparation')+'.'],
    web: ['Start the server', 'Upload the <code>AP_….zip</code> that Archipelago’s <strong>Generate</strong> put in its <code>output</code> folder (not the patches) on <a href="https://archipelago.gg/uploads">archipelago.gg</a> and select <strong>Create Room</strong>. Share the address and port.'],
    local: ['Start the server', 'In the Archipelago launcher, select <strong>Host</strong> and choose the <code>AP_….zip</code> from Archipelago’s <code>output</code> folder. Keep the window open. '+detail('start-the-server')+'.'],
    patch: ['Get your patch', 'Get your <code>.ootmm</code> file, the server address and any password from your organizer.'],
    rom: ['Make your ROM', 'On <a href="https://ootmm.com/gen/v33.0">OoTMM v33.0</a>, select your two ROMs, set <strong>Generator Mode → Patch</strong>, choose your <code>.ootmm</code> and select <strong>Generate</strong>. Never generate a normal seed there: it cannot connect.'],
    wad: ['Put the ROM in Dolphin', 'In the Archipelago launcher, type <strong>Dolphin</strong> in the search box and open <strong>OOTxMM Dolphin Setup</strong>. Choose your <code>.z64</code> from the host’s <code>Dolphin</code> folder. <strong>Recommended:</strong> when it asks for the Wii common key, choose your own <code>keys.bin</code> or 16-byte key, then your Majora’s Mask WAD: it writes a patched <code>.wad</code> next to the ROM. Without a key, select Cancel and use the Wii Menu (next step). '+detail('play-on-dolphin')+'.'],
    lua: ['Start BizHawk', 'Open your <code>.z64</code> in BizHawk. In <strong>Tools → Lua Console</strong>, open <code>data/lua/connector_bizhawk_generic.lua</code> from your Archipelago folder.'],
    client: ['Connect', 'In the Archipelago launcher, open <strong>BizHawk Client</strong>. Enter the server address and port, select <strong>Connect</strong>, then enter your name.'],
    dclient: ['Connect', 'With the key: in Dolphin, <strong>File → Open</strong> the patched <code>.wad</code>. Without it: install your Majora’s Mask WAD (<strong>Tools → Install WAD to Wii Menu</strong>) before Setup; once, <strong>Tools → Perform Online System Update → United States</strong>; then <strong>Tools → Load Wii System Menu</strong> and the Majora’s Mask channel. Load a save, then in the Archipelago launcher open <strong>OOTxMM Dolphin Client</strong>, enter the server address and port, select <strong>Connect</strong> and enter your name.'],
    play: ['Play', 'Load a save file. Items arrive once you are in game. Save in game to keep your progress. '+detail('troubleshooting', 'Problems?')]
  };
  function ids() {
    const dolphin = state.emulator === 'dolphin';
    return ['install', dolphin ? 'dolphin' : 'bizhawk', 'world', ...(state.role === 'join'
      ? ['yaml', 'patch']
      : ['ownyaml', 'generate', 'build', state.hosting]), ...(state.role === 'join' ? ['rom'] : []), ...(dolphin ? ['wad', 'dclient'] : ['lua', 'client']), 'play'];
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
    document.querySelector('#setup-hosting').hidden = state.role === 'join';
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
  for (const name of Object.keys(choices)) root.querySelector(`input[name="${name}"][value="${state[name]}"]`).checked = true;
  render();
  save();
  root.hidden = false;
  openReference();
})();
