"""v15: roofs from the level geometry (one tile per structure, two atlases) + rotation fix.
usage: v15.py S T [install]"""
import sys,io,re,os,struct,shutil
S,T=sys.argv[1:3];M=T+'/mods/zm_minimapa';Q=S+'/mm/';DOC=__import__('os').environ['MM_DOCS']+'/';G=DOC+'generadores/'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image
v14=open(G+'v14.py',encoding='utf8').read()
# drawing helpers of v14 (icons)
import math
from PIL import ImageDraw,ImageFont
K=6
exec(v14[v14.index('EL={'):v14.index('U=10000/1024')])
exec(v14[v14.index('def draw('):v14.index('ui=Image.fromarray')])
N=2048;U=10000/N
pts=np.load(Q+'reach_main.npy').astype(int);roof=np.load(Q+'roof1.npy').astype(int)
Y,X,Z=pts.T;X=X+360;wz=-820+Z*12.;wx=128+(X+.5-1024)*U;wy=808-(Y+.5-1024)*U
cov=roof<60
# ---- majority smoothing of the covered flag in plan, per 3D neighbourhood (36u steps in height)
key=lambda y,x,z:(y>>3)*100000+(x>>3)*40+(z>>2)
kk=key(Y,X,Z);u,inv=np.unique(kk,return_inverse=True)
frac=np.bincount(inv,cov)/np.bincount(inv);cov=np.where(frac[inv]>.8,True,np.where(frac[inv]<.2,False,cov))
# ---- old cave split, to keep the elemental caves apart
um=np.load(Q+'um.npy').astype(np.uint8);m1=(cv2.resize(um*255,(1024,1024),interpolation=cv2.INTER_AREA)>110).astype(np.uint8)
n,core=cv2.connectedComponents(cv2.dilate(m1,np.ones((7,7),np.uint8)));mb=m1.astype(bool);size=lambda k:int((mb&(core==k)).sum())
comps=sorted((k for k in range(1,n) if size(k)>=40),key=lambda k:-size(k))[:8]
dist=np.stack([cv2.distanceTransform((~(mb&(core==k))).astype(np.uint8),cv2.DIST_L2,5) for k in comps]);owner=dist.argmin(0);near=dist.min(0)<=9
o=owner[Y//2,X//2];nr=near[Y//2,X//2]
part=np.zeros(len(pts),int)
# 1 crypt, 2 lightning, 3 wind, 4 ice, 5 fire
c=cov
part[c&(wx**2+wy**2<640**2)]=1
part[c&nr&(o==2)&(wx<-2850)]=-2 # lightning: drawn from the older, complete picture
part[c&nr&(o==3)]=3
part[c&nr&(o==4)&(wy>-2560)]=4
part[c&nr&(o==5)]=5
# the rest: structures
rest=c&(part==0);m=np.zeros((N,N),np.uint8);m[Y[rest],X[rest]]=1
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
e=cv2.morphologyEx(m,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19)))
n,l,st,ce=cv2.connectedComponentsWithStats(m)
big=[k for k in range(1,n) if st[k,4]*U*U>45000]
big.sort(key=lambda k:-st[k,4]);print('estructuras',len(big),[(int(128+(ce[k][0]-1024)*U),int(808-(ce[k][1]-1024)*U),int(st[k,4]*U*U)) for k in big])
big=[k for k in big if not any(abs(128+(ce[k][0]-1024)*U-a)<150 and abs(808-(ce[k][1]-1024)*U-b)<150 for a,b in((2018,-1003),(-791,247)))]
big=big[:12];lm=np.zeros(n,int)
for i,k in enumerate(big):lm[k]=6+i
lab=lm[l];part[rest]=lab[Y[rest],X[rest]]
NP=5+len(big)
AMB=(255,186,96);COL={1:(60,215,190),2:EL['rayo'],3:EL['viento'],4:EL['hielo'],5:EL['fuego']}
tr=lambda x,y:((x-128)/U+1024,1024-(y-808)/U)
def tile(p):
    k=part==p;z=np.full((N,N),-9999.,np.float32);np.maximum.at(z,(Y[k],X[k]),wz[k].astype(np.float32))
    mm=(z>-9000).astype(np.uint8);mm=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
    nc,l2,s2,_=cv2.connectedComponentsWithStats(1-mm);bad=s2[:,4]<90;bad[0]=False;mm[bad[l2]]=1
    nc,l2,s2,_=cv2.connectedComponentsWithStats(mm);bad=s2[:,4]<500;bad[0]=False;mm[bad[l2]]=0
    f=cv2.GaussianBlur(mm.astype(np.float32),(0,0),2.2);mm=(f>.5).astype(np.float32)
    ok=(z>-9000).astype(np.float32);zz=np.where(ok>0,z,0)
    zf=cv2.GaussianBlur(zz*ok,(0,0),2.5)/np.maximum(cv2.GaussianBlur(ok,(0,0),2.5),1e-4)
    gy,gx=np.gradient(zf);sh=np.clip((gx+gy)*-.012,-.22,.22)
    v=zf[mm>0];lo,hi=np.percentile(v,[3,97]);h=np.clip((zf-lo)/max(60,hi-lo),0,1)
    br=(.5+.5*h+sh) if p==1 else (.68+.22*h+sh)
    out=np.array(COL.get(p,AMB),np.float32)[None,None]*np.clip(br,.3,1.1)[...,None]
    aa=cv2.GaussianBlur(mm,(0,0),.8);edge=np.clip(cv2.dilate(aa,np.ones((5,5)))-cv2.erode(aa,np.ones((3,3))),0,1)[...,None]
    out=out*(1-edge*.75)+(np.array(COL.get(p,AMB))*.45+140)*edge*.75
    a=np.clip(cv2.dilate(aa,np.ones((5,5))),0,1)
    return np.dstack([np.clip(out,0,255),a*255]).astype(np.uint8)
