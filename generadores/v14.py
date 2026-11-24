import sys,io,re,os,struct,shutil,math
S,T=sys.argv[1:3];M=T+'/mods/zm_minimapa';Q=S+'/mm/';DOC=__import__('os').environ['MM_DOCS']+'/'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
EL={'fuego':(255,90,50),'hielo':(90,200,255),'viento':(240,225,110),'rayo':(195,115,255)}
U=10000/1024;U2=U/2
# ---- same cave split as before
um=np.load(Q+'um.npy').astype(np.uint8)
m1=(cv2.resize(um*255,(1024,1024),interpolation=cv2.INTER_AREA)>110).astype(np.uint8)
n,core=cv2.connectedComponents(cv2.dilate(m1,np.ones((7,7),np.uint8)));mb=m1.astype(bool)
size=lambda k:int((mb&(core==k)).sum())
comps=sorted((k for k in range(1,n) if size(k)>=40),key=lambda k:-size(k))[:8]
dist=np.stack([cv2.distanceTransform((~(mb&(core==k))).astype(np.uint8),cv2.DIST_L2,5) for k in comps]);owner=dist.argmin(0);near=dist.min(0)<=9
src=Image.open(Q+'und11.png');print('und',src.size)
und=np.array(src.resize((2048,2048),Image.LANCZOS))
own2=owner.repeat(2,0).repeat(2,1);near2=near.repeat(2,0).repeat(2,1)
tint={1:(60,215,190),2:EL['rayo'],3:EL['viento'],4:EL['hielo'],5:EL['fuego']}
for i,c in tint.items():
    k=near2&(own2==i);lum=und[...,:3].mean(2)
    solid=k&(und[...,3]>120)
    lo,hi=np.percentile(lum[solid],[4,96]);a,z=(.38,1.12) if i==1 else (.6,1.1)
    f=a+(z-a)*np.clip((lum-lo)/max(1,hi-lo),0,1.1)
    for q in range(3):
        und[...,q]=np.where(k,np.clip(c[q]*f,0,255),und[...,q]).astype(np.uint8)
K=6
def draw(im,tr,items,r):
    """items: x,y,kind,colour. kind: staff, portal or a letter. r = radius in pixels"""
    lay=Image.new('RGBA',(im.width*K,im.height*K),(0,0,0,0)) if im.width<1200 else None
    for x,y,t,c in items:
        X,Y=tr(x,y);n=int(r*2.6);s=n*2*K;p=Image.new('RGBA',(s,s),(0,0,0,0));d=ImageDraw.Draw(p);o=s/2;R=r*K
        if t=='portal':
            R*=1.15
            for q,col in((1.12,(0,0,0,255)),(1,c+(255,)),(.72,(12,14,20,255))):d.ellipse((o-R*q,o-R*q,o+R*q,o+R*q),fill=col)
            pts=[(o+R*.62*(a/24)*math.cos(a*.62),o+R*.62*(a/24)*math.sin(a*.62)) for a in range(25)]
            d.line(pts,fill=c+(255,),width=int(R*.17),joint='curve')
        else:
            for q,col in((1.14,(0,0,0,255)),(1,c+(255,)),(.82,(14,18,24,255))):d.ellipse((o-R*q,o-R*q,o+R*q,o+R*q),fill=col)
            if t=='staff':
                g=lambda a,b:(o+a*R,o+b*R)
                d.line([g(-.42,.52),g(.24,-.2)],fill=(235,225,205,255),width=int(R*.2))
                d.line([g(.02,-.28),g(.34,.06)],fill=(235,225,205,255),width=int(R*.16))
                a,b=g(.34,-.32);e=R*.27;d.ellipse((a-e,b-e,a+e,b+e),fill=c+(255,))
            else:d.text((o,o),t,font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',int(R*1.3)),fill=c+(255,),anchor='mm')
        p=p.resize((n*2,n*2),Image.BOX)
        im.alpha_composite(p,(int(round(X-n)),int(round(Y-n))))
ui=Image.fromarray(und);tr=lambda x,y:((x-128)/U2+1024,1024-(y-808)/U2)
draw(ui,tr,[(0,-480,'K',(120,255,170))],19*.8)
# pedestals of the crypt
staffs=[(160,112,'viento'),(-160,112,'fuego'),(-208,-16,'rayo'),(208,-16,'hielo')]
draw(ui,tr,[(x,y,'staff',EL[e]) for x,y,e in staffs],12)
un=np.array(ui)
A=np.zeros((2048,2048,4),np.uint8);tiles=[];boxes=[];tc=lambda i:(round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3))
for i in range(8):
    k=near2&(own2==i)
    if i==1:k=cv2.dilate(k.astype(np.uint8),np.ones((25,25),np.uint8)).astype(bool)&(un[...,3]>0)  # keep the whole K
    ys,xs=np.where(k);cx,cy=int(xs.min()+xs.max())//2,int(ys.min()+ys.max())//2;x,y=tc(i)
    assert max(np.ptp(xs),np.ptp(ys))<600,(i,np.ptp(xs),np.ptp(ys))
    A[y+ys-cy,x+xs-cx]=un[ys,xs]
    tiles.append((128+(cx-1024)*U2-(x-1024)*U2,808-(cy-1024)*U2+(y-1024)*U2))
    k2=k&(un[...,3]>10);ys,xs=np.where(k2);boxes.append([round(v) for v in(128+(xs.min()-2-1024)*U2,128+(xs.max()+3-1024)*U2,808-(ys.max()+3-1024)*U2,808-(ys.min()-2-1024)*U2)])
