# OOTxMM playtest

Use the same world build for both players, Archipelago 0.6.8, BizHawk 2.11.1 and OoTMM v33.0. Follow [setup](setup_en.md) first. Keep the seed's spoiler with the host so expected items can be checked without revealing the whole seed to players.

## Before the session

- Give each player their own `.ootmm` patch, the matching `ootxmm.apworld`, their slot name and server connection details. Share patches, never ROMs.
- Apply each patch with the v33.0 browser generator. Confirm the downloaded ROM starts in BizHawk and both games can enter gameplay.
- Keep the generated `.archipelago` file and its server save together. Both players should use `goal: both` to exercise boss persistence.
- Record the build's SHA-256, seed name and each player's emulator version. Use in-game saves for restart tests; loading an older savestate can rewind the game's received-item index.

## Short connection test

1. Connect both slots. Confirm each client finds its mailbox and connects to the game.
2. Open a shuffled check containing your own item. Confirm the item is given once and the server records the check.
3. Open a shuffled check containing the other player's item. Confirm the server records the correct check and the other player gets the expected item once. Repeat in the other direction. The host can find suitable checks in the spoiler.
4. Save, close the client, reopen it and reconnect to the same slot. Confirm received items already saved are not given again, and new checks still work.
5. Disconnect one client from the server, then collect a check. Reconnect and confirm the pending check is reported and play resumes. Record any freeze and whether reconnecting releases it.
6. Send an item to a disconnected player. Reconnect that player and confirm it arrives once.
7. Switch OoT to MM and back through normal game transitions. After each switch, confirm new checks and received items work. Watch for repeated reconnects during normal play, rapid pickups or fast-forward: these may expose a full mailbox ring.

## During the full playthrough

- Verify at least one own check and one remote check in each game, plus a song, dungeon item, shop and fixed vanilla check. Fixed checks should retain their vanilla behavior.
- If using dungeon keysanity, receive a remote small key and boss key and confirm each opens the intended dungeon's door. With removed keys, confirm those doors open without receiving keys. Include Fire Temple when testing OoT small keys.
- Check Ganon's boss door against `ganonBossKey`: removed opens without a key; vanilla keeps the key in its original chest; ganon places it in the Castle or Tower; anywhere can require a remote delivery. Confirm a received key opens the door.
- For a dungeon-only or anywhere-rewards seed, receive a remote spiritual stone, medallion or boss remain and check that its inventory icon and related progression update. Blue warps may give ordinary or remote items in this mode.
- For `songs: anywhere`, receive a song from another player, play it in its game, and check that a song-teaching check can award a different item.
- For stray-fairy seeds, receive a remote fairy and check that it increments the correct temple counter. Test chest and freestanding pickups with mixed shuffle settings, then claim a Great Fairy reward.
- With starting maps, compasses or fairies, check the inventory before connecting, then connect and confirm those grants are not duplicated. Removed freestanding fairies also grant their counters; their pickup checks should be absent.
- For Tingle maps, confirm vanilla purchases keep their maps, anywhere purchases can give shuffled items, starting grants all six maps before connecting, and removed grants none. Starting and removed keep the purchase checks available for other items.
- Note any route the spoiler expects but gameplay cannot reach, especially MM clock windows and areas with conditional waiting. Logic tracks clock ranges and regional constraints; compare the expected arrival time and available waiting conditions with gameplay.
- For `goal: both`, beat one boss and confirm the slot has not finished. Save, restart the client and reconnect, then beat the other boss. Confirm the server marks the slot complete. If possible, use the opposite boss order for the other player.
- Restart the server with its existing save between boss victories and confirm progress survives. Do not remove the save or start another seed for this test.

## Report a problem

Send the host the slot name, check or boss name, expected and actual result, whether the game was OoT or MM, and the steps immediately before the problem. Include the client and server logs and a screenshot when useful. Record whether reconnecting, switching games or restarting changes the behavior. Keep ROMs out of reports.
