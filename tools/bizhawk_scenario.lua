-- Repeatable scenarios on disposable saves, alongside the standard AP connector.
local dir = assert(userdata.get("out")):gsub("\\", "/")
local connector = assert(userdata.get("connector")):gsub("\\", "/")
local json = require("json")
local wall_time = require("socket").socket.gettime
local started_at = wall_time()
local function readfile(path)
    local file = assert(io.open(path, "r"))
    local data = file:read("*a"); file:close(); return data
end
local scenario = json.decode(readfile(dir .. "/scenario.json"))
local log = assert(io.open(dir .. "/events.jsonl", "w"))
local frame, index, started, finished = 0, 1, 0, false
local function record(value)
    value.frame = frame
    value.elapsed_seconds = wall_time() - started_at
    log:write(json.encode(value) .. "\n"); log:flush()
end
local function probe(p)
    local address = p.address
    if p.pointer then
        address = memory.read_u32_be(p.pointer, "RDRAM") - 0x80000000 + p.address
        assert(address >= 0 and address + p.size <= memory.getmemorydomainsize("RDRAM"), "Invalid probe pointer")
    end
    local value = 0
    for i = 0, p.size - 1 do
        value = value * 256 + memory.read_u8(address + i, "RDRAM")
    end
    return value
end
-- Offsets are from v33.0 combo/{oot,mm}/play.h, combo/actor.h and combo/common/collision_check.h.
-- Collision health is a diagnostic sample; individual actors may store health elsewhere.
local fields = {
    oot = {size = 0x12518, lists = 0x1c30, stride = 8, actor_size = 0x13c, next = 0x124, prev_pos = 0x100, health = 0xaf,
        trigger = 0x11e15, entrance = 0x11e1a, transition_type = 0x11e5e},
    mm = {size = 0x19258, lists = 0x1cb0, stride = 12, actor_size = 0x144, next = 0x12c, prev_pos = 0x108, health = 0xb7,
        trigger = 0x18875, entrance = 0x1887a, transition_type = 0x1887f},
}
local function game_play(game, expected_scene)
    local layout = assert(scenario[game .. "_layout"], "Game layout is required")
    local f = fields[game]
    local play = memory.read_u32_be(layout.play_pointer, "RDRAM") - 0x80000000
    assert(play >= 0 and play + f.size <= memory.getmemorydomainsize("RDRAM"), "Invalid " .. game .. " play pointer")
    assert(memory.read_u32_be(play + 4, "RDRAM") == layout.main, "Active game does not match " .. game .. " payload")
    assert(memory.read_u16_be(play + 0xa4, "RDRAM") == expected_scene, "Unexpected " .. game .. " scene")
    return play, f
end
local function capture(name)
    client.screenshot(dir .. "/" .. name .. ".png")
    savestate.save(dir .. "/" .. name .. ".State")
    local values = {}
    for _, p in ipairs(scenario.probes or {}) do values[p.name] = probe(p) end
    record({event = "capture", name = name, values = values})
    for _, game in ipairs({"oot", "mm"}) do
      if scenario[game .. "_layout"] then
        local layout = scenario[game .. "_layout"]
        local f = fields[game]
        local ptr = memory.read_u32_be(layout.play_pointer, "RDRAM") - 0x80000000
        if ptr >= 0 and ptr + f.size <= memory.getmemorydomainsize("RDRAM") and memory.read_u32_be(ptr + 4, "RDRAM") == layout.main then
            local actors = {}
            for category = 0, 11 do
                local list = ptr + f.lists + category * f.stride
                local count = memory.read_u32_be(list, "RDRAM")
                local actor = memory.read_u32_be(list + 4, "RDRAM") - 0x80000000
                for _ = 1, math.min(count, 128) do
                    if actor < 0 or actor + f.actor_size > memory.getmemorydomainsize("RDRAM") then break end
                    table.insert(actors, {address = actor, id = memory.read_u16_be(actor, "RDRAM"), category = category,
                        params = memory.read_u16_be(actor + 0x1c, "RDRAM"), yaw = memory.read_u16_be(actor + 0x32, "RDRAM"),
                        collision_health = memory.read_u8(actor + f.health, "RDRAM"),
                        x = memory.readfloat(actor + 0x24, true, "RDRAM"), y = memory.readfloat(actor + 0x28, true, "RDRAM"), z = memory.readfloat(actor + 0x2c, true, "RDRAM")})
                    actor = memory.read_u32_be(actor + f.next, "RDRAM") - 0x80000000
                end
            end
            record({event = game .. "_actors", scene = memory.read_u16_be(ptr + 0xa4, "RDRAM"), actors = actors})
        end
      end
    end
