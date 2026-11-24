-- Hook: vanilla hud.lua always require()s T6.Zombie.HudTimerZombie in ZM, after HudPerksZombie.
-- The vanilla file is only the Turned (zcleansed) timer, stubbed below. Use this mod for Origins only.
CoD.GameTimerZombie = {}
LUI.createMenu.TimerAreaZM = function(controller)
	local w = CoD.Menu.NewSafeAreaFromState("TimerAreaZM", controller)
	w:setOwner(controller)
	return w
end

CoD.MiniMapa = {}
local MM = CoD.MiniMapa
MM.Size = 200 -- LUI units (720 high screen)
MM.Range = 1750 -- world units from center to edge
MM.CenterX = 128
MM.CenterY = 808
MM.World = 10000
MM.Material = "menu_lobby_icon_twitter"
-- Atlas image: underground (top left) and Crazy Place (bottom right), each with its own transform
MM.CrazyMaterial = "zombies_rank_5"
MM.CrazyX = 7669.9
MM.CrazyY = -4993.9
MM.CrazyWorld = 8378.2
MM.CrazyRange = 900
-- one isolated tile per underground structure
MM.AtlasB = "menu_lobby_icon_facebook"
-- x, y, atlas
MM.Under = {
	{ 3326.2, -3308.2, 1 },
	{ -3124.0, -3537.7, 1 },
	{ -448.2, -2292.6, 1 },
	{ 4742.3, -2058.2, 1 },
	{ 2857.5, 4367.6, 1 },
	{ -2826.1, -2600.2, 1 },
	{ 5772.5, 8244.5, 1 },
	{ -731.4, 6042.4, 1 },
	{ 5357.5, 393.0, 2 },
	{ -2577.1, -3337.5, 2 },
	{ -3558.5, 983.8, 2 },
	{ 4517.6, 4118.5, 2 },
	{ 372.1, 3483.8, 2 },
	{ -2752.9, 1911.5, 2 },
	{ 5264.7, 6276.8, 2 },
}
MM.UnderWorld = 10000.0
MM.BigSize = 640
-- icons that belong to the game itself; only their names are used here
MM.PerkMat = {
	J = "specialty_juggernaut_zombies", R = "specialty_quickrevive_zombies", S = "specialty_fastreload_zombies",
	M = "specialty_marathon_zombies", K = "specialty_additionalprimaryweapon_zombies",
}
-- fixed places: x, y, kind
MM.Fixed = {
	{ 2328, -232, "J" },
	{ -2355, -36, "M" },
	{ 0, -480, "K" },
	{ 2360, 5096, "R" },
	{ 888, 3288, "S" },
	{ -268, 3712, "W" },
	{ 928, -3432, "W" },
	{ 2660, 76, "W" },
	{ -2360, 176, "W" },
	{ 772, 2544, "W" },
	{ 2968, 5368, "W" },
	{ 526, 2340, "G3" },
	{ -2626, 176, "G5" },
	{ 2368, 240, "G4" },
	{ 2169, 4784, "G1" },
	{ -352, 3448, "G2" },
	{ 960, -3712, "G6" },
}
-- caves drawn whole on the full map: atlas tile, left, right, bottom, top (world)
MM.BigCaves = {
	{ 1, -517, 504, -505, 549 },
	{ 2, -3397, -2846, -598, 188 },
	{ 3, 2218, 3561, 666, 1409 },
	{ 4, 1202, 1617, -2581, -1541 },
	{ 5, 2447, 3273, 4060, 4665 },
	{ 6, -321, 1349, -3093, -2112 },
	{ 7, 1847, 3038, 4246, 5564 },
	{ 8, -1259, -194, 2214, 3196 },
	{ 9, 1647, 2403, 3157, 4289 },
	{ 10, -2924, -2221, -481, 466 },
	{ 11, -604, 162, 4079, 4548 },
	{ 12, 919, 1451, 3840, 4392 },
	{ 13, 148, 602, 3376, 3581 },
	{ 14, 357, 812, 1804, 2009 },
	{ 15, 1710, 2159, 2790, 3083 },
}
MM.BigLabels = {
	{ 1700, 5600, "LABORATORIO" }, { 0, 5080, "ESTACION DEL TANQUE" }, { -380, 3200, "BUNKER DEL TANQUE - G2" },
	{ 400, 1780, "TRINCHERA CENTRAL - G3" }, { 2450, 2250, "TRINCHERAS" }, { -1050, 1300, "TIERRA DE NADIE" },
	{ 1550, 250, "TIERRA DE NADIE" }, { 0, -760, "MID - EXCAVACION" }, { 3050, -620, "ZONA DE JUGGERNOG - G4" },
	{ -2700, 1050, "GRANJA - G5" }, { -1900, -2000, "ALDEA" }, { -1100, -3350, "ESTACION DEL TANQUE" },
	{ 600, -2500, "IGLESIA" }, { 2450, -3800, "DETRAS DE LA IGLESIA - G6" },
	{ 3930, 4450, "CUEVA DE FUEGO", 1, 0.4, 0.25 }, { 3350, 1780, "CUEVA DE VIENTO", 0.95, 0.9, 0.5 },
	{ -3250, -850, "CUEVA DE RAYO", 0.8, 0.5, 1 }, { 2340, -2000, "CUEVA DE HIELO", 0.4, 0.8, 1 },
}
MM.DotMat = "zombies_rank_3_ded"
MM.ArrowMat = "zombies_rank_4_ded"
MM.PanzerMat = "zombies_rank_5_ded"
-- one colour per player number
MM.AllyColor = {
	{ 0.25, 0.65, 1 }, { 1, 0.85, 0.2 }, { 0.25, 0.95, 0.4 }, { 1, 0.45, 0.85 },
}
MM.CaveRange = 1000
MM.CryptRange = 750
MM.MaxZombies = 24
MM.MaxAllies = 3
MM.MaxMech = 3
MM.MaxPoi = 20
MM.PoiColor = {
	J = { 0.9, 0.2, 0.2 }, R = { 0.3, 0.6, 1 }, S = { 0.2, 0.8, 0.35 }, M = { 1, 0.75, 0.2 },
	K = { 0.2, 0.7, 0.5 }, W = { 0.8, 0.4, 1 }, B = { 0.3, 0.85, 1 }, P = { 1, 0.5, 0.9 }, G = { 0.95, 0.95, 0.95 }, H = { 0.3, 1, 0.4 },
}

