import sys,io,re,json,struct,shutil,os
S,T=sys.argv[1:3];M=T+'/mods/zm_minimapa';Q=S+'/mm/'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np
from PIL import Image,ImageDraw
DOC=__import__('os').environ['MM_DOCS']+'/'
# ---------- icons
Z=1024
def blank():
    i=Image.new('RGBA',(Z,Z),(0,0,0,0));return i,ImageDraw.Draw(i)
def ell(d,x,y,rx,ry,c):d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=c)
dot,d=blank();ell(d,512,512,490,490,(0,0,0,255));ell(d,512,512,370,370,(255,255,255,255))
arrow,d=blank()
def poly(g,c):
    p=[(512,70),(890,930),(512,730),(134,930)]
    d.polygon(p,fill=c)
    if g:
        d.line(p+p[:2],fill=c,width=g,joint='curve')
        for x,y in p: ell(d,x,y,g/2,g/2,c)
poly(120,(0,0,0,255));poly(0,(255,255,255,255))
pz,d=blank()
d.rounded_rectangle((60,60,964,964),230,fill=(0,0,0,255));d.rounded_rectangle((105,105,919,919),190,fill=(225,35,25,255));d.rounded_rectangle((175,175,849,849),140,fill=(25,25,28,255))
d.pieslice((250,230,774,800),180,360,fill=(255,150,40,255));d.rectangle((250,512,774,600),fill=(255,150,40,255))
d.rounded_rectangle((320,600,704,790),50,fill=(255,150,40,255));d.rounded_rectangle((300,440,724,560),50,fill=(15,15,18,255))
ell(d,410,500,48,48,(255,60,40,255));ell(d,614,500,48,48,(255,60,40,255))
for x in(400,490,580):d.rectangle((x,650,x+34,750),fill=(15,15,18,255))
ic={}
hdr=open(T+'/images/grenadeicon.iwi','rb').read()
assert len(hdr)==4160 and struct.unpack_from('<HH',hdr,6)==(64,64)
b5=open(M+'/images/hud_zombierank_5.iwi','rb').read(64);assert hdr[4]==b5[4],(hdr[:16],b5[:16])
def dxt(im,h):
    n=im.size[0];b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5');x=b.getvalue();assert x[84:88]==b'DXT5'
    return h[:64]+x[128:128+n*n]
for n,i in(('hud_zombierank_3_ded',dot),('hud_zombierank_4_ded',arrow),('hud_zombierank_5_ded',pz)):
    s=i.resize((64,64),Image.BOX)
    a=np.array(s);
    # keep white under transparent pixels black: no light halo
    ic[n]=dxt(s,hdr);s.save(DOC+n+'.png')
# ---------- caves with their own colour (tiles 3..6)
A=np.array(Image.open(Q+'atlas11.png').convert('RGBA'))
for i,c in {2:(190,110,255),3:(235,225,120),4:(90,200,255),5:(255,90,50)}.items():
    cx,cy=round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3)
    v=A[cy-160:cy+160,cx-160:cx+160];assert (v[...,3]>0).sum()>500,i
    lum=np.clip(v[...,:3].mean(2,keepdims=True)/110.,.5,1.15)
    v[...,:3]=np.clip(np.array(c)*lum,0,255).astype(np.uint8)
ic['hud_zombierank_5']=dxt(Image.fromarray(A),b5)
# ---------- zone names
def name(z):
    for r,n in((r'ug_bottom','CRIPTA'),(r'zone_air_st','CUEVA DE VIENTO'),(r'zone_bolt_st','CUEVA DE RAYO'),(r'zone_fire_st','CUEVA DE FUEGO'),(r'zone_ice_st','CUEVA DE HIELO'),
      (r'zone_chamber','CRAZY PLACE'),(r'zone_start','LABORATORIO'),(r'zone_bunker_tank','CAMINO DEL TANQUE'),(r'zone_bunker_4e','ESTACION DEL TANQUE'),(r'zone_bunker_4','BUNKER DEL TANQUE - G2'),
      (r'zone_bunker_3','TRINCHERA CENTRAL - G3'),(r'zone_bunker','TRINCHERAS'),(r'zone_nml_celllar','SOTANO DE LA GRANJA'),(r'zone_nml_farm','GRANJA - G5'),(r'zone_nml_1[89]$','MID - EXCAVACION'),
      (r'zone_nml_1(1|1a|2|2a)$','ZONA DE JUGGERNOG - G4'),(r'zone_nml','TIERRA DE NADIE'),(r'zone_village_2','IGLESIA'),(r'zone_village_1$','IGLESIA - ABAJO'),(r'zone_village_1a','ESTACION DEL TANQUE'),
      (r'zone_village_3','DETRAS DE LA IGLESIA - G6'),(r'zone_village','ALDEA')):
        if re.match(r,z):return n
