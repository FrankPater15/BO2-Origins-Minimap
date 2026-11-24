"""v23: structures redone (lab/G1, church floors, crypt ring, clean caves) and full-map labels with pointers"""
import sys,io,os,re,struct,shutil
S,T=sys.argv[1:3];go=len(sys.argv)>3;M=T+'/mods/zm_minimapa';Q=S+'/mm/';G=os.path.dirname(os.path.abspath(__file__))+'/';DOC=G+'../'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
ns={'__name__':'arte'};exec(compile(open(G+'arte.py',encoding='utf8').read(),'arte','exec'),ns)
def mydraw(im,tr,items,r):
    for x,y,t,c in items:
        X,Y=tr(x,y);sz=int(r*2.75);a=(ns['staff'](c) if t=='staff' else ns['portal'](c)).out(256).resize((sz,sz),Image.LANCZOS)
        im.alpha_composite(a,(int(round(X-sz/2)),int(round(Y-sz/2))))
v=open(G+'v15.py',encoding='utf8').read()
def V(a,b,n=1):
    global v
    assert v.count(a)==n,(v.count(a),a);v=v.replace(a,b)
v=v[:v.index("if len(sys.argv)<4:")]
V("N=2048;U=10000/N\n","N=2048;U=10000/N\ndraw=MYDRAW\n")
V("draw(t,tr,[(0,-480,'K',(120,255,170))],15);","")
V("part[c&nr&(o==4)&(wy>-2560)]=4","part[c&nr&(o==4)&(wy>-2560)&~((wx<1340)&(wy<-2290))&(wy>-2575)]=4")
# numbering: 6 church top, 7 church bottom, 8 lab, 9 G1, then the rest; 17 = upper crypt
V("part[rest]=lab[Y[rest],X[rest]]\nNP=5+len(big)","""raw=lab[Y[rest],X[rest]]
cen={6+i:(128+(ce[k][0]-1024)*U,808-(ce[k][1]-1024)*U) for i,k in enumerate(big)}
def near_(p,a,b):return abs(cen[p][0]-a)<200 and abs(cen[p][1]-b)<200
new=np.zeros(len(raw),int);nx=10;NAME={}
rx,ry,rz=wx[rest],wy[rest],wz[rest]
for p in cen:
    k=raw==p
    if near_(p,516,-2626):new[k&(rz>=230)]=6;new[k&(rz<230)]=7
    elif near_(p,2452,4925):
        L_=(ry>4985)&(rx>2420);new[k&L_]=8;new[k&~L_]=9
    elif near_(p,619,1894):pass
    else:new[k]=nx;NAME[nx]=cen[p];nx+=1
part[rest]=new
NP=nx;print('partes',NP,NAME);assert NP==17""")
V("    k=part==p;z=np.full(","    if p==17:return upper()\n    k=part==p;z=np.full(")
V("    mm=(z>-9000).astype(np.uint8);mm=cv2.morphologyEx(mm","""    mm=(z>-9000).astype(np.uint8)
    if p==4:
        fx,fy=int(tr(1345,0)[0]),int(tr(0,-2280)[1]);mm[fy:,:fx]=0;z[fy:,:fx]=-9999
    if p==1:
        # complete the lower crypt with the scanned outline
        old=cv2.resize(((owner==1)&mb).astype(np.uint8),(N,N),interpolation=cv2.INTER_NEAREST);d_,lb=cv2.distanceTransformWithLabels(1-mm,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
        vv=np.zeros(lb.max()+1,np.float32);a_,b_=np.where(mm>0);vv[lb[a_,b_]]=z[a_,b_];f_=(old>0)&(mm==0);z=np.where(f_,vv[lb],z).astype(np.float32);mm|=old
    if p==1:mm=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
    mm=cv2.morphologyEx(mm""")
