"""v21: generator states (capturing, yours, in danger, attacked) and footprints that point where the robot walks"""
import sys,io,os,re,struct,shutil
S,T=sys.argv[1:3];go=len(sys.argv)>3;M=T+'/mods/zm_minimapa';Q=S+'/mm/';G=os.path.dirname(os.path.abspath(__file__))+'/'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image,ImageDraw
ns={'__name__':'arte'};exec(compile(open(G+'arte.py',encoding='utf8').read(),'arte','exec'),ns)
# ---- printed stomp zones, toe towards the east
src=open(Q+'v11.py',encoding='utf8').read().split('icons(base,items,tr); base.save')[0].replace("Image.open(Q+'surf11.png')","Image.open(SURF)")
SURF=G+'surf17.png';ar=sys.argv;sys.argv=['x',S,T,M];exec(src);sys.argv=ar
ft=ns['ICONS']['foot']();ft.c=ft.c*np.array([1,.66,.2],np.float32);sole=ft.out(256).rotate(-90).resize((24,24),Image.LANCZOS)
ring=Image.new('RGBA',(256,256),(0,0,0,0));ImageDraw.Draw(ring).ellipse((10,10,246,246),fill=(255,150,30,60),outline=(255,170,50,235),width=16);ring=ring.resize((30,30),Image.LANCZOS)
for x,y in feet:
    X,Y=tr(x,y);base.alpha_composite(ring,(int(round(X-15)),int(round(Y-15))));base.alpha_composite(sole,(int(round(X-12)),int(round(Y-12))))
base.save(G+'base21.png')
with open(M+'/images/icon_twitter.iwi','rb') as fh:h=fh.read(64)
b=io.BytesIO();base.save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5' and struct.unpack_from('<HH',h,6)==(1024,1024)
tw=h+d[128:128+1024*1024]
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc'
s=open(lp,newline='').read();g=open(gp,newline='').read()
def R(a,c,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a);s=s.replace(a,c)
def RG(a,c,n=1):
    global g
    assert g.count(a)==n,(g.count(a),a);g=g.replace(a,c)
# ================= GSC
RG('\tlevel thread mml_zone();\n','\tlevel thread mml_zone();\n\tlevel thread mml_gens();\n')
RG('\tsetdvar( "mm_zone", "" );\n','\tsetdvar( "mm_zone", "" );\n\tsetdvar( "mm_gen", "" );\n')
for side in('LE','RI'):
    RG('list = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_%s" ), mml_foot( robot, "TAG_ATTACH_HATCH_%s" ) );'%(side,side),'list = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_%s" ), mml_foot( robot, "TAG_ATTACH_HATCH_%s" ) + "," + heading );'%(side,side))