CUR=open(T+'/respaldo_hud/zm_minimapa_v14/ui_mp/t6/zombie/hudtimerzombie.lua' if os.path.exists(T+'/respaldo_hud/zm_minimapa_v14') else M+'/ui_mp/t6/zombie/hudtimerzombie.lua').read()
ub=CUR[CUR.index('MM.Under = {'):];un14=[tuple(map(float,t)) for t in re.findall(r'\{ (-?[\d.]+), (-?[\d.]+) \}',ub[:ub.index('\n}')])]
def rayo():
    a=np.array(Image.open(G+'atlas14.png').convert('RGBA'));x0,y0=round(2.5*2048/3),round(.5*2048/3)
    wxc,wyc=un14[2][0]+(x0-1024)*U,un14[2][1]-(y0-1024)*U
    X0,Y0=[int(round(v)) for v in tr(wxc,wyc)];out=np.zeros((N,N,4),np.uint8);r=170
    c=a[y0-r:y0+r,x0-r:x0+r];l=max(0,r-X0);out[Y0-r:Y0+r,X0-r+l:X0+r]=c[:,l:]
    out[:,int(tr(-2850,0)[0]):]=0
    return out
items={1:[(160,112,'staff',EL['viento']),(-160,112,'staff',EL['fuego']),(-208,-16,'staff',EL['rayo']),(208,-16,'staff',EL['hielo'])]}
A=[np.zeros((N,N,4),np.uint8) for _ in range(2)];tiles=[];boxes=[]
tc=lambda i:(round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3))
# slots: atlas 1 holds parts 1..8 (slot 8 = Crazy Place), atlas 2 the rest
for p in range(1,NP+1):
    t=Image.fromarray(tile(p) if p!=2 else rayo())
    if p==1:
        draw(t,tr,[(0,-480,'K',(120,255,170))],15);draw(t,tr,items[1],12)
    t=np.array(t);ys,xs=np.where(t[...,3]>8);cx,cy=int(xs.min()+xs.max())//2,int(ys.min()+ys.max())//2
    a,slot=(0,p-1) if p<=8 else (1,p-9);x,y=tc(slot)
    assert max(np.ptp(xs),np.ptp(ys))<660,(p,np.ptp(xs),np.ptp(ys))
    A[a][y+ys-cy,x+xs-cx]=t[ys,xs]
    tiles.append((128+(cx-1024)*U-(x-1024)*U,808-(cy-1024)*U+(y-1024)*U,a+1))
    boxes.append([round(v) for v in(128+(xs.min()-1-1024)*U,128+(xs.max()+2-1024)*U,808-(ys.max()+2-1024)*U,808-(ys.min()-1-1024)*U)])