V("def tile(p):","""def shade(mm,zf,c):
    gy,gx=np.gradient(zf);sh=np.clip((gx+gy)*-.02,-.2,.2);q=zf[mm>0];lo,hi=q.min(),q.max();br=.62+.38*np.clip((zf-lo)/max(60,hi-lo),0,1)+sh
    out=np.array(c,np.float32)[None,None]*np.clip(br,.3,1.15)[...,None];aa=cv2.GaussianBlur(mm,(0,0),.8)
    edge=np.clip(cv2.dilate(aa,np.ones((5,5)))-cv2.erode(aa,np.ones((3,3))),0,1)[...,None];out=out*(1-edge*.75)+(np.array(c)*.45+140)*edge*.75
    return np.dstack([np.clip(out,0,255),np.clip(cv2.dilate(aa,np.ones((5,5))),0,1)*255]).astype(np.uint8)
def upper():
    # upper crypt floor: the geometry lacks it, so it comes from the scanned path nodes
    n_=np.load(Q+'nodes_main.npy');n_=n_[(np.hypot(n_[:,0],n_[:,1])<480)&(n_[:,2]>0)&(n_[:,2]<250)]
    mm=np.zeros((N,N),np.uint8);P=[tuple(int(round(q)) for q in tr(x,y)) for x,y in n_[:,:2]]
    for i in range(len(P)):
        cv2.circle(mm,P[i],int(62/U),1,-1)
        for j in range(i):
            if np.hypot(*(n_[i,:2]-n_[j,:2]))<185 and abs(n_[i,2]-n_[j,2])<75:cv2.line(mm,P[i],P[j],1,int(105/U))
    mm=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)));mm=(cv2.GaussianBlur(mm.astype(np.float32),(0,0),4)>.5).astype(np.float32)
    yy,xx=np.mgrid[0:N,0:N];s_=(np.abs(yy-tr(0,0)[1])<140)&(np.abs(xx-tr(0,0)[0])<140);zf=np.zeros((N,N),np.float32)
    w=np.zeros(s_.sum());a=np.zeros(s_.sum())
    for (px,py),h in zip(P,n_[:,2]):
        k=1/((xx[s_]-px)**2+(yy[s_]-py)**2+30.)**1.5;w+=k;a+=k*h
    zf[s_]=a/w;return shade(mm,zf,(120,240,215))
def tile(p):""")
V("    out[:,int(tr(-2850,0)[0]):]=0\n","""    # soften the join with the farm and remove the stray line
    e_=int(tr(-2850,0)[0]);out[:,e_:]=0;al=out[...,3].astype(np.float32)
    al[:,e_-16:e_]*=np.linspace(1,0,16)[None];med=cv2.medianBlur(np.ascontiguousarray(out[...,:3]),13);inn=cv2.erode((out[...,3]>200).astype(np.uint8),np.ones((11,11)))>0
    out[inn,:3]=med[inn];out[...,3]=al.astype(np.uint8)
""")
# the upper crypt uses no reach points, so its box and cells are handled apart
V("G+'atlas15_%d.png'","G+'atlas23_%d.png'")
v=v.replace("k=part==q;print(q,'bien","k=part==q\n    if k.any():print(q,'bien")
v=v.replace("N=2048;U=10000/N\n","N=2048;U=10000/N\n",1)
ar=sys.argv;sys.argv=['x',S,T];n15={'__file__':__file__,'MYDRAW':mydraw};exec(compile(v,'v15','exec'),n15);sys.argv=ar
A,tiles,boxes,cells,tc,NP=[n15[k] for k in('A','tiles','boxes','cells','tc','NP')]
N=2048
# Crazy Place with the current icons
old=np.array(Image.open(G+'atlas20_1.png').convert('RGBA'));x,y=tc(8);A[0][y-340:y+340,x-340:x+340]=old[y-340:y+340,x-340:x+340]
Image.fromarray(A[0]).save(G+'atlas23_1.png')
# preview
pv=Image.new('RGBA',(N,N),(8,11,15,255));bs=Image.open(G+'base21.png').resize((N,N));bs.putalpha(bs.getchannel('A').point(lambda q:int(q*.35)));pv.alpha_composite(bs)
for p in list(range(NP,0,-1)):
    if p in(17,7):continue
    pv.alpha_composite(Image.fromarray(n15['tile'](p) if p!=2 else n15['rayo']()))
