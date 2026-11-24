import sys,io,struct,shutil,re,json
S,T,M=sys.argv[1:4]; sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
Q=S+'/mm/'
surf=Image.open(Q+'surf11.png');und=Image.open(Q+'und11.png').resize((1024,1024),Image.LANCZOS);um=np.load(Q+'um.npy');sm=np.load(Q+'sm.npy')
# grey hint where only a lower floor exists
only=cv2.resize((um&(cv2.dilate(sm,np.ones((9,9),np.uint8))==0)).astype(np.uint8)*255,(1024,1024),interpolation=cv2.INTER_AREA)
base=Image.new('RGBA',(1024,1024),(0,0,0,0))
g=np.zeros((1024,1024,4),np.uint8);g[...,:3]=(70,72,76);g[...,3]=(only*.8).astype(np.uint8)
base.alpha_composite(Image.fromarray(g));base.alpha_composite(surf.resize((1024,1024),Image.LANCZOS))
K=4
def icons(im,items,tr):
    lay=Image.new('RGBA',(im.size[0]*K,im.size[1]*K),(0,0,0,0)); d=ImageDraw.Draw(lay)
    fnt=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',14*K)
    for x,y,t,c in items:
        X,Y=tr(x,y);X*=K;Y*=K;r=(12 if t[0]=='G' else 9.5)*K
        if t=='foot':
            r=12*K;d.ellipse((X-r,Y-r,X+r,Y+r),fill=(255,150,30,45),outline=(255,165,40,200),width=2*K)
            for dx in(-4,4): d.rounded_rectangle((X+(dx-2.6)*K,Y-5*K,X+(dx+2.6)*K,Y+5*K),radius=2*K,fill=(255,175,60,200))
            continue
        d.ellipse((X-r-K,Y-r-K,X+r+K,Y+r+K),fill=(0,0,0,255));d.ellipse((X-r,Y-r,X+r,Y+r),fill=c+(255,))
        q=r-1.8*K;d.ellipse((X-q,Y-q,X+q,Y+q),fill=(16,20,25,255))
        d.text((X,Y),t,font=fnt,fill=c+(255,),anchor='mm')
    im.alpha_composite(lay.resize(im.size,Image.LANCZOS))
tr=lambda x,y:((x-128)/10000*1024+512,512-(y-808)/10000*1024)
feet=[(-227.5,4118),(519.5,3126.5),(2324,3144.5),(2094.5,803.5),(515.5,812),(-1631.5,675.5),(-2526,-365),(-880,-364.5),(1261.5,-235),(2884.5,-237),(336,-1969),(954,-3124)]
col=dict(specialty_armorvest=('J',(235,70,60)),specialty_longersprint=('M',(255,195,60)),specialty_quickrevive=('R',(90,165,255)),specialty_fastreload=('S',(70,215,100)),specialty_weapupgrade=('P',(255,130,225)))
gn=dict(generator_start_bunker='G1',generator_tank_trench='G2',generator_mid_trench='G3',generator_nml_right='G4',generator_nml_left='G5',generator_church='G6')
items=[(x,y,'foot',None) for x,y in feet]
for e in json.load(open(Q+'ents.json')):
    if 'origin' not in e: continue
    x,y=map(float,e['origin'].split()[:2]);t=e.get('targetname');n=e.get('script_noteworthy')
    if t=='random_perk_machine': items.append((x,y,'W',(205,120,255)))
    if t=='zm_perk_machine' and n in col: items.append((x,y)+col[n])
    if t=='s_generator': items.append((x,y,gn[n],(230,235,240)))