end
local function finish(ok, reason)
    if finished then return end
    finished = true
    local captured, err = pcall(capture, ok and "final" or "failure")
    if not captured then ok = false; reason = reason .. "; capture failed: " .. tostring(err) end
    local result = {passed = ok, reason = reason, frame = frame, step = index}
    record(result)
    local file = assert(io.open(dir .. "/result.json", "w"))
    file:write(json.encode(result)); file:close(); log:close()
    client.exitCode(ok and 0 or 1)
end
local boss_support = nil
local function support_boss()
    if not boss_support then return end
    if frame > boss_support.until_frame then
        record({event = "boss_support_end", reason = "frame budget"}); boss_support = nil; return
    end
    local layout = scenario.mm_layout
    local ptr = memory.read_u32_be(layout.play_pointer, "RDRAM") - 0x80000000
    if ptr < 0 or ptr + fields.mm.size > memory.getmemorydomainsize("RDRAM")
        or memory.read_u32_be(ptr + 4, "RDRAM") ~= layout.main
        or memory.read_u16_be(ptr + 0xa4, "RDRAM") ~= 11 then
        record({event = "boss_support_end", reason = "left Majora arena"}); boss_support = nil; return
    end
    local play, f = game_play("mm", 11)
    local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
    assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
    assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
    local save = 0x1ef670
    local capacity = memory.read_u16_be(save + 0x34, "RDRAM")
    assert(capacity >= 0x30 and capacity <= 0x140, "Invalid health capacity")
    assert(memory.read_u8(save + 0x40, "RDRAM") == 1, "Magic must already be acquired")
    memory.write_u16_be(save + 0x36, capacity, "RDRAM")
    local magic = memory.read_u8(save + 0x41, "RDRAM") == 1 and 0x60 or 0x30
    memory.write_u8(save + 0x39, magic, "RDRAM")
    -- Vanilla Boss07 damage handlers use colChkInfo.health for types 10, 20 and 30.
    -- Lower a live phase once; leave damage, death state and final victory to the game.
    local actor = memory.read_u32_be(play + f.lists + 9 * f.stride + 4, "RDRAM") - 0x80000000
    local visited = {}
    while actor >= 0 do
        assert(actor + f.actor_size <= memory.getmemorydomainsize("RDRAM") and not visited[actor], "Invalid boss actor list")
        visited[actor] = true
        local params = memory.read_u16_be(actor + 0x1c, "RDRAM")
        if memory.read_u16_be(actor, "RDRAM") == 0x12f and memory.read_u8(actor + 2, "RDRAM") == 9
            and (params == 10 or params == 20 or params == 30) then
            local key = tostring(actor) .. ":" .. tostring(params)
            local health = memory.read_u8(actor + f.health, "RDRAM")
            if not boss_support.lowered[key] and health >= 1 and health <= 40 then
                memory.write_u8(actor + f.health, 1, "RDRAM")
                boss_support.lowered[key] = true
                record({event = "boss_support_health", actor = actor, phase = params, before = health, after = 1})
            end
        end
        actor = memory.read_u32_be(actor + f.next, "RDRAM") - 0x80000000
    end
end
local ganon_support = nil
local function ganon_actor(play, f)
    local actor = memory.read_u32_be(play + f.lists + 9 * f.stride + 4, "RDRAM") - 0x80000000
    local visited = {}
    while actor >= 0 do
        assert(actor + 0x444 <= memory.getmemorydomainsize("RDRAM") and not visited[actor], "Invalid Ganon actor list")
        visited[actor] = true
        if memory.read_u16_be(actor, "RDRAM") == 0x17a and memory.read_u8(actor + 2, "RDRAM") == 9 then return actor end
        actor = memory.read_u32_be(actor + f.next, "RDRAM") - 0x80000000
    end
    return nil
