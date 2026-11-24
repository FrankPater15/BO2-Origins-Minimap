import sys,re,os,shutil
T=sys.argv[1];M=T+'/mods/zm_minimapa'
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
bp=T+'/players/mods/zm_minimapa/bindings_zm.bdg'
g=open(gp,newline='').read();s=open(lp,newline='').read();b=open(bp,newline='').read()
def rep(t,a,c):
    assert t.count(a)==1,(t.count(a),a);return t.replace(a,c)
# ---- GSC
g=rep(g,'\tsetdvar( "mm_zone", "" );\n','\tsetdvar( "mm_zone", "" );\n\tsetdvar( "mm_big", "0" ); // full map, key M\n')
g=rep(g,'\tlevel waittill( "end_game" );\n','\tlevel waittill( "end_game" );\n\tsetdvar( "mm_big", "0" );\n')
g=rep(g,'\tcount = 0;\n\tteam = "axis";','\tcount = 0;\n\tbig = getdvarint( "mm_big" );\n\tteam = "axis";')
g=rep(g,'if ( dx * dx + dy * dy > 12500000 )','if ( big != 1 && dx * dx + dy * dy > 12500000 )')
# ---- Lua
s=rep(s,'MM.UnderWorld = 20000\n','''MM.UnderWorld = 20000
MM.BigSize = 640
MM.BigLabels = {
	{ 1700, 5600, "LABORATORIO" }, { 0, 5080, "ESTACION DEL TANQUE" }, { -380, 3200, "BUNKER DEL TANQUE - G2" },
	{ 400, 1780, "TRINCHERA CENTRAL - G3" }, { 2450, 2250, "TRINCHERAS" }, { -1050, 1300, "TIERRA DE NADIE" },
	{ 1550, 250, "TIERRA DE NADIE" }, { 0, -370, "MID - EXCAVACION" }, { 3050, -620, "ZONA DE JUGGERNOG - G4" },
	{ -2700, 1050, "GRANJA - G5" }, { -1900, -2000, "ALDEA" }, { -1100, -3350, "ESTACION DEL TANQUE" },
	{ 600, -2500, "IGLESIA" }, { 2450, -3800, "DETRAS DE LA IGLESIA - G6" },
	{ 3850, 4450, "CUEVA DE FUEGO", 1, 0.4, 0.25 }, { 3350, 1750, "CUEVA DE VIENTO", 0.95, 0.9, 0.5 },
	{ -3500, -850, "CUEVA DE RAYO", 0.8, 0.5, 1 }, { 2500, -1850, "CUEVA DE HIELO", 0.4, 0.8, 1 },
}
''')
# update function, inserted before the info panel one
s=rep(s,'MM.PlaceColor = {\n','''-- Full map, north up. Uses the positions MM.Update has already interpolated.
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
	show(big.map, crazy and 0 or 1)
	show(big.crazy, crazy and 1 or 0)
	show(big.labels, crazy and 0 or 1)
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
''')
s=rep(s,'\troot:registerEventHandler("mm_tick", MM.Update)','''	-- full map: sibling of the minimap, so both keep their own transparency
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

	root:registerEventHandler("mm_tick", MM.Update)''')
s=rep(s,'\tsafe("place", MM.UpdatePlace, self)\n','\tsafe("place", MM.UpdatePlace, self)\n\tsafe("big", MM.UpdateBig, self)\n')
t=re.sub('--.*','',re.sub('"[^"]*"','',s))
o,e=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',o,e);assert o==e
for x in('()','{}','[]'):
    assert t.count(x[0])==t.count(x[1]) and g.count(x[0])==g.count(x[1]),x
assert not re.search(r'^bind2? M ',b,re.M)
nl='\r\n' if '\r\n' in b else '\n'
b=rep(b,nl+'bind Q ',nl+'bind M "toggle mm_big 0 1"'+nl+'bind Q ')
R=T+'/respaldo_hud/zm_minimapa_v12';assert not os.path.exists(R);shutil.copytree(M,R)
shutil.copy2(bp,T+'/respaldo_hud/bindings_zm_mod_antes_v13.bdg')
for p,x in((gp,g),(lp,s),(bp,b)):
    with open(p,'w',newline='') as fh: fh.write(x)
print('instalado')