print(len(items),sorted(i[2] for i in items))
icons(base,items,tr); base.save(Q+'base11.png')
# ---- atlas
m1=(cv2.resize(um*255,(1024,1024),interpolation=cv2.INTER_AREA)>110).astype(np.uint8)
n,core=cv2.connectedComponents(cv2.dilate(m1,np.ones((7,7),np.uint8)))
mb=m1.astype(bool); size=lambda k:int((mb&(core==k)).sum())
comps=sorted((k for k in range(1,n) if size(k)>=40),key=lambda k:-size(k))[:8];print([size(k) for k in comps])
dist=np.stack([cv2.distanceTransform((~(mb&(core==k))).astype(np.uint8),cv2.DIST_L2,5) for k in comps]);owner=dist.argmin(0);near=dist.min(0)<=9
icons(und,[(0,-480,'K',(80,215,160))],tr); un=np.array(und)
A=np.zeros((2048,2048,4),np.uint8);U=10000/1024;tiles=[];tc=lambda i:(round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3))
for i in range(len(comps)):
    ys,xs=np.where(near&(owner==i));cx,cy=int(xs.min()+xs.max())//2,int(ys.min()+ys.max())//2;x,y=tc(i)
    w=int(max(np.ptp(xs),np.ptp(ys)))//2+3;assert w<150,w
    A[y+ys-cy,x+xs-cx]=un[ys,xs];tiles.append((128+(cx-512)*U-(x-1024)*U,808-(cy-512)*U+(y-1024)*U))
x,y=tc(8);A[y-230:y+230,x-230:x+230]=np.array(Image.open(Q+'crazy11.png').resize((460,460),Image.LANCZOS))
def dxt(im,h):
    n=im.size[0];b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5');d=b.getvalue()
    assert d[84:88]==b'DXT5' and struct.unpack_from('<HH',h,6)==(n,n)
    return h+d[128:128+n*n]
out={}
for f,im in(('icon_twitter',base),('hud_zombierank_5',Image.fromarray(A))):
    with open(M+f'/images/{f}.iwi','rb') as fh: out[f]=dxt(im,fh.read(64))
Image.fromarray(A).save(Q+'atlas11.png')
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
with open(gp,newline='') as f:g=f.read()
with open(lp,newline='') as f:s=f.read()
def part(mm):
    kx,ky,z,_=map(int,mm.groups());px=int(round(((kx+.5)*200-128)/U+512));py=int(round(512-((ky+.5)*200-808)/U))
    return 'mml_cell( %d, %d, %d, %d );'%(kx,ky,z,int(owner[py,px])+1)
g,c=re.subn(r'mml_cell\( (-?\d+), (-?\d+), (-?\d+), (\d+) \);',part,g);assert c==195
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.Under = {\n'+''.join('\t{ %.1f, %.1f },\n'%t for t in tiles)+'}\n'+s[j:]
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a);s=s.replace(a,b)
# fixed places are printed on the map; only the box (moves) and the captured badge stay live
i=s.index('\t\t-- icons that would overlap');j=s.index('\t\tif e and math.abs(ex) < half - 2',i);s=s[:i]+s[j:]
rep('\t\t\te.px, e.py = ex, ey\n','')
i=s.index('\t\tlocal color = MM.PoiColor');j=s.index('\t\tlocal e = color and',i)
s=s[:i]+'''		local kind = string.sub(o.t, 1, 1)
		local color = (kind == "B" or kind == "H") and MM.PoiColor[kind]
'''+s[j:]
rep('		local ex, ey = project(o.x, o.y)\n		if e and math','''		local ex, ey = project(o.x, o.y)
		if kind == "H" then
			ex, ey = project(o.x + 105, o.y + 105)
		end
		if e and math''')
rep('e.label:setText((string.gsub(o.t, "H", "G")))','e.label:setText(kind == "H" and "" or o.t)\n\t\t\t\te.box:setAlpha(kind == "H" and 0 or 1)\n\t\t\t\te.cap:setAlpha(kind == "H" and 1 or 0)')
rep('\t\tdot(e, 6, 0.08, 0.1, 0.13)\n','\t\te.box = group(e, 7, 1)\n\t\tdot(e.box, 6, 0.08, 0.1, 0.13)\n\t\te.cap = group(e, 7, 0)\n\t\tdot(e.cap, 3.2, 0.25, 1, 0.35)\n')
rep('mapAlpha = 0.35','mapAlpha = 0.3')
shutil.copytree(M,T+'/respaldo_hud/zm_minimapa_v10')
for f,b in out.items():
    for p in(M,T):
        with open(p+f'/images/{f}.iwi','wb') as fh: fh.write(b)
with open(gp,'w',newline='\n') as f:f.write(g)
with open(lp,'w',newline='\n') as f:f.write(s)
v=Image.new('RGBA',(1024,1024),(10,14,18,255));v.alpha_composite(base);v.save(Q+'base11v.png');print('ok')
