-- Command-line boot check. Pass --userdata=out:<absolute output directory> with --lua=<this file>.
-- Uses a separate emulator config/save directory; never load a player's existing save for this check.
local dir = assert(userdata.get("out"), "Pass --userdata=out:<output directory>"):gsub("\\", "/")
local out = assert(io.open(dir .. "/boot.txt", "w"))
local function log(s) out:write(s .. "\n"); out:flush() end
local function wait(n) for _ = 1, n do emu.frameadvance() end end
local function tap(button)
    for _ = 1, 8 do joypad.set({[button] = true}); emu.frameadvance() end
    for _ = 1, 30 do joypad.set({[button] = false}); emu.frameadvance() end
end
local function scan()
    local matches = {}
    local magic = "OoTMM-IPC-RAM-1\0"
    for base = 0, memory.getmemorydomainsize("RDRAM") - 0x8000, 0x8000 do
        local data = memory.read_bytes_as_array(base, 0x8000, "RDRAM")
        for offset = 0, 0x8000 - 24, 16 do
            local same = true
            for j = 1, #magic do
                if data[offset + j] ~= magic:byte(j) then same = false; break end
            end
            if same then matches[base + offset] = memory.read_u32_be(base + offset + 20, "RDRAM") end
        end
    end
    return matches
end
log("ROM " .. gameinfo.getromname())
for button, _ in pairs(joypad.get()) do log("control " .. button) end
wait(1200)
log("startup frames advanced")
local candidates = scan()
local buttons = {"P1 Start", "P1 A", "P1 A", "P1 Start", "P1 A"}
local mailbox = nil
for n = 1, 200 do
    tap(buttons[(n - 1) % #buttons + 1])
    if n % 10 == 0 then
        log("file-menu input batch " .. n)
        client.screenshot(dir .. "/boot-progress.png")
        local current = scan()
        for address, alive in pairs(current) do
            if candidates[address] and candidates[address] ~= alive then mailbox = address; break end
        end
        candidates = current
        if mailbox then break end
    end
end
if not mailbox then
    client.screenshot(dir .. "/boot-failed.png")
    log("FAIL: no moving mailbox after automated file creation")
    out:close()
    client.exitCode(1)
    return
end
for _ = 1, 40 do tap("P1 B") end
log(string.format("PASS: live mailbox at 0x%X, alive=%d", mailbox,
                  memory.read_u32_be(mailbox + 20, "RDRAM")))
savestate.save(dir .. "/gameplay.State")
client.screenshot(dir .. "/gameplay.png")
out:close()
client.exitCode(0)
