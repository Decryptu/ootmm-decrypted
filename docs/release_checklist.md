# Release readiness

Work through these gates before handing out the next playtest build. Keep unfinished work here; remove completed tasks after recording reproducible validation with the frozen build. The player-facing scenarios are in [the playtest checklist](playtest_en.md).

## 1. Reproducible gameplay setup

Use the [isolated scenario harness](gameplay_testing.md) with separate configuration, saves, matching ROMs and temporary servers. Keep source-verified layouts pinned to the ROM hash, record seed/slot/settings and inherited assistance beside checkpoints, and retain inputs, logs, screenshots and server assertions under ignored `dist/`. Preserve frozen packages and player saves.

Test shortcuts may prepare inventory, position the player, enter a boss room, enable invulnerability or reduce enemy health. They must leave the actual chest interaction, transition or final defeat handler to the game. Writing a boss flag, location flag, mailbox packet or server check directly is protocol coverage, not proof of gameplay reporting. If a shortcut skips part of a route, record that limit.

## 2. Actual pickups and delivery

The candidate verifies its native cross-game door, MM opening-song award, bidirectional OoT chest exchange and the remote South Clock Town chest with two running players. Both receipt indices remain stable; the MM chest's recipient has the native Mirror Shield equipped after switching to MM. OoT nut upgrade inventory and refill are covered by the OoT exchange.

- [ ] Verify representative shop, dungeon reward and fixed vanilla checks; candidate song coverage currently uses the MM opening award.
- [ ] Verify remote key use at the intended doors, Ganon's boss key and temple fairy rewards. Diagnostic candidate grants already verify the native Fire Temple small-key count/boss-key bit and the Woodfall fairy counter; these are item-application coverage, not actual source pickups or door use.
- [ ] Exercise shared equipment and songs in both games; check upgrades and abilities as well as item messages.

## 3. Recovery and load

- [ ] Collect and receive remote items after each direction of a continuous candidate round trip. The candidate verifies both native entrance directions, both mailbox changes and the MM opening-song award persisting on return to OoT; direct mailbox lookup and cached reattachment pass. Include actual source pickups and remote receipt after each switch. New builds carry both compiled mailbox addresses, and sequential attached/control round trips verify first-arrival discovery without full RAM scans.
- [ ] Repeat native-save/cold-boot recovery on the final candidate, including pending checks. The earlier seed retains the song and opened chest across fresh emulator/client/server processes, then reports a new own chest and verifies its inventory item. Another native save/cold boot retains received index 3 with no replay after three simulated remote source checks. A separate real own-item pickup while disconnected recovers its pending check after reconnect.
- [ ] Repeat disconnected real-pickup recovery on the final candidate and interrupt a socket during reporting. The earlier seed grants the own Odd Potion while disconnected and reports its pending Mido chest exactly once after reconnect. A second real Mido chest interaction begun offline also recovers after reconnect, with exactly one award for each chest. The source waits for the first pending acknowledgement before sending the second pickup; unrestricted offline play is not established.
- [ ] Repeat disconnected-recipient backlog delivery on the final candidate with real source pickups. On the earlier seed, three simulated remote source checks queue while disconnected; the real recipient game reaches received index 3 after reconnect and remains there through 16 further polls, while its actual offline own-item chest reports exactly once.
- [ ] Restart the server with its existing disposable save and verify delivery resumes.
- [ ] Exercise rapid pickups, queued deliveries, dialogue, pause and fast-forward. Measure ring occupancy and recovery; investigate any repeated handshake, freeze or missing item.

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