vols=sorted({e['targetname'] for e in json.load(open(Q+'ents.json')) if e.get('script_noteworthy')=='player_volume' and 'targetname' in e})
zn={v:name(v) for v in vols if name(v)};print(len(vols),'sin nombre:',[v for v in vols if v not in zn])
# ---------- GSC
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
g=open(gp,newline='').read();s=open(lp,newline='').read()
def rep(t,a,b):
    assert t.count(a)==1,(t.count(a),a);return t.replace(a,b)
g=rep(g,'\tprecacheshader( "zombies_rank_5" );\n','\tprecacheshader( "zombies_rank_5" );\n\tprecacheshader( "zombies_rank_3_ded" );\n\tprecacheshader( "zombies_rank_4_ded" );\n\tprecacheshader( "zombies_rank_5_ded" );\n\tsetdvar( "mm_zone", "" );\n\tsetdvar( "mm_ay", "" );\n')
g=rep(g,'\tlevel thread mml_feet();\n','\tlevel thread mml_feet();\n\tlevel thread mml_zone();\n')
g=rep(g,'\tforeach ( player in players )\n\t{\n\t\tif ( player == me','\tyaws = "";\n\tforeach ( player in players )\n\t{\n\t\tif ( player == me')
g=rep(g,'",3," + player getentitynumber() + ";";\n','",3," + player getentitynumber() + ";";\n\t\tpa = player getplayerangles();\n\t\tyaws = yaws + player getentitynumber() + "," + int( pa[ 1 ] ) + ";";\n')
g=rep(g,'\t\tsetdvar( "mm_e" + k, out[ k ] );\n}','\t\tsetdvar( "mm_e" + k, out[ k ] );\n\tsetdvar( "mm_ay", yaws );\n}')
g=g.rstrip()+'''

// name of the place the host is in, from the zone volumes of the map
mml_zone()
{
	level endon( "end_game" );
	mml_zone_names();
	wait 1;
	vols = getentarray( "player_volume", "script_noteworthy" );
	last = undefined;
	for ( ;; )
	{
		wait 0.3;
		players = get_players();
		if ( players.size == 0 || !isdefined( players[ 0 ] ) )
			continue;
		me = players[ 0 ];
		if ( isdefined( last ) && me istouching( last ) )
			continue;
		last = undefined;
		for ( i = 0; i < vols.size; i++ )
		{
			vol = vols[ i ];
			if ( !isdefined( vol ) || !isdefined( vol.targetname ) || !isdefined( level.mml_names[ vol.targetname ] ) )
				continue;
			if ( me istouching( vol ) )
			{
				last = vol;
				setdvar( "mm_zone", level.mml_names[ vol.targetname ] );
				break;
			}
		}
	}
}

mml_zone_names()
{
	level.mml_names = [];
'''+''.join('\tlevel.mml_names[ "%s" ] = "%s";\n'%k for k in zn.items())+'}\n'
# ---------- Lua
s=rep(s,'MM.UnderWorld = 20000\n','''MM.UnderWorld = 20000
MM.DotMat = "zombies_rank_3_ded"
MM.ArrowMat = "zombies_rank_4_ded"
MM.PanzerMat = "zombies_rank_5_ded"
-- one colour per player number
MM.AllyColor = {
	{ 0.25, 0.65, 1 }, { 1, 0.85, 0.2 }, { 0.25, 0.95, 0.4 }, { 1, 0.45, 0.85 },
}
''')
s=rep(s,'\tfor id, o in pairs(self.ents) do\n\t\tif o.seq','''	local yaws = UIExpression.DvarString(nil, "mm_ay")
	if yaws then
		for id, a in string.gmatch(yaws, "(%d+),(%-?%d+)") do
			if self.ents[id] then
				self.ents[id].yaw = tonumber(a)
			end
		end
	end
	for id, o in pairs(self.ents) do
		if o.seq''')
s=rep(s,'\t\t\t\te = self.mech[bi]\n','\t\t\t\te = self.mech[bi]\n')
s=rep(s,'\t\t\tif e.up and e.h ~= h then','''			if e.arrow then
				e.arrow:setZRot(((o.yaw or yaw) - yaw) * (self.rotsign or 1))
				if e.id ~= id then
					e.id = id
					local ac = MM.AllyColor[(tonumber(id) or 0) % 4 + 1]
					e.arrow:setRGB(ac[1], ac[2], ac[3])
				end
			end
			if e.up and e.h ~= h then''')