end
local function support_ganon()
    if not ganon_support then return end
    local layout = scenario.oot_layout
    local ptr = memory.read_u32_be(layout.play_pointer, "RDRAM") - 0x80000000
    if frame > ganon_support.until_frame or ptr < 0 or ptr + fields.oot.size > memory.getmemorydomainsize("RDRAM")
        or memory.read_u32_be(ptr + 4, "RDRAM") ~= layout.main
        or memory.read_u16_be(ptr + 0xa4, "RDRAM") ~= 79 then
        record({event = "ganon_support_end"}); ganon_support = nil; return
    end
    local capacity = memory.read_u16_be(0x11a5d0 + 0x2e, "RDRAM")
    assert(capacity >= 0x30 and capacity <= 0x140, "Invalid health capacity")
    memory.write_u16_be(0x11a5d0 + 0x30, capacity, "RDRAM")
    local actor = ganon_actor(ptr, fields.oot)
    if actor then
        local health = memory.read_u8(actor + 0xaf, "RDRAM")
        -- Native Ganon initializes health to 30, then resets it to 25 after the first phase.
        if (health == 30 or health == 25) and not ganon_support.lowered[health] then
            ganon_support.lowered[health] = true
            memory.write_u8(actor + 0xaf, 1, "RDRAM")
            record({event = "ganon_support_health", actor = actor, before = health, after = 1})
        end
    end