boxes[2][1]=-2850;boxes[3][0]=2290
# ---- Crazy Place
cp=Image.open(Q+'crazy11.png').convert('RGBA');print('crazy',cp.size)
c=np.array(cp);h=c.shape[0];alpha=c[...,3];sc=h/1200
white=c[...,:3].min(2)>175
solid=(alpha>200).astype(np.uint8);inside=cv2.erode(solid,np.ones((int(9*sc)|1,)*2,np.uint8))
edge=cv2.dilate((white&(alpha>60)).astype(np.uint8),np.ones((int(9*sc)|1,)*2,np.uint8))
flat=cv2.cvtColor(cv2.medianBlur(cv2.cvtColor(c[...,:3],cv2.COLOR_RGB2BGR),int(17*sc)|1),cv2.COLOR_BGR2RGB)
ok=((inside>0)&(edge==0));w=cv2.GaussianBlur(ok.astype(np.float32),(0,0),2*sc)[...,None]*ok[...,None]
c[...,:3]=(flat*w+c[...,:3]*(1-w)).astype(np.uint8)
P=660;ci=Image.fromarray(c).resize((P,P),Image.LANCZOS);ct=lambda x,y:((x-10464)/2700*P+P/2,P/2-(y+7788)/2700*P)
port=[(11322,-8813,'viento'),(9425,-8620,'fuego'),(9552,-6905,'rayo'),(11367,-6900,'hielo')]
ped=[(10576,-8142,'viento'),(10104,-8142,'fuego'),(10104,-7670,'rayo'),(10576,-7670,'hielo')]
draw(ci,ct,[(x,y,'portal',EL[e]) for x,y,e in port],23);draw(ci,ct,[(x,y,'staff',EL[e]) for x,y,e in ped],22)
x,y=tc(8);A[y-P//2:y+P//2,x-P//2:x+P//2]=np.array(ci)
cu=2700/P;CW=cu*2048;CX=10464-(x-1024)*cu;CY=-7788+(y-1024)*cu
at=Image.fromarray(A);at.save(DOC+'generadores/atlas14.png')
with open(M+'/images/hud_zombierank_5.iwi','rb') as fh:hdr=fh.read(64)
b=io.BytesIO();at.save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5';iwi=hdr+d[128:128+2048*2048]
# ---- Lua
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';s=open(lp,newline='').read()
def rep(a,z):
    global s
    assert s.count(a)==1,(s.count(a),a);s=s.replace(a,z)
def num(k,v):
    global s
    s,c=re.subn(r'(?m)^MM\.%s = \S+'%k,'MM.%s = %.1f'%(k,v),s);assert c==1,k
num('CrazyX',CX);num('CrazyY',CY);num('CrazyWorld',CW);num('UnderWorld',10000)
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.Under = {\n'+''.join('\t{ %.1f, %.1f },\n'%t for t in tiles)+'}\n'+s[j:]
i=s.index('MM.BigCaves = {');j=s.index('MM.BigLabels');s=s[:i]+'MM.BigCaves = {\n'+''.join('\t{ %d, %d, %d, %d, %d },\n'%((q,)+tuple(boxes[q-1])) for q in range(1,9))+'}\n'+s[j:]
rep('MM.MaxZombies = 24\n','MM.CaveRange = 1000\nMM.CryptRange = 750\nMM.MaxZombies = 24\n')
rep('''		range = self.zoom or MM.Range
	end
''','''		range = self.zoom or MM.Range
		-- closer inside a cave, with a short glide
		if self.part == 2 then
			range = math.min(range, MM.CryptRange)
		elseif MM.Under[self.part] then
			range = math.min(range, MM.CaveRange)
		end
		self.range = (self.range or range) + (range - (self.range or range)) * 0.06
		if math.abs(self.range - range) < 2 then
			self.range = range
		end
		range = self.range
	end
''')
rep('\tshow(big.map, crazy and 0 or 1)\n','''	-- on a lower floor: dim the surface and light only that structure
	local part = not crazy and MM.Under[self.part] and self.part or 0
	show(big.map, (crazy and 0) or (part > 0 and 0.3) or 1)
	for i = 1, #big.caveBox do
		local a = 0
		if part > 0 then
			a = (i == part) and 1 or 0
		elseif i >= 3 and i <= 6 then
			a = 0.9
		end
		show(big.caveBox[i], a)
	end
''')
rep('\tbig.caves = group(big, frame, 1)\n','\tbig.caves = group(big, frame, 1)\n\tbig.caveBox = {}\n')
rep('MM.UnderWorld * bk, 1, 1, 1, 0.9)','MM.UnderWorld * bk, 1, 1, 1, 1)\n\t\tbig.caveBox[i] = img')
rep('{ 0, -370, "MID - EXCAVACION" }','{ 0, -760, "MID - EXCAVACION" }')
rep('	{ "FUEGO", 1, 0.4, 0.25 },','	{ "CRIPTA", 0.3, 0.95, 0.8 }, { "CRAZY", 0.85, 0.65, 1 }, { "FUEGO", 1, 0.4, 0.25 },')
t=re.sub('--.*','',re.sub('"[^"]*"','',s))
assert len(re.findall(r'\b(function|if|do)\b',t))==len(re.findall(r'\bend\b',t)),'bloques'
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1])
R=T+'/respaldo_hud/zm_minimapa_v13';assert not os.path.exists(R);shutil.copytree(M,R)
for p in(M,T):
    with open(p+'/images/hud_zombierank_5.iwi','wb') as fh:fh.write(iwi)
with open(lp,'w',newline='') as fh:fh.write(s)
print('instalado',boxes)
