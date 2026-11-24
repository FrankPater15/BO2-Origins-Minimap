"""v16: perk machines with the game's own perk icons (by material name), drawn upright and on top of the highlights."""
import sys,io,os,re,json,shutil,struct
S,T=sys.argv[1:3];M=T+'/mods/zm_minimapa';Q=S+'/mm/';G=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(Q+'v11.py',encoding='utf8').read().split('icons(base,items,tr); base.save')[0]
argv=sys.argv;sys.argv=['x',S,T,M]
exec(src)
sys.argv=argv
# only what still has no live icon stays printed
fixed=[]
for e in json.load(open(Q+'ents.json')):
    if 'origin' not in e: continue
    x,y=[round(float(v)) for v in e['origin'].split()[:2]];t=e.get('targetname');n=e.get('script_noteworthy')
    if t=='random_perk_machine':fixed.append((x,y,'W'))
    if t=='s_generator':fixed.append((x,y,gn[n]))
    k={'specialty_armorvest':'J','specialty_longersprint':'M','specialty_quickrevive':'R','specialty_fastreload':'S','specialty_additionalprimaryweapon':'K'}.get(n)
    if t=='zm_perk_machine' and k:fixed.append((x,y,k))
print(len(fixed),fixed);assert len(fixed)==17
items=[i for i in items if i[2] in('foot','P')]
icons(base,items,tr);base.save(G+'base16.png')
with open(M+'/images/icon_twitter.iwi','rb') as fh:h=fh.read(64)
b=io.BytesIO();base.save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5' and struct.unpack_from('<HH',h,6)==(1024,1024)
tw=h+d[128:128+1024*1024]
# crypt tile without the printed K: rerun the v15 drawing code
v15=open(G+'v15.py',encoding='utf8').read().split('# ---- lookup cells')[0]
v15=v15.replace("draw(t,tr,[(0,-480,'K',(120,255,170))],15);","").replace("G+'atlas15_%d.png'","G+'atlas16_%d.png'")
ns={'__file__':__file__}
sys.argv=['x',S,T];exec(compile(v15,'v15','exec'),ns);sys.argv=argv
A,tiles,boxes=ns['A'],ns['tiles'],ns['boxes']
with open(M+'/images/hud_zombierank_5.iwi','rb') as fh:h2=fh.read(64)
b=io.BytesIO();Image.fromarray(A[0]).save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();rk=h2+d[128:128+2048*2048]
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';s=open(lp,newline='').read()
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';g=open(gp,newline='').read()
def rep(a,z):
    global s
    assert s.count(a)==1,(s.count(a),a);s=s.replace(a,z)
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.Under = {\n'+''.join('\t{ %.1f, %.1f, %d },\n'%t for t in tiles)+'}\n'+s[j:]
i=s.index('MM.BigCaves = {');j=s.index('MM.BigLabels');s=s[:i]+'MM.BigCaves = {\n'+''.join('\t{ %d, %d, %d, %d, %d },\n'%((q+1,)+tuple(bx)) for q,bx in enumerate(boxes))+'}\n'+s[j:]
rep('MM.BigSize = 640\n','''MM.BigSize = 640
-- icons that belong to the game itself; only their names are used here
MM.PerkMat = {
	J = "specialty_juggernaut_zombies", R = "specialty_quickrevive_zombies", S = "specialty_fastreload_zombies",
	M = "specialty_marathon_zombies", K = "specialty_additionalprimaryweapon_zombies",
}
-- fixed places: x, y, kind
MM.Fixed = {
'''+''.join('\t{ %d, %d, "%s" },\n'%f for f in fixed)+'''}
''')
# alpha of a fixed place: full on its own floor, faded when you are inside another structure
rep('MM.Update = function(self, event)\n\tlocal state','''local function fixedAlpha(f, part)
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
	local state''')
rep('	local pi = 0\n	for k = 1, #self.poiList do\n','''	for i = 1, #MM.Fixed do
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
''')
rep('	root.poi = {}\n	for i = 1, MM.MaxPoi do','''	local function fixedIcon(parent, kind, k)
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
			dot(e, 6.6 * k, 0.95, 0.95, 0.95)
			dot(e, 5 * k, 0.07, 0.09, 0.12)
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
	for i = 1, MM.MaxPoi do''')
rep('	big.feet, big.caps, big.zombies','''	big.fixed = {}
	for i = 1, #MM.Fixed do
		local e = fixedIcon(view, MM.Fixed[i][3], 0.95)
		place(e, (MM.Fixed[i][1] - MM.CenterX) * MM.BigSize / MM.World, (MM.CenterY - MM.Fixed[i][2]) * MM.BigSize / MM.World, 7, 0)
		big.fixed[i] = e
	end
	big.feet, big.caps, big.zombies''')
rep('	local rs = self.rotsign or 1\n	local function put(','''	for i = 1, #MM.Fixed do
		show(big.fixed[i], crazy and 0 or fixedAlpha(MM.Fixed[i], part))
	end
	local rs = self.rotsign or 1
	local function put(''')
# the live box/captured badges must not repeat the old letters
g_add=''.join('\tprecacheshader( "%s" );\n'%m for m in('specialty_juggernaut_zombies','specialty_quickrevive_zombies','specialty_fastreload_zombies','specialty_marathon_zombies','specialty_additionalprimaryweapon_zombies'))
a='\tprecacheshader( "zombies_rank_5" );\n';assert g.count(a)==1;g=g.replace(a,a+g_add)
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x1,x2=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',x1,x2);assert x1==x2
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1])
assert s.index('local function oval(')<s.index('local function fixedIcon(') and s.index('local function text(')<s.index('local function fixedIcon(')
R=T+'/respaldo_hud/zm_minimapa_v15';assert not os.path.exists(R);shutil.copytree(M,R)
for p in(M,T):
    for n,v in(('icon_twitter',tw),('hud_zombierank_5',rk)):
        with open(p+'/images/%s.iwi'%n,'wb') as fh:fh.write(v)
for p,v in((lp,s),(gp,g)):
    with open(p,'w',newline='') as fh:fh.write(v)
print('instalado')
