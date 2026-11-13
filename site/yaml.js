"use strict";

// Settings in an ootmm.com export that describe the website's own generation, not the seed's gameplay.
const NOT_GAMEPLAY = new Set(["games", "mode", "players", "teams", "generateSpoilerLog"]);

function checkName(name) {
  // The characters YAML files can't hold, and the name Archipelago keeps for itself, fail generation for everyone.
  if (!name || [...name].length > 16 || /[{}\x00-\x1f\x7f-\x84\x86-\x9f￾￿]/u.test(name)) {
    throw new Error("Enter a name of 1–16 characters without braces or control characters.");
  }
  if (name === "Archipelago") throw new Error("That name is reserved. Choose another.");
}

// Deep equality for JSON values, ignoring object key order.
function sameValue(a, b) {
  if (a === b) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every((key) => key in b && sameValue(a[key], b[key]));
}

// An OoTMM value as the YAML value of the world's option, or undefined when the option can't take it.
function convert(spec, value) {
  if (spec.type === "choice") return spec.values.includes(value) ? (spec.aliases?.[value] ?? value) : undefined;
  if (spec.type === "toggle") return typeof value === "boolean" ? value : undefined;
  if (spec.type === "range") return Number.isInteger(value) && value >= spec.min && value <= spec.max ? value : undefined;
  // Sets: OoTMM's {type: none | all | specific, values} for key rings, a plain list for tricks.
  let list;
  if (Array.isArray(value)) list = value;
  else if (value && value.type === "none") list = [];
  else if (value && value.type === "all") list = spec.values;
  else if (value && value.type === "specific" && Array.isArray(value.values)) list = value.values;
  if (!list || !list.every((entry) => spec.values.includes(entry))) return undefined;
  return [...new Set(list)];
}

// OoTMM's starting items ({item ID: count}) as Archipelago's start_inventory, or undefined if one is unknown.
function startInventory(value, itemNames) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return undefined;
  const inventory = {};
  for (const [id, count] of Object.entries(value)) {
    if (!(id in itemNames) || !Number.isInteger(count) || count < 0) return undefined;
    if (count > 0) inventory[itemNames[id]] = count;
  }
  return inventory;
}

// specs: the hub's options.json, with the world's options, OoTMM's default settings and the item names.
function importSettings(exported, { options: specs, ootmmDefaults, itemNames }) {
  const settings = exported?.data?.settings ?? exported?.settings;
  if (!settings || typeof settings !== "object") {
    throw new Error("This file is not an OoTMM settings export. On ootmm.com, export your settings and choose that file.");
  }
  const options = {};
  const skipped = [];
  for (const [key, value] of Object.entries(settings)) {
    if (NOT_GAMEPLAY.has(key)) continue;
    if (key === "startingItems") {
      const inventory = startInventory(value, itemNames);
      if (inventory === undefined) skipped.push(key);
      else if (Object.keys(inventory).length) options.start_inventory = inventory;
      continue;
    }
    const spec = specs[key];
    const converted = spec === undefined ? undefined : convert(spec, value);
    if (converted === undefined) {
      // Unsupported settings left at OoTMM's default are what the seed gets anyway.
      if (spec !== undefined || !(key in ootmmDefaults) || !sameValue(value, ootmmDefaults[key])) skipped.push(key);
      continue;
    }
    if (!sameValue(converted, spec.default)) options[key] = converted;
  }
  return { options, skipped };
}

function playerYaml(name, goal, options = {}) {
  name = name.trim();
  checkName(name);
  if (!["both", "ganon", "majora", "any"].includes(goal)) throw new Error("Choose a supported goal.");
  const lines = [`name: ${JSON.stringify(name)}`, "game: OOTxMM", "OOTxMM:", `  goal: ${goal}`];
  for (const [key, value] of Object.entries(options)) {
    if (key !== "goal") lines.push(`  ${key}: ${JSON.stringify(value)}`);
  }
  return lines.join("\n") + "\n";
}

if (typeof document !== "undefined") {
  let specs;
  const loadSpecs = async () => {
    if (!specs) {
      const response = await fetch("options.json");
      if (!response.ok) throw new Error("The settings list could not be loaded. Reload the page and try again.");
      specs = await response.json();
    }
    return specs;
  };

  document.getElementById("yaml-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const status = document.getElementById("yaml-status");
    const report = document.getElementById("import-report");
    report.hidden = true;
    try {
      const name = document.getElementById("player").value;
      let goal = document.getElementById("goal").value;
      let imported = { options: {}, skipped: [] };
      const file = document.getElementById("ootmm-settings").files[0];
      if (file) {
        checkName(name.trim());
        let exported;
        try {
          exported = JSON.parse(await file.text());
        } catch {
          throw new Error("This file is not valid JSON. Choose the settings file exported from ootmm.com.");
        }
        imported = importSettings(exported, await loadSpecs());
        const fileGoal = (exported?.data?.settings ?? exported?.settings)?.goal;
        if (specs.options.goal.values.includes(fileGoal)) goal = fileGoal;
      }
      const text = playerYaml(name, goal, imported.options);
      const url = URL.createObjectURL(new Blob([text], { type: "application/yaml;charset=utf-8" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = `${name.trim().replace(/[^a-zA-Z0-9_-]/g, "_") || "player"}.yaml`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      if (file) {
        const count = Object.keys(imported.options).filter((key) => key !== "goal").length;
        status.textContent = `YAML downloaded with ${count} imported setting${count === 1 ? "" : "s"}. Send it to your host.`;
        const list = document.getElementById("import-skipped");
        list.replaceChildren(...imported.skipped.map((key) => {
          const item = document.createElement("li");
          item.textContent = key;
          return item;
        }));
        report.hidden = imported.skipped.length === 0;
      } else {
        status.textContent = "YAML downloaded. Send it to your host.";
      }
    } catch (error) {
      status.textContent = error.message;
    }
  });
}

if (typeof module !== "undefined") module.exports = { importSettings, playerYaml };