RG('list = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_LE" )','heading = mml_heading( robot );\n\t\t\t\tlist = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_LE" )')
g=g.rstrip()+'''

// yaw the robot walks towards, from the real movement of both feet; east until it has moved
mml_heading( robot )
{
	a = robot gettagorigin( "TAG_ATTACH_HATCH_LE" );
	b = robot gettagorigin( "TAG_ATTACH_HATCH_RI" );
	mid = ( a + b ) * 0.5;
	if ( !isdefined( robot.mml_mid ) || distance2d( mid, robot.mml_mid ) > 1500 )
	{
		robot.mml_mid = mid;
		robot.mml_yaw = 0;
	}
	if ( distance2d( mid, robot.mml_mid ) > 150 )
	{
		ang = vectortoangles( mid - robot.mml_mid );
		robot.mml_yaw = int( ang[ 1 ] );
		robot.mml_mid = mid;
	}
	return robot.mml_yaw;
}

mml_flag( zone, name )
{
	return isdefined( zone.ent_flag ) && isdefined( zone.ent_flag[ name ] ) && zone.ent_flag[ name ];
}

// "number,state,progress;" 0 free, 1 being captured, 2 yours, 3 zombies on their way, 4 under attack
mml_gens()
{
	level endon( "end_game" );
	for ( ;; )
	{
		wait 0.25;
		if ( !isdefined( level.zone_capture ) || !isdefined( level.zone_capture.zones ) )
			continue;
		list = "";
		foreach ( zone in level.zone_capture.zones )
		{
			n = mml_gen_number( zone.script_noteworthy );
			if ( n == 0 )
				continue;
			state = 0;
			if ( mml_flag( zone, "attacked_by_recapture_zombies" ) )
				state = 4;
			else if ( mml_flag( zone, "current_recapture_target_zone" ) && mml_flag( zone, "player_controlled" ) )
				state = 3;
			else if ( mml_flag( zone, "player_controlled" ) )
				state = 2;
			else if ( mml_flag( zone, "zone_contested" ) )
				state = 1;
			progress = 0;
			if ( isdefined( zone.n_current_progress ) )
				progress = int( zone.n_current_progress );
			list = list + n + "," + state + "," + progress + ";";
		}
		setdvar( "mm_gen", list );
	}
}

mml_gen_number( name )
{
	if ( !isdefined( name ) )
		return 0;
	switch ( name )
	{
		case "generator_start_bunker":
			return 1;
		case "generator_tank_trench":
			return 2;
		case "generator_mid_trench":
			return 3;
		case "generator_nml_right":
			return 4;
		case "generator_nml_left":
			return 5;
		case "generator_church":
			return 6;
	}
	return 0;
}
'''
# ================= Lua: feet
R('for ex, ey, a in string.gmatch(feet, "(%-?%d+),(%-?%d+),(%d)") do','for ex, ey, a, fy in string.gmatch(feet, "(%-?%d+),(%-?%d+),(%d),(%-?%d+)") do')
R('follow(self.footPos, fi, tonumber(ex), tonumber(ey), self.packet).a = a','local fo = follow(self.footPos, fi, tonumber(ex), tonumber(ey), self.packet)\n\t\t\tfo.a = a\n\t\t\tfo.yaw = tonumber(fy)')
R('\t\tfootprint(e, 0.9, 1, 0.8, 0.15)\n','\t\te.sole = footprint(e, 0.9, 1, 0.8, 0.15)\n')
R('\t\tfootprint(e.danger, 1.2, 1, 0.12, 0.08)\n','\t\te.redSole = footprint(e.danger, 1.2, 1, 0.12, 0.08)\n')
R('\t\timage(parent, MM.FootMat, 21 * k, cr, cg, cb, 1)\n','\t\treturn image(parent, MM.FootMat, 21 * k, cr, cg, cb, 1)\n')
R('\t\t\tshow(e.danger, (o.a','\t\t\tlocal footRot = ((o.yaw or 0) - yaw) * (self.rotsign or 1)\n\t\t\te.sole:setZRot(footRot)\n\t\t\te.redSole:setZRot(footRot)\n\t\t\tshow(e.danger, (o.a')
R('\t\t\tput(e, o.x, o.y, 9)\n','\t\t\tput(e, o.x, o.y, 9)\n\t\t\te:setZRot(((o.yaw or 0) - 90) * rs)\n')
# ================= Lua: generators
R('\t-- these change rarely\n','''	if self.packet % 5 == 1 then
		local gens = UIExpression.DvarString(nil, "mm_gen")
		self.gens = self.gens or {}
		self.alert, self.alertState = nil, 0
		if gens then
			for n, st, pr in string.gmatch(gens, "(%d),(%d),(%d+)") do
				st = tonumber(st)
				self.gens["G" .. n] = { st = st, pr = pr }
				if st >= 3 and st > self.alertState then
					self.alertState = st
					self.alert = "G" .. n
				end
			end
		end
	end
	-- these change rarely
''')
R('local function fixedAlpha(f, part)\n','''-- colour, text and mark of a generator badge
local function dressGen(e, f, gens, packet)
	local o = gens and gens[f[3]]
	local st = o and o.st or 0
	local blink = (packet or 0) % 10 < 5
	local key = st .. (st == 1 and o.pr or "") .. ((st == 1 or st == 4) and blink and "b" or "")
	if e.genKey == key then
		return st
	end
	e.genKey = key
	local r, g, b = 1, 1, 1
	if st == 1 then
		r, g, b = 1, 0.85, 0.15
		if blink then
			r, g, b = 1, 0.95, 0.6
		end
	elseif st == 2 then
		r, g, b = 0.25, 1, 0.4
	elseif st == 3 then
		r, g, b = 1, 0.55, 0.05
	elseif st == 4 then
		r, g, b = 1, 0.1, 0.05
		if blink then
			r, g, b = 1, 0.65, 0.6
		end
	end
	e.gen:setRGB(r, g, b)
	e.genText:setText(st == 1 and (o.pr .. "%") or f[3])
	e.genTick:setAlpha(st == 2 and 1 or 0)
	e.genBang:setAlpha(st >= 3 and 1 or 0)
	return st
end

local function fixedAlpha(f, part)
''')
R('''		local ex, ey = project(f[1], f[2])
		if not crazy and math.abs(ex)''','''		local ex, ey = project(f[1], f[2])
		local st = e.gen and dressGen(e, f, self.gens, self.packet) or 0
		if st >= 3 and not crazy then
			-- in danger: stays on the border to show the way
			ex = math.max(-half + 11, math.min(half - 11, ex))
			ey = math.max(-half + 11, math.min(half - 11, ey))
		end
		if not crazy and math.abs(ex)''')