side=Image.new('RGBA',(1500,700),(8,11,15,255));d=ImageDraw.Draw(side);f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',28)
for i,(p,t) in enumerate(((1,'CRIPTA (abajo)'),(17,'CRIPTA (arriba)'),(6,'IGLESIA (arriba)'),(7,'IGLESIA (abajo)'),(8,'LABORATORIO'),(9,'G1'),(2,'RAYO'),(4,'HIELO'))):
    b=boxes[p-1];X0,Y0=n15['tr'](b[0],b[3]);X1,Y1=n15['tr'](b[1],b[2]);c=Image.fromarray(n15['tile'](p) if p!=2 else n15['rayo']()).crop((int(X0)-4,int(Y0)-4,int(X1)+4,int(Y1)+4));z=min(290/c.width,270/c.height);c=c.resize((int(c.width*z),int(c.height*z)),Image.LANCZOS)
    px,py=40+(i%4)*365,30+(i//4)*340;side.alpha_composite(c,(px,py));d.text((px+140,py+292),t,font=f,fill='white',anchor='mm')
side.convert('RGB').save(DOC+'zonas_v23.png');pv.crop((340,0,1760,N)).convert('RGB').resize((1065,1536)).save(DOC+'techos_v23.png')
# ---- GSC
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';g=open(gp,newline='').read();s=open(lp,newline='').read()
i=g.index('mml_cells_setup()\n{');j=g.index('mml_inside( org )')
rows=[';'.join('%d,%d,%d,%d'%c for c in cells[k:k+25]) for k in range(0,len(cells),25)]
g=g[:i]+'mml_cells_setup()\n{\n'+''.join('\tmml_row( "%s" );\n'%r for r in rows)+'}\n\n'+g[j:]
def RG(a,b):
    global g
    assert g.count(a)==1,(g.count(a),a);g=g.replace(a,b)
RG('org[ 1 ] * org[ 1 ] < 230400 )\n\t\treturn 1;','org[ 1 ] * org[ 1 ] < 230400 )\n\t{\n\t\tif ( org[ 2 ] > 0 )\n\t\t\treturn 17;\n\t\treturn 1;\n\t}')
RG('\t\tcase 1:\n\t\t\treturn "CRIPTA";','\t\tcase 1:\n\t\t\treturn "CRIPTA";\n\t\tcase 17:\n\t\t\treturn "CRIPTA";')
# ---- Lua
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a);s=s.replace(a,b)
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.Under = {\n'+''.join('\t{ %.1f, %.1f, %d },\n'%t for t in tiles)+'}\n'+s[j:]
i=s.index('MM.BigCaves = {');j=s.index('MM.BigLabels');s=s[:i]+'MM.BigCaves = {\n'+''.join('\t{ %d, %d, %d, %d, %d },\n'%((q+1,)+tuple(bx)) for q,bx in enumerate(boxes))+'}\n'+s[j:]
R('if self.part == 1 then\n\t\t\trange','if self.part == 1 or self.part == 17 then\n\t\t\trange')
R('part ~= 1) then','part ~= 1 and part ~= 17) then')
C=(1,.95,.8)
LB=[(1500,5600,'LABORATORIO',C,(2450,5350)),(0,5120,'ESTACION DEL TANQUE',C,None),(-3000,3700,'BUNKER DEL TANQUE - G2',C,(-620,3400)),(400,1700,'TRINCHERA CENTRAL - G3',C,(480,2150)),(3700,3400,'TRINCHERAS',C,(2650,3080)),
 (400,1400,'TIERRA DE NADIE',C,(250,1010)),(620,-430,'MID - EXCAVACION',C,(120,-120)),(3850,-800,'ZONA DE JUGGERNOG - G4',C,(2950,-420)),(-2750,1150,'GRANJA - G5',C,None),(-2400,-1900,'ALDEA',C,(-750,-2420)),
 (-1900,-3300,'ESTACION DEL TANQUE',C,(230,-2960)),(2900,-2700,'IGLESIA',C,(720,-2620)),(2700,-3900,'DETRAS DE LA IGLESIA - G6',C,(1180,-3820)),
 (3930,4450,'CUEVA DE FUEGO',(1,.4,.25),None),(3350,1780,'CUEVA DE VIENTO',(.95,.9,.5),None),(-3250,-850,'CUEVA DE RAYO',(.8,.5,1),None),(2340,-1900,'CUEVA DE HIELO',(.4,.8,1),None)]
i=s.index('MM.BigLabels = {');j=s.index('\n}\n',i)+3
s=s[:i]+'-- x, y, name, colour, place it points to\nMM.BigLabels = {\n'+''.join('\t{ %d, %d, "%s", %g, %g, %g%s },\n'%((a,b,t)+c+((', %d, %d'%p) if p else '',)) for a,b,t,c,p in LB)+'}\n'+s[j:]
R('\t\tlocal w = string.len(d[3]) * 2.7 + 4\n','''		local w = string.len(d[3]) * 2.7 + 4
		if d[7] then
			-- pointer: a thin bar turned towards the place, with a dot at its end
			local mk = MM.BigSize / MM.World
			local x1, y1 = (d[1] - MM.CenterX) * mk, (MM.CenterY - d[2]) * mk
			local x2, y2 = (d[7] - MM.CenterX) * mk, (MM.CenterY - d[8]) * mk
			local dx, dy = x2 - x1, y2 - y1
			local len = math.sqrt(dx * dx + dy * dy)
			local line = bar(big.labels, (x1 + x2 - len) / 2, (y1 + y2) / 2 - 0.6, (x1 + x2 + len) / 2, (y1 + y2) / 2 + 0.6, d[4], d[5], d[6], 0.75)
			line:setZRot(-math.atan2(dy, dx) * 57.29578)
			local tip = image(big.labels, MM.DotMat, 6, d[4], d[5], d[6], 1)
			place(tip, x2, y2, 3, 0)
		end
''')
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x1,x2=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',x1,x2);assert x1==x2
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1]) and g.count(q[0])==g.count(q[1]),q
open(G+'v23_prev.lua','w',newline='').write(s)
if go:
    def dxt(a,h):
        n=a.shape[0];b=io.BytesIO();Image.fromarray(a).save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5';return h+d[128:128+n*n]
    bk=T+'/respaldo_hud/zm_minimapa_v22';assert not os.path.exists(bk);shutil.copytree(M,bk)
    for f_,a in(('hud_zombierank_5',A[0]),('icon_facebook',A[1])):
        with open(M+'/images/%s.iwi'%f_,'rb') as fh:h=fh.read(64)
        o=dxt(a,h)
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f_,'wb') as fh:fh.write(o)
    for p,q in((lp,s),(gp,g)):
        with open(p,'w',newline='') as fh:fh.write(q)
    print('instalado')