local function dvarNum(name, default)
	return tonumber(UIExpression.DvarString(nil, name)) or default
end

local function place(e, cx, cy, half, smooth)
	if smooth > 0 then
		e:beginAnimation("mm", smooth)
	end
	e:setLeftRight(false, false, cx - half, cx + half)
	e:setTopBottom(false, false, cy - half, cy + half)
end

local function image(parent, material, size, r, g, b, a)
	local e = LUI.UIImage.new()
	e:setLeftRight(false, false, -size / 2, size / 2)
	e:setTopBottom(false, false, -size / 2, size / 2)
	e:setImage(RegisterMaterial(material))
	e:setRGB(r, g, b)
	e:setAlpha(a)
	parent:addElement(e)
	return e
end

local function show(e, a)
	if e.shown ~= a then
		e.shown = a
		e:setAlpha(a)
	end
end

-- New packet (about 20 per second): remember where we were drawn and where to go next.
local function follow(list, id, x, y, seq)
	local o = list[id]
	if not o then
		o = { x = x, y = y, fx = x, fy = y }
		list[id] = o
	else
		o.fx, o.fy = o.x, o.y
		-- far jump: teleport or reused number
		if math.abs(x - o.x) + math.abs(y - o.y) > 400 then
			o.fx, o.fy = x, y
		end
	end
	o.tx, o.ty, o.seq = x, y, seq
	return o
end