R('\t\t\tshow(e, fixedAlpha(f, self.part))\n','\t\t\tshow(e, st >= 3 and 1 or fixedAlpha(f, self.part))\n')
R('show(big.fixed[i], crazy and 0 or fixedAlpha(MM.Fixed[i], part))','''local st = big.fixed[i].gen and dressGen(big.fixed[i], MM.Fixed[i], self.gens, self.packet) or 0
		show(big.fixed[i], crazy and 0 or (st >= 3 and 1) or fixedAlpha(MM.Fixed[i], part))''')
R('''			image(e, MM.GenMat, 20 * k, 1, 1, 1, 1)
			local q = text(e, 10, 2)
			q:setText(kind)
''','''			e.gen = image(e, MM.GenMat, 20 * k, 1, 1, 1, 1)
			e.genText = text(e, 10, 2)
			e.genText:setText(kind)
			e.genTick = group(e, 7, 0)
			local tk = image(e.genTick, MM.TickMat, 10, 1, 1, 1, 1)
			place(tk, 8, -7, 5, 0)
			e.genBang = group(e, 7, 0)
			local bg = image(e.genBang, MM.PanzerMat, 13, 1, 0.75, 0.7, 1)
			place(bg, 8, -8, 6.5, 0)
''')
# the old captured mark came with the live list
R('local color = (kind == "B" or kind == "H") and MM.PoiColor[kind]','local color = kind == "B" and MM.PoiColor[kind]')
R('if kind == "H" and big.caps[ci + 1] then','if false then')
# alert line
R('''	if zone == nil or zone == self.lastZone then
		return
	end
	self.lastZone = zone
''','''	if zone == nil then
		return
	end
	local blink = (self.packet or 0) % 10 < 5
	if self.alert then
		zone = (self.alertState == 4 and "ATACAN " or "ZOMBIS HACIA ") .. self.alert
	end
	local key = zone .. (self.alert and blink and "*" or "")
	if key == self.lastZone then
		return
	end
	self.lastZone = key
''')
R('\tself.place:setRGB(r, g, b)\n','''	if self.alert then
		r, g, b = 1, 0.55, 0.1
		if self.alertState == 4 then
			r, g, b = 1, blink and 0.2 or 0.55, blink and 0.15 or 0.5
		end
	end
	self.place:setRGB(r, g, b)
''')
# legend
R('''		{ "Generador", pic(MM.GenMat, 20) },
		{ "Generador capturado", pic(MM.TickMat, 18) },
''','''		{ "Generador libre", pic(MM.GenMat, 19) },
		{ "Generador: capturandolo", pic(MM.GenMat, 19, 1, 0.85, 0.15) },
		{ "Generador tuyo", pic(MM.GenMat, 19, 0.25, 1, 0.4) },
		{ "Generador: zombis hacia el", pic(MM.GenMat, 19, 1, 0.55, 0.05) },
		{ "Generador ATACADO", pic(MM.GenMat, 19, 1, 0.1, 0.05) },
''')
R('local y = -273 + (i - 1) * 25','local y = -277 + (i - 1) * 21.8')
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x,y=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',x,y);assert x==y
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1]) and g.count(q[0])==g.count(q[1]),q
i=g.index('mml_feet()\n{');print(g[i:g.index('// 1 = this foot',i)])
if go:
    b_=T+'/respaldo_hud/zm_minimapa_v20b';assert not os.path.exists(b_);shutil.copytree(M,b_)
    for p in(M,T):
        with open(p+'/images/icon_twitter.iwi','wb') as fh:fh.write(tw)
    for p,v in((lp,s),(gp,g)):
        with open(p,'w',newline='') as fh:fh.write(v)
    print('instalado')
