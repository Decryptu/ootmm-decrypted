"use strict";

function playerYaml(name, goal) {
  name = name.trim();
  // The characters YAML files can't hold, and the name Archipelago keeps for itself, fail generation for everyone.
  if (!name || [...name].length > 16 || /[{}\x00-\x1f\x7f-\x84\x86-\x9f\ufffe\uffff]/u.test(name)) {
    throw new Error("Enter a name of 1–16 characters without braces or control characters.");
  }
  if (name === "Archipelago") throw new Error("That name is reserved. Choose another.");
  if (!["both", "ganon", "majora", "any"].includes(goal)) throw new Error("Choose a supported goal.");
  return `name: ${JSON.stringify(name)}\ngame: OOTxMM\nOOTxMM:\n  goal: ${goal}\n`;
}

document.getElementById("yaml-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const status = document.getElementById("yaml-status");
  try {
    const name = document.getElementById("player").value;
    const text = playerYaml(name, document.getElementById("goal").value);
    const url = URL.createObjectURL(new Blob([text], { type: "application/yaml;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `${name.trim().replace(/[^a-zA-Z0-9_-]/g, "_") || "player"}.yaml`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = "YAML downloaded. Send it to your host.";
  } catch (error) {
    status.textContent = error.message;
  }
});