local function parse(self, state)
	local n = {}
	for v in string.gmatch(state, "%-?%d+") do
		n[#n + 1] = tonumber(v)
	end
	self.visible = #n >= 5 and n[2] == 1
	if not self.visible then
		self.me = nil
		return
	end
	local x, y, yaw = n[3], n[4], n[5] / 10
	local me = self.me
	if not me or math.abs(x - me.x) + math.abs(y - me.y) > 600 then
		me = { x = x, y = y, yaw = yaw }
		self.me = me
		self.ents, self.footPos = {}, {}
	end
	me.fx, me.fy, me.fyaw = me.x, me.y, me.yaw
	local turn = (yaw - me.yaw) % 360
	if turn > 180 then
		turn = turn - 360
	end
	me.tx, me.ty, me.tyaw = x, y, me.yaw + turn
	self.part = n[6] or 0

	self.packet = (self.packet or 0) + 1
	for k = 0, 3 do
		local list = UIExpression.DvarString(nil, "mm_e" .. k)
		if list then
			for ex, ey, h, id in string.gmatch(list, "(%-?%d+),(%-?%d+),(%d),(%d+)") do
				follow(self.ents, id, tonumber(ex), tonumber(ey), self.packet).h = h
			end
		end
	end
	local yaws = UIExpression.DvarString(nil, "mm_ay")
	if yaws then
		for id, a in string.gmatch(yaws, "(%d+),(%-?%d+)") do
			if self.ents[id] then
				self.ents[id].yaw = tonumber(a)
			end
		end
	end
	for id, o in pairs(self.ents) do
		if o.seq ~= self.packet then
			self.ents[id] = nil
		end
	end
	local feet = UIExpression.DvarString(nil, "mm_feet")
	local fi = 0
	if feet then
		for ex, ey, a in string.gmatch(feet, "(%-?%d+),(%-?%d+),(%d)") do
			fi = fi + 1
			follow(self.footPos, fi, tonumber(ex), tonumber(ey), self.packet).a = a
		end
	end
	for i = fi + 1, 6 do
		self.footPos[i] = nil
	end
	-- these change rarely
	if self.packet % 20 == 1 or not self.poiList then
		self.poiList = {}
		for k = 0, 1 do
			local list = UIExpression.DvarString(nil, "mm_poi" .. k)
			if list then
				for ex, ey, t in string.gmatch(list, "(%-?%d+),(%-?%d+),(%a%d?)") do
					self.poiList[#self.poiList + 1] = { x = tonumber(ex), y = tonumber(ey), t = t }
				end
			end
		end
		self.zoom = math.max(700, math.min(2500, dvarNum("mm_zoom", MM.Range)))
		self.rotsign = dvarNum("mm_rotsign", 1)
		self.giro = dvarNum("mm_giro", 1)
		if Engine and Engine.SetDvar then
			Engine.SetDvar("mm_tpp", math.floor((self.tpp or 0) * 10))
		end
	end
end

local function fixedAlpha(f, part)
	if f[3] == "K" then
		return part == 1 and 1 or 0
	end
	local box = MM.BigCaves[part]
	if not box or (f[1] > box[2] and f[1] < box[3] and f[2] > box[4] and f[2] < box[5] and part ~= 1) then
		return 1
	end
	return 0.45
end

MM.Update = function(self, event)
	local state = UIExpression.DvarString(nil, "mm_state")
	if state == nil then
		return
	end
	self.ticks = (self.ticks or 0) + 1
	if state ~= self.lastState then
		self.lastState = state
		-- average number of drawn frames between packets
		if self.ticks < 40 then
			self.tpp = (self.tpp or self.ticks) * 0.9 + self.ticks * 0.1
		end
		self.ticks = 0
		parse(self, state)
	end
	if not self.visible or not self.me then
		show(self, 0)
		return
	end
	show(self, 1)
	local t = math.min(1, (self.ticks + 1) / math.max(1, self.tpp or 1))
	local function glide(o)
		o.x = o.fx + (o.tx - o.fx) * t
		o.y = o.fy + (o.ty - o.fy) * t
	end
	local me = self.me
	glide(me)
	me.yaw = me.fyaw + (me.tyaw - me.fyaw) * t
	local px, py, yaw = me.x, me.y, me.yaw
	-- measured on video: positions reach the screen one frame after setZRot, so the
	-- pictures are turned with an older yaw (mm_giro 1: one frame, 3: two frames)
	local turnYaw = yaw
	if self.giro == 1 then
		turnYaw = me.yaw1 or yaw
	elseif self.giro == 3 then
		turnYaw = me.yaw2 or me.yaw1 or yaw
	end
	me.yaw2 = me.yaw1
	me.yaw1 = yaw
	local rad = yaw * 0.017453292519943
	local s, c = math.sin(rad), math.cos(rad)
	local crazy = px > 8000
	local range = MM.CrazyRange
	if not crazy then
		range = self.zoom or MM.Range
		-- closer inside a cave, with a short glide
		if self.part == 1 then
			range = math.min(range, MM.CryptRange)
		elseif MM.Under[self.part] then
			range = math.min(range, self.part <= 5 and MM.CaveRange or 1300)
		end
		self.range = (self.range or range) + (range - (self.range or range)) * 0.06
		if math.abs(self.range - range) < 2 then
			self.range = range
		end
		range = self.range
	end
	local scale = (MM.Size / 2) / range
	-- world -> minimap-local; screen y points down
	local function project(x, y)
		local dx, dy = x - px, y - py
		return (dx * s - dy * c) * scale, -(dx * c + dy * s) * scale
	end

	local smooth = 0
	local under = not crazy and MM.Under[self.part]
	local mapAlpha = 0.9
	if crazy then
		mapAlpha = 0
	elseif under then
		mapAlpha = 0.3
	end
	local spin = self.giro == 2
	local layer = self.layers[spin and 2 or 1]
	local other = self.layers[spin and 1 or 2]
	for i = 1, 3 do
		show(other[i], 0)
	end
	local a = crazy and 1 or (under and under[3]) or 0
	show(layer[1], mapAlpha)
	show(layer[2], a == 1 and 0.95 or 0)
	show(layer[3], a == 2 and 0.95 or 0)
	local rs = self.rotsign or 1
	local function lay(e, x, y, w)
		if spin then
			-- north-up offsets; the container, centred on the player, does the turning
			place(e, (x - px) * scale, (py - y) * scale, w * scale / 2, 0)
		else
			local cx, cy = project(x, y)
			place(e, cx, cy, w * scale / 2, 0)
			e:setZRot((90 - turnYaw) * rs)
		end
	end
	if spin then
		self.spin:setZRot((90 - turnYaw) * rs)
	end
	if crazy then
		lay(layer[2], MM.CrazyX, MM.CrazyY, MM.CrazyWorld)
	else
		lay(layer[1], MM.CenterX, MM.CenterY, MM.World)
		if under then
			lay(layer[1 + a], under[1], under[2], MM.UnderWorld)
		end
	end

	-- compass letters, sliding along the square border: N, E, S, O
	for i = 1, 4 do
		local nx, ny = -c, -s
		if i == 2 then
			nx, ny = s, -c
		elseif i == 3 then
			nx, ny = c, s
		elseif i == 4 then
			nx, ny = -s, c
		end
		local k = (MM.Size / 2 - 9) / math.max(math.abs(nx), math.abs(ny))
		place(self.compass[i], nx * k, ny * k, i == 1 and 8 or 7, 0)
	end

	local half = MM.Size / 2
	-- "x,y,h;" h: 0 same floor, 1 above, 2 below, 3 ally, 4 boss
	local zi, ai, bi = 0, 0, 0
	for id, o in pairs(self.ents) do
		glide(o)
		local e
		local h = o.h
		local ex, ey = project(o.x, o.y)
		if h == "3" then
			ai = ai + 1
			e = self.allies[ai]
			ex = math.max(-half + 6, math.min(half - 6, ex))
			ey = math.max(-half + 6, math.min(half - 6, ey))
		elseif math.abs(ex) < half + 6 and math.abs(ey) < half + 6 then
			if h == "4" then
				bi = bi + 1
				e = self.mech[bi]
			else
				zi = zi + 1
				e = self.zombies[zi]
			end
		end
		if e then
			place(e, ex, ey, 6, 0)
			show(e, 1)
			if e.arrow then
				e.arrow:setZRot(((o.yaw or yaw) - yaw) * (self.rotsign or 1))
				if e.id ~= id then
					e.id = id
					local ac = MM.AllyColor[(tonumber(id) or 0) % 4 + 1]
					e.arrow:setRGB(ac[1], ac[2], ac[3])
				end
			end
			if e.up and e.h ~= h then
				e.h = h
				e.up:setAlpha(h == "1" and 1 or 0)
				e.down:setAlpha(h == "2" and 1 or 0)
			end
		end
	end
	for i = zi + 1, MM.MaxZombies do
		show(self.zombies[i], 0)
	end
	for i = ai + 1, MM.MaxAllies do
		show(self.allies[i], 0)
	end
	for i = bi + 1, MM.MaxMech do
		show(self.mech[i], 0)
	end

	local fi = 0
	for i, o in pairs(self.footPos) do
		fi = fi + 1
		local e = self.feet[fi]
		if e then
			glide(o)
			local ex, ey = project(o.x, o.y)
			place(e, ex, ey, 11, 0)
			show(e, 1)
			show(e.danger, (o.a == "1" and (self.packet or 0) % 6 < 4) and 1 or 0)
		end
	end
	for i = fi + 1, 6 do
		show(self.feet[i], 0)
	end

	for i = 1, #MM.Fixed do
		local f = MM.Fixed[i]
		local e = self.fixed[i]
		local ex, ey = project(f[1], f[2])
		if not crazy and math.abs(ex) < half + 6 and math.abs(ey) < half + 6 then
			place(e, ex, ey, 7, 0)
			show(e, fixedAlpha(f, self.part))
		else
			show(e, 0)
		end
	end

	local pi = 0
	for k = 1, #self.poiList do
		local o = self.poiList[k]
		local kind = string.sub(o.t, 1, 1)
		local color = (kind == "B" or kind == "H") and MM.PoiColor[kind]
		local e = color and self.poi[pi + 1]
		local ex, ey = project(o.x, o.y)
		if kind == "H" then
			ex, ey = project(o.x + 105, o.y + 105)
		end
		if e and math.abs(ex) < half - 2 and math.abs(ey) < half - 2 then
			pi = pi + 1
			place(e, ex, ey, 7, 0)
			if e.t ~= o.t then
				e.t = o.t
				e.label:setText(kind == "H" and "" or o.t)
				e.box:setAlpha(kind == "H" and 0 or 1)
				e.cap:setAlpha(kind == "H" and 1 or 0)
				e.label:setRGB(color[1], color[2], color[3])
			end
			show(e, 1)
		end
	end
	for i = pi + 1, MM.MaxPoi do
		show(self.poi[i], 0)
	end
end

-- Full map, north up. Uses the positions MM.Update has already interpolated.
MM.UpdateBig = function(self)
	local big = self.big
	if not big then
		return
	end
	local open = self.visible and self.me and UIExpression.DvarString(nil, "mm_big") == "1"
	show(big, open and 1 or 0)
	if not open then
		return
	end
	local me = self.me
	local crazy = me.x > 8000
	local ox, oy, span = MM.CenterX, MM.CenterY, MM.World
	if crazy then
		ox, oy, span = 10464, -7788, 2700
	end
	local k = MM.BigSize / span
	local half = MM.BigSize / 2
	-- on a lower floor: dim the surface and light only that structure
	local part = not crazy and MM.Under[self.part] and self.part or 0
	show(big.map, (crazy and 0) or (part > 0 and 0.3) or 1)
	for i = 1, #big.caveBox do
		local a = 0
		if part > 0 then
			a = (i == part) and 1 or 0
		elseif i >= 2 and i <= 5 then
			a = 0.9
		end
		show(big.caveBox[i], a)
	end
	show(big.crazy, crazy and 1 or 0)
	show(big.labels, crazy and 0 or 1)
	show(big.caves, crazy and 0 or 1)
	for i = 1, #MM.Fixed do
		show(big.fixed[i], crazy and 0 or fixedAlpha(MM.Fixed[i], part))
	end
	local rs = self.rotsign or 1
	local function put(e, x, y, size)
		x, y = (x - ox) * k, (oy - y) * k
		if math.abs(x) > half or math.abs(y) > half then
			show(e, 0)
			return
		end
		place(e, x, y, size, 0)
		show(e, 1)
	end
	put(big.me, me.x, me.y, 8)
	big.me:setZRot((me.yaw - 90) * rs)
	local zi, ai, bi = 0, 0, 0
	for id, o in pairs(self.ents) do
		local e
		if o.h == "3" then
			ai = ai + 1
			e = big.allies[ai]
			if e then
				e:setZRot(((o.yaw or 90) - 90) * rs)
				local ac = MM.AllyColor[(tonumber(id) or 0) % 4 + 1]
				e:setRGB(ac[1], ac[2], ac[3])
			end
		elseif o.h == "4" then
			bi = bi + 1
			e = big.mech[bi]
		else
			zi = zi + 1
			e = big.zombies[zi]
		end
		if e then
			put(e, o.x, o.y, (o.h == "3" and 7) or (o.h == "4" and 9) or 3.4)
		end
	end
	for i = zi + 1, MM.MaxZombies do
		show(big.zombies[i], 0)
	end
	for i = ai + 1, MM.MaxAllies do
		show(big.allies[i], 0)
	end
	for i = bi + 1, MM.MaxMech do
		show(big.mech[i], 0)
	end
	local fi = 0
	for i, o in pairs(self.footPos) do
		fi = fi + 1
		local e = big.feet[fi]
		if e then
			put(e, o.x, o.y, 7)
			if o.a == "1" then
				e:setRGB(1, 0.12, 0.08)
			else
				e:setRGB(1, 0.8, 0.15)
			end
		end
	end
	for i = fi + 1, 6 do
		show(big.feet[i], 0)
	end
	-- captured generators and the box
	local ci, boxed = 0, false
	for i = 1, #self.poiList do
		local o = self.poiList[i]
		local kind = string.sub(o.t, 1, 1)
		if kind == "H" and big.caps[ci + 1] then
			ci = ci + 1
			put(big.caps[ci], o.x + 130, o.y + 130, 4)
		elseif kind == "B" then
			boxed = true
			put(big.box, o.x, o.y, 8)
		end
	end
	for i = ci + 1, 6 do
		show(big.caps[i], 0)
	end
	if not boxed then
		show(big.box, 0)
	end
end

MM.PlaceColor = {
	{ "CRIPTA", 0.3, 0.95, 0.8 }, { "CRAZY", 0.85, 0.65, 1 }, { "FUEGO", 1, 0.4, 0.25 }, { "HIELO", 0.4, 0.8, 1 }, { "VIENTO", 0.95, 0.9, 0.5 }, { "RAYO", 0.8, 0.5, 1 },
}
MM.UpdatePlace = function(self)
	local zone = UIExpression.DvarString(nil, "mm_zone")
	if zone == nil or zone == self.lastZone then
		return
	end
	self.lastZone = zone
	self.place:setText(zone)
	local r, g, b = 1, 0.95, 0.8
	for i = 1, #MM.PlaceColor do
		local p = MM.PlaceColor[i]
		if string.find(zone, p[1]) then
			r, g, b = p[2], p[3], p[4]
		end
	end
	self.place:setRGB(r, g, b)
end

MM.UpdateInfo = function(self)
	local info = UIExpression.DvarString(nil, "mm_info")
	if info == nil or info == self.lastInfo then
		return
	end
	self.lastInfo = info
	local n = {}
	for v in string.gmatch(info, "%-?%d+") do
		n[#n + 1] = tonumber(v)
	end
	if #n < 3 then
		return
	end
	local hp, maxhp = math.max(0, n[2]), math.max(1, n[3])
	local f = math.min(1, hp / maxhp)
	self.count:setText("ZOMBIS " .. n[1])
	self.life:setText("VIDA " .. hp)
	self.lifeBar:setLeftRight(false, false, 4, 4 + (MM.Size / 2 - 8) * f)
	if f > 0.6 then
		self.lifeBar:setRGB(0.3, 0.9, 0.4)
	elseif f > 0.3 then
		self.lifeBar:setRGB(1, 0.75, 0.2)
	else
		self.lifeBar:setRGB(1, 0.2, 0.2)
	end
end

MM.Attach = function(parent)
	local root = LUI.UIElement.new()
	root:setLeftRight(false, true, -MM.Size - 10, -10)
	root:setTopBottom(true, false, 10, 10 + MM.Size)
	root:setAlpha(0)
	parent:addElement(root)

	local clip = LUI.UIElement.new()
	clip:setLeftRight(true, true, 0, 0)
	clip:setTopBottom(true, true, 0, 0)
	clip:setUseStencil(true)
	root:addElement(clip)

	-- draw order = insertion order
	image(clip, "white", MM.Size, 0.03, 0.045, 0.06, 0.82)
	local function pictures(p)
		return {
			image(p, MM.Material, MM.World * (MM.Size / 2) / MM.Range, 1, 1, 1, 0),
			image(p, MM.CrazyMaterial, 100, 1, 1, 1, 0),
			image(p, MM.AtlasB, 100, 1, 1, 1, 0),
		}
	end
	root.spin = LUI.UIElement.new()
	root.spin:setLeftRight(false, false, -MM.Size / 2, MM.Size / 2)
	root.spin:setTopBottom(false, false, -MM.Size / 2, MM.Size / 2)
	clip:addElement(root.spin)
	root.layers = { pictures(clip), pictures(root.spin) }
	local function bar(parent, l, t, r, b, cr, cg, cb, a)
		local e = image(parent, "white", 2, cr, cg, cb, a)
		e:setLeftRight(false, false, l, r)
		e:setTopBottom(false, false, t, b)
		return e
	end
	local function group(parent, size, alpha)
		local e = LUI.UIElement.new()
		e:setLeftRight(false, false, -size, size)
		e:setTopBottom(false, false, -size, size)
		e:setAlpha(alpha)
		parent:addElement(e)
		return e
	end
	-- round dot with dark rim; the rim is part of the picture, so it stays dark when tinted
	local function dot(parent, r, cr, cg, cb)
		return image(parent, MM.DotMat, (r + 0.8) * 2, cr, cg, cb, 1)
	end
	local function oval(parent, l, t, r, b, cr, cg, cb)
		local e = image(parent, MM.DotMat, 2, cr, cg, cb, 1)
		e:setLeftRight(false, false, l, r)
		e:setTopBottom(false, false, t, b)
		return e
	end
	local function footprint(parent, k, cr, cg, cb)
		oval(parent, -4.5 * k, -9 * k, 4.5 * k, 3.5 * k, cr, cg, cb)
		oval(parent, -3.6 * k, 2.5 * k, 3.6 * k, 9 * k, cr, cg, cb)
	end
	local function text(parent, size, t)
		local e = LUI.UIText.new()
		e:setLeftRight(true, true, 0, 0)
		e:setTopBottom(true, false, t, t + size)
		e:setFont(CoD.fonts.Default)
		e:setAlignment(LUI.Alignment.Center)
		e:setText("")
		parent:addElement(e)
		return e
	end
	root.feet = {}
	for i = 1, 6 do
		local e = group(clip, 11, 0)
		footprint(e, 0.9, 1, 0.8, 0.15)
		e.danger = group(e, 11, 0)
		footprint(e.danger, 1.2, 1, 0.12, 0.08)
		root.feet[i] = e
	end
	local function fixedIcon(parent, kind, k)
		local e = group(parent, 7, 0)
		local mat = MM.PerkMat[kind]
		if mat then
			image(e, mat, 19 * k, 1, 1, 1, 1)
		elseif kind == "W" then
			-- own drawing for the random perk machine: a bottle with a question mark
			bar(e, -2.6 * k, -8 * k, 2.6 * k, -3 * k, 0, 0, 0, 1)
			oval(e, -6.4 * k, -5.2 * k, 6.4 * k, 8 * k, 0.62, 0.25, 0.95)
			bar(e, -1.8 * k, -7.2 * k, 1.8 * k, -3.4 * k, 0.62, 0.25, 0.95, 1)
			bar(e, -2.6 * k, -8.2 * k, 2.6 * k, -6.6 * k, 1, 0.85, 0.3, 1)
			local q = text(e, 9.5, 3.4)
			q:setText("?")
		else
			dot(e, 7.6 * k, 0.95, 0.95, 0.95)
			dot(e, 4.4 * k, 0.07, 0.09, 0.12)
			local q = text(e, 9, 2.5)
			q:setText(kind)
		end
		return e
	end
	root.fixed = {}
	for i = 1, #MM.Fixed do
		root.fixed[i] = fixedIcon(clip, MM.Fixed[i][3], 1)
	end
	root.poi = {}
	for i = 1, MM.MaxPoi do
		local e = group(clip, 7, 0)
		e.box = group(e, 7, 1)
		dot(e.box, 6, 0.08, 0.1, 0.13)
		e.cap = group(e, 7, 0)
		-- green square with a white tick: cannot be mistaken for a player
		bar(e.cap, -3.6, -3.6, 3.6, 3.6, 0, 0, 0, 1)
		bar(e.cap, -2.8, -2.8, 2.8, 2.8, 0.1, 0.65, 0.25, 1)
		local t1 = bar(e.cap, -2.1, 0, 0.1, 1, 1, 1, 1, 1)
		t1:setZRot(-45)
		local t2 = bar(e.cap, -1.4, -0.6, 2.6, 0.4, 1, 1, 1, 1)
		t2:setZRot(50)
		e.label = text(e, 11, 1)
		root.poi[i] = e
	end
	root.zombies, root.allies, root.mech = {}, {}, {}
	for i = 1, MM.MaxZombies do
		local e = group(clip, 6, 0)
		dot(e, 2.4, 1, 0.13, 0.1)
		e.up = group(e, 6, 0)
		local tri = image(e.up, MM.ArrowMat, 6, 1, 0.85, 0.2, 1)
		tri:setLeftRight(false, false, -3.2, 3.2)
		tri:setTopBottom(false, false, -8.4, -3.4)
		e.down = group(e, 6, 0)
		tri = image(e.down, MM.ArrowMat, 6, 0.4, 0.75, 1, 1)
		tri:setLeftRight(false, false, -3.2, 3.2)
		tri:setTopBottom(false, false, 3.4, 8.4)
		tri:setZRot(180)
		root.zombies[i] = e
	end
	for i = 1, MM.MaxMech do
		root.mech[i] = group(clip, 6, 0)
		image(root.mech[i], MM.PanzerMat, 16, 1, 1, 1, 1)
	end
	for i = 1, MM.MaxAllies do
		root.allies[i] = group(clip, 6, 0)
		root.allies[i].arrow = image(root.allies[i], MM.ArrowMat, 11, 0.25, 0.95, 0.4, 1)
	end
	-- you: smaller than before (was about 20 tall)
	image(clip, MM.ArrowMat, 13, 1, 1, 1, 1)
	local h = MM.Size / 2
	bar(root, -h - 2, -h - 2, h + 2, -h, 0.55, 0.75, 0.8, 0.9)
	bar(root, -h - 2, h, h + 2, h + 2, 0.55, 0.75, 0.8, 0.9)
	bar(root, -h - 2, -h, -h, h, 0.55, 0.75, 0.8, 0.9)
	bar(root, h, -h, h + 2, h, 0.55, 0.75, 0.8, 0.9)
	root.compass = {}
	local letters = { "N", "E", "S", "O" }
	for i = 1, 4 do
		local e = LUI.UIText.new()
		e:setFont(CoD.fonts.Default)
		e:setAlignment(LUI.Alignment.Center)
		e:setText(letters[i])
		if i == 1 then
			e:setRGB(1, 0.85, 0.3)
		else
			e:setRGB(1, 0.85, 0.3)
		end
		root:addElement(e)
		root.compass[i] = e
	end

	-- info panel under the map
	local panel = LUI.UIElement.new()
	panel:setLeftRight(true, true, 0, 0)
	panel:setTopBottom(false, true, 5, 31)
	root:addElement(panel)
	bar(panel, -h - 2, -13, h + 2, 13, 0.03, 0.05, 0.07, 0.7)
	bar(panel, -0.5, -10, 0.5, 10, 0.55, 0.75, 0.8, 0.6)
	local leftBox = LUI.UIElement.new()
	leftBox:setLeftRight(true, false, 0, h)
	leftBox:setTopBottom(true, true, 0, 0)
	panel:addElement(leftBox)
	local rightBox = LUI.UIElement.new()
	rightBox:setLeftRight(false, true, -h, 0)
	rightBox:setTopBottom(true, true, 0, 0)
	panel:addElement(rightBox)
	-- name of the place, always upright
	local placeBox = LUI.UIElement.new()
	placeBox:setLeftRight(true, true, 0, 0)
	placeBox:setTopBottom(false, true, 33, 51)
	root:addElement(placeBox)
	bar(placeBox, -h - 2, -9, h + 2, 9, 0.03, 0.05, 0.07, 0.7)
	root.place = text(placeBox, 14, 2)
	root.count = text(leftBox, 16, 5)
	root.count:setRGB(1, 0.35, 0.3)
	root.life = text(rightBox, 16, 2)
	bar(panel, 4, 7, h - 4, 10, 0.2, 0.2, 0.2, 0.9)
	root.lifeBar = bar(panel, 4, 7, h - 4, 10, 0.3, 0.9, 0.4, 1)

	-- full map: sibling of the minimap, so both keep their own transparency
	local big = group(parent, MM.BigSize / 2, 0)
	root.big = big
	bar(big, -900, -500, 900, 500, 0, 0, 0, 0.6)
	local frame = MM.BigSize / 2
	bar(big, -frame - 2, -frame - 2, frame + 2, frame + 2, 0.55, 0.75, 0.8, 0.9)
	bar(big, -frame, -frame, frame, frame, 0.03, 0.045, 0.06, 1)
	local view = group(big, frame, 1)
	view:setUseStencil(true)
	big.map = image(view, MM.Material, MM.BigSize, 1, 1, 1, 1)
	local ck = MM.BigSize / 2700
	big.crazy = image(view, MM.CrazyMaterial, MM.CrazyWorld * ck, 1, 1, 1, 0)
	place(big.crazy, (MM.CrazyX - 10464) * ck, (-7788 - MM.CrazyY) * ck, MM.CrazyWorld * ck / 2, 0)
	-- each cave: a small clip box showing only its own tile of the atlas
	big.caves = group(big, frame, 1)
	big.caveBox = {}
	local bk = MM.BigSize / MM.World
	for i = 1, #MM.BigCaves do
		local d = MM.BigCaves[i]
		local mx, my = (d[2] + d[3]) / 2, (d[4] + d[5]) / 2
		local box = group(big.caves, 10, 1)
		box:setLeftRight(false, false, (d[2] - MM.CenterX) * bk, (d[3] - MM.CenterX) * bk)
		box:setTopBottom(false, false, (MM.CenterY - d[5]) * bk, (MM.CenterY - d[4]) * bk)
		box:setUseStencil(true)
		local img = image(box, MM.Under[d[1]][3] == 2 and MM.AtlasB or MM.CrazyMaterial, MM.UnderWorld * bk, 1, 1, 1, 1)
		big.caveBox[i] = img
		local un = MM.Under[d[1]]
		place(img, (un[1] - mx) * bk, (my - un[2]) * bk, MM.UnderWorld * bk / 2, 0)
	end
	-- everything on top of the caves
	view = group(big, frame, 1)
	big.labels = group(view, frame, 1)
	for i = 1, #MM.BigLabels do
		local d = MM.BigLabels[i]
		local e = group(big.labels, 80, 1)
		local w = string.len(d[3]) * 2.7 + 4
		local lx = (d[1] - MM.CenterX) * MM.BigSize / MM.World
		place(e, lx, (MM.CenterY - d[2]) * MM.BigSize / MM.World, 80, 0)
		bar(e, -w, -7, w, 7, 0.02, 0.03, 0.04, 0.75)
		local t = text(e, 11, 74)
		t:setText(d[3])
		t:setRGB(d[4] or 1, d[5] or 0.95, d[6] or 0.8)
	end
	big.fixed = {}
	for i = 1, #MM.Fixed do
		local e = fixedIcon(view, MM.Fixed[i][3], 0.95)
		place(e, (MM.Fixed[i][1] - MM.CenterX) * MM.BigSize / MM.World, (MM.CenterY - MM.Fixed[i][2]) * MM.BigSize / MM.World, 7, 0)
		big.fixed[i] = e
	end
	big.feet, big.caps, big.zombies, big.mech, big.allies = {}, {}, {}, {}, {}
	for i = 1, 6 do
		big.feet[i] = image(view, MM.DotMat, 14, 1, 0.8, 0.15, 0)
		big.caps[i] = image(view, "white", 8, 0.15, 0.85, 0.3, 0)
	end
	big.box = group(view, 8, 0)
	dot(big.box, 6, 0.08, 0.1, 0.13)
	local bt = text(big.box, 11, 2)
	bt:setText("B")
	bt:setRGB(0.3, 0.85, 1)
	for i = 1, MM.MaxZombies do
		big.zombies[i] = image(view, MM.DotMat, 7, 1, 0.13, 0.1, 0)
	end
	for i = 1, MM.MaxMech do
		big.mech[i] = image(view, MM.PanzerMat, 18, 1, 1, 1, 0)
	end
	for i = 1, MM.MaxAllies do
		big.allies[i] = image(view, MM.ArrowMat, 14, 1, 1, 1, 0)
	end
	big.me = image(view, MM.ArrowMat, 16, 1, 1, 1, 0)
	local function side(l, x, y)
		local e = group(view, 10, 1)
		place(e, x, y, 10, 0)
		local t = text(e, 16, 2)
		t:setText(l)
		t:setRGB(1, 0.85, 0.3)
	end
	side("N", 0, -frame + 12)
	side("S", 0, frame - 12)
	side("E", frame - 12, 0)
	side("O", -frame + 12, 0)

	-- legend, left of the full map
	local lg = group(big, 10, 1)
	bar(lg, -628, -318, -334, 196, 0.03, 0.045, 0.06, 0.92)
	bar(lg, -628, -318, -334, -316, 0.55, 0.75, 0.8, 0.9)
	local function words(t, x, y, size, r, g, b)
		local e = LUI.UIText.new()
		e:setLeftRight(false, false, x, x + 250)
		e:setTopBottom(false, false, y - size / 2, y + size / 2)
		e:setFont(CoD.fonts.Default)
		e:setAlignment(LUI.Alignment.Left)
		e:setText(t)
		e:setRGB(r, g, b)
		lg:addElement(e)
	end
	words("SIGNIFICADO", -614, -301, 18, 1, 0.85, 0.3)
	local function ring(e, r, cr, cg, cb)
		dot(e, r + 0.8, cr, cg, cb)
		dot(e, r * 0.64, 0.07, 0.09, 0.12)
	end
	local function letter(e, l, cr, cg, cb)
		local q = text(e, 11, 1.5)
		q:setText(l)
		q:setRGB(cr, cg, cb)
	end
	local rows = {
		{ "Tu", function(e) image(e, MM.ArrowMat, 18, 1, 1, 1, 1) end },
		{ "Otro jugador (un color cada uno)", function(e) image(e, MM.ArrowMat, 16, 1, 0.85, 0.2, 1) end },
		{ "Zombi", function(e) dot(e, 3.5, 1, 0.13, 0.1) end },
		{ "Panzer Soldat", function(e) image(e, MM.PanzerMat, 20, 1, 1, 1, 1) end },
		{ "Zona donde pisa un robot", function(e)
			ring(e, 7.5, 1, 0.65, 0.15)
			bar(e, -3.4, -3, -0.8, 3, 1, 0.68, 0.23, 1)
			bar(e, 0.8, -3, 3.4, 3, 1, 0.68, 0.23, 1)
		end },
		{ "Pie de robot", function(e) dot(e, 6, 1, 0.8, 0.15) end },
		{ "Pie bajando: sal de ahi", function(e) dot(e, 6, 1, 0.12, 0.08) end },
		{ "Generador", function(e) ring(e, 7, 0.95, 0.95, 0.95) letter(e, "G", 1, 1, 1) end },
		{ "Generador capturado", function(e)
			bar(e, -5, -5, 5, 5, 0, 0, 0, 1)
			bar(e, -4, -4, 4, 4, 0.15, 0.85, 0.3, 1)
		end },
		{ "Caja misteriosa", function(e) dot(e, 7, 0.08, 0.1, 0.13) letter(e, "B", 0.3, 0.85, 1) end },
		{ "Pack-a-Punch", function(e) ring(e, 7, 1, 0.5, 0.9) letter(e, "P", 1, 0.5, 0.9) end },
		{ "Wunderfizz (ventaja al azar)", "W" },
		{ "Juggernog", "J" },
		{ "Quick Revive", "R" },
		{ "Speed Cola", "S" },
		{ "Stamin-Up", "M" },
		{ "Mule Kick (en la cripta)", "K" },
		{ "Baston (cripta y Crazy Place)", function(e)
			ring(e, 7.5, 0.35, 0.78, 1)
			local st = bar(e, -0.8, -4.5, 0.8, 4.5, 0.92, 0.88, 0.8, 1)
			st:setZRot(-45)
			oval(e, 1, -5, 4.6, -1.4, 0.35, 0.78, 1)
		end },
		{ "Portal (Crazy Place)", function(e)
			dot(e, 7.5, 0.76, 0.45, 1)
			dot(e, 4, 0.07, 0.09, 0.12)
			dot(e, 2.4, 0.76, 0.45, 1)
		end },
	}
	for i = 1, #rows do
		local y = -273 + (i - 1) * 25
		local e
		if type(rows[i][2]) == "string" then
			e = fixedIcon(lg, rows[i][2], 1)
			e:setAlpha(1)
		else
			e = group(lg, 7, 1)
			rows[i][2](e)
		end
		place(e, -604, y, 7, 0)
		words(rows[i][1], -584, y, 14, 0.92, 0.94, 0.95)
	end

	root:registerEventHandler("mm_tick", MM.Update)
	root:addElement(LUI.UITimer.new(1, "mm_tick", false, root))
end

local function diag(msg)
	if Engine and Engine.SetDvar then
		Engine.SetDvar("mm_diag", msg)
	end
end

local function safe(label, fn, ...)
	if not pcall then
		return fn(...)
	end
	local ok, err = pcall(fn, ...)
	if not ok then
		diag(label .. ": " .. tostring(err))
	end
end

local rawUpdate = MM.Update
MM.Update = function(self, event)
	if not self.diagTick then
		self.diagTick = true
		diag("tick")
	end
	safe("update", rawUpdate, self, event)
	safe("info", MM.UpdateInfo, self)
	safe("place", MM.UpdatePlace, self)
	safe("big", MM.UpdateBig, self)
end

-- The BO3 HUD clears hud_visible, which hides the perk area. Keep the minimap as a
-- sibling of that area (inside a plain container) so it is not hidden with it.
local vanillaPerksArea = LUI.createMenu.PerksArea
if vanillaPerksArea then
	diag("hooked")
	LUI.createMenu.PerksArea = function(controller)
		local perks = vanillaPerksArea(controller)
		diag("created map=" .. tostring(UIExpression.DvarString(nil, "mapname")) .. " ui=" .. tostring(UIExpression.DvarString(nil, "ui_mapname")))
		if UIExpression.DvarString(nil, "mapname") ~= "zm_tomb" and UIExpression.DvarString(nil, "ui_mapname") ~= "zm_tomb" then
			return perks
		end
		local box = LUI.UIElement.new()
		box:setLeftRight(true, true, 0, 0)
		box:setTopBottom(true, true, 0, 0)
		box:addElement(perks)
		safe("attach", MM.Attach, box)
		return box
	end
else
	diag("PerksArea missing")
end
