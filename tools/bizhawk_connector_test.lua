-- Disposable-save harness: dismiss received-item text and run the standard AP connector.
local dir = assert(userdata.get("out")):gsub("\\", "/")
local connector = assert(userdata.get("connector"))
event.onframestart(function()
    joypad.set({["P1 B"] = emu.framecount() % 30 < 8})
end)
event.onframeend(function()
    if emu.framecount() % 300 == 0 then client.screenshot(dir .. "/delivery.png") end
end)
dofile(connector)