end
local function tick()
    if finished then return end
    frame = frame + 1
    local neutral = {}
    for button, _ in pairs(joypad.get()) do neutral[button] = false end
    joypad.set(neutral)
    joypad.setanalog({["P1 X Axis"] = 0, ["P1 Y Axis"] = 0})
    if frame > scenario.max_frames then finish(false, "Scenario frame budget exceeded"); return end
    support_boss()
    support_ganon()
    local step = scenario.steps[index]
    if not step then finish(true, "All scenario steps completed"); return end
    local elapsed = frame - started
    if elapsed == 1 then record({event = "step", index = index, action = step.action}) end
    local done = false
    if step.action == "boot_file" then
        local layout = scenario.oot_layout
        local play = memory.read_u32_be(layout.play_pointer, "RDRAM") - 0x80000000
        done = play >= 0 and play + fields.oot.size <= memory.getmemorydomainsize("RDRAM")
            and memory.read_u32_be(play + 4, "RDRAM") == layout.main
            and memory.read_u32_be(0x11a5d0 + 0x135c, "RDRAM") == 0
            and memory.read_u16_be(play + 0xa4, "RDRAM") == step.scene
        if not done then
            local buttons = {"P1 Start", "P1 A", "P1 A", "P1 Start", "P1 A"}
            local press = math.floor((elapsed - 1) / 38)
            if (elapsed - 1) % 38 < 8 then joypad.set({[buttons[press % #buttons + 1]] = true}) end
            if elapsed >= step.timeout_frames then finish(false, "No gameplay after automated file creation"); return end
        end
    elseif step.action == "input" then
        joypad.set(step.buttons or {})
        joypad.setanalog(step.analog or {})
        done = elapsed >= step.frames
    elseif step.action == "wait" then
        done = elapsed >= step.frames
    elseif step.action == "capture" then
        capture(step.name); done = true
    elseif step.action == "mm_boss_approach" then
      if boss_support then
        local play, f = game_play("mm", 11)
        local actor = memory.read_u32_be(play + f.lists + 9 * f.stride + 4, "RDRAM") - 0x80000000
        local visited, target = {}, nil
        while actor >= 0 do
            assert(actor + f.actor_size <= memory.getmemorydomainsize("RDRAM") and not visited[actor], "Invalid boss actor list")
            visited[actor] = true
            local params = memory.read_u16_be(actor + 0x1c, "RDRAM")
            local health = memory.read_u8(actor + f.health, "RDRAM")
            if memory.read_u16_be(actor, "RDRAM") == 0x12f and memory.read_u8(actor + 2, "RDRAM") == 9
                and (params == 10 or params == 20 or params == 30) and health >= 1 and health <= 40 then
                target = actor; break
            end
            actor = memory.read_u32_be(actor + f.next, "RDRAM") - 0x80000000
        end
        if target then
            local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
            assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
            assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
            local yaw = memory.read_u16_be(target + 0xbe, "RDRAM")
            local radians = yaw * math.pi / 32768
            local x = memory.readfloat(target + 0x24, true, "RDRAM") - math.sin(radians) * 160
            local y = math.max(0, memory.readfloat(target + 0x28, true, "RDRAM") - 80)
            local z = memory.readfloat(target + 0x2c, true, "RDRAM") - math.cos(radians) * 160
            assert(math.abs(x) <= 1500 and y <= 1000 and math.abs(z) <= 1500, "Unexpected boss position")
            for _, offset in ipairs({0x24, f.prev_pos}) do
                memory.writefloat(player + offset, x, true, "RDRAM")
                memory.writefloat(player + offset + 4, y, true, "RDRAM")
                memory.writefloat(player + offset + 8, z, true, "RDRAM")
            end
            memory.write_u16_be(player + 0x32, yaw, "RDRAM")
            memory.write_u16_be(player + 0xbe, yaw, "RDRAM")
            record({event = "boss_approach", target = target, x = x, y = y, z = z, yaw = yaw})
        end
      end
        done = true
    elseif step.action == "mm_boss_support" then
        game_play("mm", 11)
        boss_support = {until_frame = frame + step.frames, lowered = {}}
        record({event = "boss_support_start", frames = step.frames,
            assistance = "health/magic refill; each live Majora phase reduced to one health"})
        done = true
    elseif step.action == "oot_boss_arm" then
        local play, f = game_play("oot", 79)
        local save = 0x11a5d0
        local owned = memory.read_u16_be(save + 0x9c, "RDRAM") % 16
        local master = step.sword == "master"
        assert(master and owned % 4 >= 2 or not master and owned % 8 >= 4, "Receive the requested sword before equipping")
        memory.write_u8(save + 0x68, master and 0x3c or 0x3d, "RDRAM")
        local equips = memory.read_u16_be(save + 0x70, "RDRAM")
        memory.write_u16_be(save + 0x70, equips - equips % 16 + (master and 2 or 3), "RDRAM")
        -- eventsMisc[29] is only the native swordless equipment state.
        memory.write_u16_be(save + 0xef8 + 29 * 2, 0, "RDRAM")
        record({event = "ganon_arm", sword = step.sword})
        done = true
    elseif step.action == "oot_boss_weapon" then
        local play, f = game_play("oot", 79)
        assert(ganon_actor(play, f), "Ganon must be present")
        local effects = memory.read_u32_be(play + 0x11e10, "RDRAM") - 0x80000000
        assert(effects >= 0 and effects + 0x44 <= memory.getmemorydomainsize("RDRAM"), "Invalid Ganon effects pointer")
        local actor = ganon_actor(play, f)
        local health = memory.read_u8(actor + 0xaf, "RDRAM")
        if (health == 0 or health >= 128) and memory.read_u8(effects, "RDRAM") == 1
            and memory.read_u16_be(effects + 0x2e, "RDRAM") == 1 then
            local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
            assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
            assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
            local x = memory.readfloat(effects + 4, true, "RDRAM")
            local z = memory.readfloat(effects + 12, true, "RDRAM")
            assert(math.abs(x) <= 2000 and math.abs(z) <= 2000, "Unexpected sword position")
            for _, offset in ipairs({0x24, f.prev_pos}) do
                memory.writefloat(player + offset, x, true, "RDRAM")
                memory.writefloat(player + offset + 4, 1086, true, "RDRAM")
                memory.writefloat(player + offset + 8, z, true, "RDRAM")
            end
            record({event = "ganon_weapon_approach", x = x, z = z})
        end
        done = true
    elseif step.action == "oot_boss_support" then
        game_play("oot", 79)
        ganon_support = {until_frame = frame + step.frames, lowered = {}}
        record({event = "ganon_support_start", frames = step.frames})
        done = true
    elseif step.action == "oot_boss_approach" then
      if ganon_support then
        local play, f = game_play("oot", 79)
        local actor = ganon_actor(play, f)
        if actor and memory.readfloat(actor + 0x28, true, "RDRAM") >= 1000 then
            local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
            assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
            assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
            local health = memory.read_u8(actor + 0xaf, "RDRAM")
            local x, y, z
            if health == 0 or health >= 128 then
                -- Native final-blow camera target is the head position at retail offset 0x1a8 (debug Actor adds 0x10).
                x = memory.readfloat(actor + 0x1a8, true, "RDRAM")
                y = memory.readfloat(actor + 0x1ac, true, "RDRAM")
                z = memory.readfloat(actor + 0x1b0, true, "RDRAM")
            else
                -- The native damage handler tests JntSph element 15 for tail hits.
                assert(memory.read_u32_be(actor + 0x414 + 0x18, "RDRAM") >= 16, "Missing tail collider")
                local elements = memory.read_u32_be(actor + 0x414 + 0x1c, "RDRAM") - 0x80000000
                assert(elements >= 0 and elements + 16 * 0x40 <= memory.getmemorydomainsize("RDRAM"), "Invalid tail collider pointer")
                local sphere = elements + 15 * 0x40 + 0x30
                x = memory.read_s16_be(sphere, "RDRAM")
                y = memory.read_s16_be(sphere + 2, "RDRAM")
                z = memory.read_s16_be(sphere + 4, "RDRAM")
            end
            assert(math.abs(x) <= 2000 and y >= 1000 and y <= 1800 and math.abs(z) <= 2000, "Unexpected Ganon interaction point")
            y = math.max(1086, y - 40)
            -- Keep final-blow setup on the arena floor, facing the head.
            if health == 0 or health >= 128 then
                y = 1086
                memory.write_u16_be(player + 0x32, 0x8000, "RDRAM")
                memory.write_u16_be(player + 0xb6, 0x8000, "RDRAM")
            end
            z = z + 35
            for _, offset in ipairs({0x24, f.prev_pos}) do
                memory.writefloat(player + offset, x, true, "RDRAM")
                memory.writefloat(player + offset + 4, y, true, "RDRAM")
                memory.writefloat(player + offset + 8, z, true, "RDRAM")
            end
            record({event = "ganon_approach", x = x, y = y, z = z, health = health})
        end
      end
        done = true
    elseif step.action == "oot_boss_loadout" then
        local play, f = game_play("oot", step.scene)
        assert(memory.read_u8(play + f.trigger, "RDRAM") == 0, "Transition already active")
        local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
        assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
        assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
        local save = 0x11a5d0
        assert(memory.read_u16_be(save + 0x9c, "RDRAM") % 4 >= 2, "Receive the Master Sword before preparing Ganon")
        -- Age_SetRawOot defers the change through PlayState.linkAgeOnLoad.
        -- Age_OnChangeOot restores adultEquips during the following scene load.
        memory.write_u8(play + 0x11de8, 0, "RDRAM")
        memory.write_u16_be(save + 0x2e, 0x140, "RDRAM")
        memory.write_u16_be(save + 0x30, 0x140, "RDRAM")
        memory.write_u8(save + 0x4a, 0x3c, "RDRAM")
        local equips = memory.read_u16_be(save + 0x52, "RDRAM")
        memory.write_u16_be(save + 0x52, equips - equips % 16 + 2, "RDRAM")
        record({event = "setup_loadout", game = "oot", scene = step.scene,
            equipment = "Adult on next scene load, acquired Master Sword equipped, twenty hearts"})
        done = true
    elseif step.action == "mm_boss_loadout" then
        local play, f = game_play("mm", step.scene)
        assert(memory.read_u8(play + f.trigger, "RDRAM") == 0, "Transition already active")
        local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
        assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
        assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
        -- v33.0 link_mm.in gSaveContext; mm/save.h MmSave.info (0x24), player data,
        -- equips (0x4c), inventory (0x70); data/items.h item and slot IDs.
        local save = 0x1ef670
        assert(memory.read_u8(save + 0x20, "RDRAM") == 4, "Loadout requires human form")
        memory.write_u16_be(save + 0x34, 0x140, "RDRAM")
        memory.write_u16_be(save + 0x36, 0x140, "RDRAM")
        memory.write_u8(save + 0x38, 2, "RDRAM")
        memory.write_u8(save + 0x39, 0x60, "RDRAM")
        memory.write_u8(save + 0x40, 1, "RDRAM")
        memory.write_u8(save + 0x41, 1, "RDRAM")
        memory.write_u8(save + 0x4c, 0x4f, "RDRAM")
        memory.write_u8(save + 0x4d, 0x35, "RDRAM")
        memory.write_u8(save + 0x5d, 0x2f, "RDRAM")
        local equips = memory.read_u16_be(save + 0x6c, "RDRAM")
        memory.write_u16_be(save + 0x6c, equips - equips % 16 + 3, "RDRAM")
        memory.write_u8(save + 0x9f, 0x35, "RDRAM")
        record({event = "setup_loadout", game = "mm", scene = step.scene,
            equipment = "Gilded Sword, Fierce Deity mask on C-left, full health and magic"})
        done = true
    elseif step.action == "oot_transition" or step.action == "mm_transition" then
        local game = step.action:sub(1, -12)
        local play, f = game_play(game, step.from_scene)
        assert(memory.read_u8(play + f.trigger, "RDRAM") == 0, "Transition already active")
        memory.write_u16_be(play + f.entrance, step.entrance, "RDRAM")
        memory.write_u8(play + f.transition_type, 2, "RDRAM")
        memory.write_u8(play + f.trigger, 0x14, "RDRAM")
        record({event = "setup_transition", game = game, entrance = step.entrance, from_scene = step.from_scene})
        done = true
    elseif step.action == "oot_position" or step.action == "mm_position" then
        local game = step.action:sub(1, -10)
        local play, f = game_play(game, step.scene)
        local player = memory.read_u32_be(play + f.lists + 2 * f.stride + 4, "RDRAM") - 0x80000000
        assert(player >= 0 and player + f.actor_size <= memory.getmemorydomainsize("RDRAM"), "Invalid player pointer")
        assert(memory.read_u16_be(player, "RDRAM") == 0 and memory.read_u8(player + 2, "RDRAM") == 2, "Player actor guard failed")
        memory.writefloat(player + 0x24, step.x, true, "RDRAM")
        memory.writefloat(player + 0x28, step.y, true, "RDRAM")
        memory.writefloat(player + 0x2c, step.z, true, "RDRAM")
        if step.yaw then
            memory.write_u16_be(player + 0x32, step.yaw, "RDRAM")
            memory.write_u16_be(player + (game == "oot" and 0xb6 or 0xbe), step.yaw, "RDRAM")
        end
        -- Keep collision sweeps local to the destination instead of crossing intervening walls.
        memory.writefloat(player + f.prev_pos, step.x, true, "RDRAM")
        memory.writefloat(player + f.prev_pos + 4, step.y, true, "RDRAM")
        memory.writefloat(player + f.prev_pos + 8, step.z, true, "RDRAM")
        if elapsed == 1 then record({event = "setup_position", game = game, x = step.x, y = step.y, z = step.z, frames = step.frames or 1}) end
        done = elapsed >= (step.frames or 1)
    elseif step.action == "wait_client" then
        local ready = io.open(dir .. "/client-ready.json", "r")
        if ready then
            ready:close()
            record({event = "client_ready"})
            done = true
        elseif elapsed >= step.timeout_frames then
            finish(false, "Timed out waiting for the live client query"); return
        end
    elseif step.action == "wait_game" then
        -- During a native game switch gPlay can be null or point at the departing payload.
        local active = pcall(game_play, step.game, step.scene)
        done = active
        if done then
            record({event = "game_ready", game = step.game, scene = step.scene})
        elseif elapsed >= step.timeout_frames then
            finish(false, "Timed out waiting for " .. step.game .. " scene " .. step.scene); return
        end
    elseif step.action == "expect" then
        local value = probe(step)
        done = value == step.value
        if done then record({event = "expect", name = step.name, value = value})
        elseif elapsed >= step.timeout_frames then
            finish(false, "Timed out: " .. step.name .. ", observed " .. tostring(value)); return
        end
    else
        finish(false, "Unknown scenario action"); return
    end
    if done then index = index + 1; started = frame end
end
event.onframestart(function()
    local ok, err = pcall(tick)
    if not ok then finish(false, tostring(err)) end
end, "scenario")
record({event = "start", rom = gameinfo.getromname()})
dofile(connector)