s=rep(s,'show(e.danger, o.a == "1" and 1 or 0)','show(e.danger, (o.a == "1" and (self.packet or 0) % 6 < 4) and 1 or 0)')
i=s.index('\t-- octagonal dot');j=s.index('\tlocal function text(parent')
s=s[:i]+'''	-- round dot with dark rim; the rim is part of the picture, so it stays dark when tinted
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
'''+s[j:]
s=rep(s,'\t\tdot(e, 7, 1, 0.75, 0.1)\n','\t\tfootprint(e, 0.9, 1, 0.8, 0.15)\n')
s=rep(s,'\t\tdot(e.danger, 10, 1, 0.1, 0.05)\n','\t\tfootprint(e.danger, 1.2, 1, 0.12, 0.08)\n')
s=rep(s,'\t\tdot(e.cap, 3.2, 0.25, 1, 0.35)\n','''		-- green square with a white tick: cannot be mistaken for a player
		bar(e.cap, -3.6, -3.6, 3.6, 3.6, 0, 0, 0, 1)
		bar(e.cap, -2.8, -2.8, 2.8, 2.8, 0.1, 0.65, 0.25, 1)
		local t1 = bar(e.cap, -2.1, 0, 0.1, 1, 1, 1, 1, 1)
		t1:setZRot(-45)
		local t2 = bar(e.cap, -1.4, -0.6, 2.6, 0.4, 1, 1, 1, 1)
		t2:setZRot(50)
''')
s=rep(s,'\t\tdot(e, 2.8, 1, 0.13, 0.1)\n','\t\tdot(e, 2.4, 1, 0.13, 0.1)\n')
i=s.index('\t\tbar(e.up, -0.7');j=s.index('\t\troot.zombies[i] = e')
s=s[:i]+'''		local tri = image(e.up, MM.ArrowMat, 6, 1, 0.85, 0.2, 1)
		tri:setLeftRight(false, false, -3.2, 3.2)
		tri:setTopBottom(false, false, -8.4, -3.4)
		e.down = group(e, 6, 0)
		tri = image(e.down, MM.ArrowMat, 6, 0.4, 0.75, 1, 1)
		tri:setLeftRight(false, false, -3.2, 3.2)
		tri:setTopBottom(false, false, 3.4, 8.4)
		tri:setZRot(180)
'''+s[j:]
s=rep(s,'\t\tdot(root.mech[i], 5, 1, 0.5, 0.05)\n','\t\timage(root.mech[i], MM.PanzerMat, 16, 1, 1, 1, 1)\n')
s=rep(s,'\t\tdot(root.allies[i], 3.5, 0.2, 0.95, 0.35)\n','\t\troot.allies[i].arrow = image(root.allies[i], MM.ArrowMat, 11, 0.25, 0.95, 0.4, 1)\n')
i=s.index('\t-- arrow out of stacked rows');j=s.index('\tlocal h = MM.Size / 2\n',i)
s=s[:i]+'\t-- you: smaller than before (was about 20 tall)\n\timage(clip, MM.ArrowMat, 13, 1, 1, 1, 1)\n'+s[j:]
s=rep(s,'\troot.count = text(leftBox, 16, 5)','''	-- name of the place, always upright
	local placeBox = LUI.UIElement.new()
	placeBox:setLeftRight(true, true, 0, 0)
	placeBox:setTopBottom(false, true, 33, 51)
	root:addElement(placeBox)
	bar(placeBox, -h - 2, -9, h + 2, 9, 0.03, 0.05, 0.07, 0.7)
	root.place = text(placeBox, 14, 2)
	root.count = text(leftBox, 16, 5)''')
s=rep(s,'MM.UpdateInfo = function(self)\n','''MM.PlaceColor = {
	{ "FUEGO", 1, 0.4, 0.25 }, { "HIELO", 0.4, 0.8, 1 }, { "VIENTO", 0.95, 0.9, 0.5 }, { "RAYO", 0.8, 0.5, 1 },
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
''')
s=rep(s,'\tsafe("info", MM.UpdateInfo, self)\n','\tsafe("info", MM.UpdateInfo, self)\n\tsafe("place", MM.UpdatePlace, self)\n')
# block balance, strings/comments removed
t=re.sub(r'--[^\n]*','',re.sub(r'"(?:\\.|[^"\\])*"','""',s))
op=len(re.findall(r'\b(function|if|do)\b',t));en=len(re.findall(r'\bend\b',t));print('lua blocks',op,en);assert op==en
for a,b in('()','{}','[]'):
    assert t.count(a)==t.count(b),a
    assert g.count(a)==g.count(b),a
if len(sys.argv)>3 and sys.argv[3]=='install':
    R=T+'/respaldo_hud/zm_minimapa_v11';assert not os.path.exists(R);shutil.copytree(M,R)
    shutil.copy2(T+'/images/hud_zombierank_5.iwi',T+'/respaldo_hud/hud_zombierank_5_v11.iwi')
    for n,b in ic.items():
        for p in(M,T):
            with open(p+'/images/%s.iwi'%n,'wb') as fh: fh.write(b)
    with open(gp,'w',newline='\n') as fh: fh.write(g)
    with open(lp,'w',newline='\n') as fh: fh.write(s)
    print('instalado')
else:
    with open(DOC+'v12_prev.lua','w',newline='\n') as fh: fh.write(s)