old=np.array(Image.open(G+'atlas14.png').convert('RGBA'));x,y=tc(8);A[0][y-330:y+330,x-330:x+330]=old[y-330:y+330,x-330:x+330]
for i in(0,1):Image.fromarray(A[i]).save(G+'atlas15_%d.png'%(i+1))
# ---- lookup cells, 100u: z threshold below which you are inside that part
C=100;cellx=np.floor((wx+20000)/C).astype(int);celly=np.floor((wy+20000)/C).astype(int);cid=cellx*1000+celly
order=np.argsort(cid,kind='stable');cells=[];okc=tot=0
B_=np.flatnonzero(np.diff(cid[order]))+1
for g in np.split(order,B_):
    z=wz[g];p=part[g];c=cov[g]&(p>0)
    if c.sum()<max(12,.2*len(g)):continue
    ent=[];top=None
    for q in np.unique(p[c]):
        s=c&(p==q)
        if s.sum()<.15*len(g):continue
        hi=np.percentile(z[s],95);un=z[~s&(z>hi+50)]
        lo=z[s].min()
        th=hi+70 if not len(un) else min(hi+70,(hi+np.percentile(un,5))/2)
        # open floor at the same height wins when it is the majority
        same=(~c)&(z>lo-40)&(z<th)
        if same.sum()>s.sum():continue
        ent.append((int(th),int(q)))
    ent.sort()
    for th,q in ent[:2]:cells.append((int(cid[g[0]]//1000),int(cid[g[0]]%1000),th,q))
have={(a,b) for a,b,_,_ in cells}
for a,b,z in re.findall(r'mml_cell\( (-?\d+), (-?\d+), (-?\d+), 3 \)',open(T+('/respaldo_hud/zm_minimapa_v14' if os.path.exists(T+'/respaldo_hud/zm_minimapa_v14') else '/mods/zm_minimapa')+'/scripts/zm/zm_tomb/minimapa_lui.gsc').read()):
    a,b=int(a),int(b)
    if a>-15:continue
    for i in(0,1):
        for j in(0,1):
            k=((a+100)*2+i,(b+100)*2+j)
            if k not in have:cells.append(k+(int(z),2))
look={}
for a,b,t,q in cells:look.setdefault((a,b),[]).append((t,q))
hit=np.array([next((q for t,q in look.get((a,b),()) if zz<t),0) for a,b,zz in zip(cellx,celly,wz)])
ins=cov&(part>0)
print('celdas',len(cells),'dentro bien %.1f%%'%(100*(hit[ins]==part[ins]).mean()),'fuera bien %.1f%%'%(100*(hit[~ins]==0).mean()))
for q in range(1,NP+1):
    k=part==q;print(q,'bien %.0f%%'%(100*(hit[k]==q).mean()),boxes[q-1])
if len(sys.argv)<4:
    v=np.zeros((N,N,4),np.uint8);v[...,3]=255
    im=Image.fromarray(v);im.alpha_composite(Image.open(Q+'base11.png').resize((N,N)));im=Image.fromarray((np.array(im)*[.4,.4,.4,1]).astype(np.uint8))
    for p in range(NP,0,-1):
        t=Image.fromarray(tile(p) if p!=2 else rayo())
        if p==1:draw(t,tr,[(0,-480,'K',(120,255,170))],15);draw(t,tr,items[1],12)
        im.alpha_composite(t)
    d=ImageDraw.Draw(im)
    for p in range(1,NP+1):
        b=boxes[p-1];d.text(tr(b[0],b[3]),str(p),font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',40),fill='white',anchor='rb')
    im.crop((340,0,1760,N)).convert('RGB').save(DOC+'techos.png');sys.exit()
# ================= install
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
g=open(gp,newline='').read();s=open(lp,newline='').read()
def R(t,a,z,c=1):
    assert t.count(a)==c,(t.count(a),a);return t.replace(a,z)
# GSC: compact cells
i=g.index('mml_under( org )');j=g.index('mml_inside( org )')
rows=[';'.join('%d,%d,%d,%d'%c for c in cells[k:k+25]) for k in range(0,len(cells),25)]
g=g[:i]+'''mml_under( org )
{
	// 100 unit cells; the offset keeps the values positive
	k = mml_key( int( ( org[ 0 ] + 20000 ) / 100 ), int( ( org[ 1 ] + 20000 ) / 100 ) );
	if ( isdefined( level.mml_cells[ k ] ) && org[ 2 ] < level.mml_cells[ k ] )
		return level.mml_parts[ k ];
	k = k + "b";
	if ( isdefined( level.mml_cells[ k ] ) && org[ 2 ] < level.mml_cells[ k ] )
		return level.mml_parts[ k ];
	return 0;
}

// "x,y,z,part;..." a second entry of a cell is the higher one
mml_row( row )
{
	list = strtok( row, ";" );
	for ( i = 0; i < list.size; i++ )
	{
		v = strtok( list[ i ], "," );
		k = v[ 0 ] + "_" + v[ 1 ];
		if ( isdefined( level.mml_cells[ k ] ) )
			k = k + "b";
		level.mml_cells[ k ] = int( v[ 2 ] );
		level.mml_parts[ k ] = int( v[ 3 ] );
	}
	wait 0.05;
}

mml_cells_setup()
{
'''+''.join('\tmml_row( "%s" );\n'%r for r in rows)+'}\n\n'+g[j:]
i=g.index('mml_cell( x, y, z, part )');j=g.index('mml_under( org )');g=g[:i]+g[j:]
g=R(g,'\tmml_cells_setup();\n','\tlevel thread mml_cells_setup();\n')
g=R(g,'precacheshader( "zombies_rank_5" );\n','precacheshader( "zombies_rank_5" );\n\tprecacheshader( "menu_lobby_icon_facebook" );\n')
# name: inside a cave the cave wins over the (bigger) zone volume
g=R(g,'\t\tme = players[ 0 ];\n\t\tif ( isdefined( last )','''		me = players[ 0 ];
		special = mml_part_name( mml_under( me.origin ) );
		if ( special != "" )
		{
			last = undefined;
			setdvar( "mm_zone", special );
			continue;
		}
		if ( isdefined( last )''')
g=g.rstrip()+'''

mml_part_name( part )
{
	switch ( part )
	{
		case 1:
			return "CRIPTA";
		case 2:
			return "CUEVA DE RAYO";
		case 3:
			return "CUEVA DE VIENTO";
		case 4:
			return "CUEVA DE HIELO";
		case 5:
			return "CUEVA DE FUEGO";
	}
	return "";
}
'''
g=R(g,'\tsetdvar( "mm_zone", "" );\n','\tsetdvar( "mm_zone", "" );\n\tif ( getdvar( "mm_giro" ) == "" )\n\t\tsetdvar( "mm_giro", "1" ); // 0 plain, 1 compensate rotation delay, 2 container\n')
# Lua
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.AtlasB = "menu_lobby_icon_facebook"\n-- x, y, atlas\nMM.Under = {\n'+''.join('\t{ %.1f, %.1f, %d },\n'%t for t in tiles)+'}\n'+s[j:]
i=s.index('MM.BigCaves = {');j=s.index('MM.BigLabels');s=s[:i]+'MM.BigCaves = {\n'+''.join('\t{ %d, %d, %d, %d, %d },\n'%((q,)+tuple(boxes[q-1])) for q in range(1,NP+1))+'}\n'+s[j:]
s=R(s,'elseif i >= 3 and i <= 6 then','elseif i >= 2 and i <= 5 then')
s=R(s,'image(box, MM.CrazyMaterial, MM.UnderWorld * bk','image(box, MM.Under[d[1]][3] == 2 and MM.AtlasB or MM.CrazyMaterial, MM.UnderWorld * bk')
s=R(s,'if self.part == 2 then','if self.part == 1 then')
s=R(s,'''		elseif MM.Under[self.part] then
			range = math.min(range, MM.CaveRange)''','''		elseif MM.Under[self.part] then
			range = math.min(range, self.part <= 5 and MM.CaveRange or 1300)''')
s=R(s,'		self.rotsign = dvarNum("mm_rotsign", 1)\n','		self.rotsign = dvarNum("mm_rotsign", 1)\n		self.giro = dvarNum("mm_giro", 1)\n')
# rotation of a picture is shown one frame after its position: place everything with the yaw of the previous frame
s=R(s,'	local px, py, yaw = me.x, me.y, me.yaw\n','''	local px, py, yaw = me.x, me.y, me.yaw
	local newYaw = yaw
	if self.giro == 1 then
		yaw = me.lastYaw or yaw
	end
	me.lastYaw = newYaw
''')
i=s.index('\tshow(self.map, mapAlpha)\n');j=s.index('\t-- compass letters')
s=s[:i]+'''	local spin = self.giro == 2
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
			e:setZRot((90 - newYaw) * rs)
		end
	end
	if spin then
		self.spin:setZRot((90 - newYaw) * rs)
	end
	if crazy then
		lay(layer[2], MM.CrazyX, MM.CrazyY, MM.CrazyWorld)
	else
		lay(layer[1], MM.CenterX, MM.CenterY, MM.World)
		if under then
			lay(layer[1 + a], under[1], under[2], MM.UnderWorld)
		end
	end

'''+s[j:]
i=s.index('\t-- Each element rotates about');j=s.index('\tlocal under = not crazy')
s=s[:i]+s[j:]
i=s.index('\troot.map = image(');j=s.index('\tlocal function bar(parent')
pic='''	local function pictures(p)
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
'''
s=s[:i]+pic+s[j:]
# every delayed-yaw consumer uses the same value, allies included
t=re.sub('--.*','',re.sub('"[^"]*"','',s))
a_,b_=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',a_,b_);assert a_==b_
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1]) and g.count(q[0])==g.count(q[1])
assert 'self.map' not in s and 'self.crazyMap' not in s
with open(M+'/images/hud_zombierank_5.iwi','rb') as fh:hdr=fh.read(64)
def dxt(a):
    b=io.BytesIO();Image.fromarray(a).save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5';return hdr+d[128:128+N*N]
RR=T+'/respaldo_hud/zm_minimapa_v14';assert not os.path.exists(RR);shutil.copytree(M,RR)
for f,a in(('hud_zombierank_5',A[0]),('icon_facebook',A[1])):
    b=dxt(a)
    for p in(M,T):
        with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(b)
for p,xx in((gp,g),(lp,s)):
    with open(p,'w',newline='') as fh:fh.write(xx)
print('instalado')
