import sys; sys.path.insert(0,'../agent_map/_lib'); sys.path.insert(0,'../agent_map')
import numpy as np, cv2, layers
from PIL import Image, ImageDraw, ImageFont
N=2048
def labels(a):
    from layers import links,ground
    L,D,_=links(a);g=ground(a);g=np.where(a[:,1]<1500,np.maximum(g,90),g);rel=a[:,2]-g
    u=rel<-120;grow=rel<-75
    for _ in range(30):u=u|(grow&(L&u[None,:]).any(1))
    for _ in range(2):
        s=L@u.astype(int);n=L.sum(1);u=np.where((n>2)&(s>=.8*n),True,np.where((n>2)&(s<=.2*n),False,u))
    return u
def layer(name,sel_nodes,lab,want,maskfile,x0,Z0,SP,C):
    pts=np.load(f'reach_{name}.npy').astype(int); U=SP/N
    wx=C[0]+((pts[:,1]+x0+.5)/N-.5)*SP; wy=C[1]-((pts[:,0]+.5)/N-.5)*SP; wz=Z0+pts[:,2]*12
    near=np.zeros(len(pts),int); a=sel_nodes
    for i in range(0,len(pts),20000):
        s=slice(i,i+20000)
        near[s]=(((wx[s,None]-a[None,:,0])**2+(wy[s,None]-a[None,:,1])**2+(3*(wz[s,None]-a[None,:,2]))**2).argmin(1))
    k=lab[near]==want
    z=np.full((N,N),-9999.,np.float32); np.maximum.at(z,(pts[k,0],pts[k,1]+x0),wz[k].astype(np.float32))
    im=np.array(Image.open(f'../agent_map/{maskfile}_2048.png').convert('RGBA')).astype(int)
    scan=(np.abs(im[...,:3]-im[2,2,:3]).max(2)>60).astype(np.uint8)
    scan=cv2.morphologyEx(scan,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    r=int((18 if name=="main" else 10)/U)|1
    allow=cv2.dilate(scan,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,)*2))
    m=((z>-9000)&(allow>0)).astype(np.uint8)
    # scanned spots the geometry could not seed (props, steep mud)
    miss=np.load(f'miss_{name}.npy'); disk=np.zeros_like(m)
    for x,y in a[miss&(lab==want),:2]:
        cv2.circle(disk,(int((x-C[0])/SP*N+N/2),int(N/2-(y-C[1])/SP*N)),int(75/U),1,-1)
    m|=disk&scan
    L,D,_=layers.links(a); w0=lab==want; P=lambda p:(int((p[0]-C[0])/SP*N+N/2),int(N/2-(p[1]-C[1])/SP*N))
    for i,j in zip(*np.where(np.triu(L)&w0[:,None]&w0[None]&(D<170))): cv2.line(m,P(a[i]),P(a[j]),1,max(2,int(62/U)))
    s=40/9.77*2/ (U*2/9.77) if 0 else 1
    q=max(3,int(16/U)|1)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(q,q)))
    nc,l,st,_=cv2.connectedComponentsWithStats(m,connectivity=4); bad=st[:,4]*U*U<14000;bad[0]=False;m[bad[l]]=0
    nc,l,st,_=cv2.connectedComponentsWithStats(1-m,connectivity=8); bad=st[:,4]*U*U<1600;bad[0]=False;m[bad[l]]=1
    # smooth outline
    b=cv2.GaussianBlur(m.astype(np.float32),(0,0),9/U); m=(b>.5).astype(np.uint8)
    b=cv2.GaussianBlur(m.astype(np.float32),(0,0),7/U); m=(b>.5).astype(np.uint8)
    ok=(z>-9000).astype(np.float32); zz=np.where(z>-9000,z,0)
    num=cv2.GaussianBlur(zz*ok,(0,0),12/U);den=cv2.GaussianBlur(ok,(0,0),12/U)
    n2=cv2.GaussianBlur(zz*ok,(0,0),90/U);d2=cv2.GaussianBlur(ok,(0,0),90/U)
    zf=np.where(den>.05,num/np.maximum(den,1e-6),n2/np.maximum(d2,1e-6))
    return m,zf,U
def over(b,rgb,al):
    al=np.broadcast_to(al,b.shape[:2])[...,None].astype(np.float32);rgb=np.asarray(rgb,np.float32);ba=b[...,3:]
    o=al+ba*(1-al);b[...,:3]=(rgb*al+b[...,:3]*ba*(1-al))/np.maximum(o,1e-6);b[...,3:]=o
def ramp(z,st): return np.stack([np.interp(z,[s[0] for s in st],[s[1][c] for s in st]) for c in range(3)],-1)
def paint(m,z,U,stops,line,al=.97):
    b=np.zeros((N,N,4),np.float32); f=m.astype(np.float32)
    # wall thickness: dark rim outside, then bright line
    sh=cv2.GaussianBlur(cv2.dilate(m,np.ones((int(40/U)|1,)*2,np.uint8)).astype(np.float32),(0,0),16/U)
    over(b,(0,0,0),sh*.6)
    gx=cv2.Sobel(z,cv2.CV_32F,1,0,ksize=3)/8/U;gy=cv2.Sobel(z,cv2.CV_32F,0,1,ksize=3)/8/U
    hs=np.clip(1+(gx*.55+gy*.55)*.9,.62,1.32)
    rng=np.random.default_rng(3);gr=cv2.GaussianBlur(rng.normal(0,1,(N,N)).astype(np.float32),(0,0),22/U);gr/=gr.std()
    col=np.clip(ramp(z,stops)*(hs*(1+.035*gr))[...,None],0,255)
    over(b,col,cv2.GaussianBlur(f,(0,0),.8)*al)
    inn=cv2.GaussianBlur(1-f,(0,0),22/U); over(b,(0,0,0),np.clip(inn*1.0,0,.6)*f)
    w=int(round(13/U))|1
    ed=cv2.subtract(cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*w-1,)*2)),m).astype(np.float32)
    # thin walls must stay readable: drop tiny outline fragments
    over(b,line,cv2.GaussianBlur(ed,(0,0),.7)*.92)
    return b
def img(b): return Image.fromarray(np.clip(np.dstack([b[...,:3],b[...,3]*255])+.5,0,255).astype(np.uint8),'RGBA')
a=np.load('nodes_main.npy');lab=labels(a).astype(int);c=np.load('nodes_crazy.npy')
SURF=[(-450,(58,84,100)),(-250,(80,110,120)),(0,(112,132,122)),(200,(146,148,116)),(400,(184,172,128))]
UND=[(-750,(80,40,32)),(-400,(126,66,38)),(-100,(168,94,44)),(150,(198,126,62))]
CR=[(-463,(84,70,120)),(-240,(128,108,158)),(-15,(186,166,206))]
A=('main',a,lab)
s=layer('main',a,lab,0,'surface',360,-820,10000.,(128,808)); u=layer('main',a,lab,1,'underground',360,-820,10000.,(128,808))
k=layer('crazy',c,np.zeros(len(c),int),0,'crazyplace',0,-700,2700.,(10464,-7788))
img(paint(*s,SURF,(226,232,226))).save('surf11.png'); img(paint(*u,UND,(255,214,150))).save('und11.png'); img(paint(*k,CR,(238,230,248))).save('crazy11.png')
np.save('um.npy',u[0]);np.save('sm.npy',s[0])
bg=Image.new('RGBA',(N,N),(14,19,24,255))
for n in('surf','und','crazy'):
    t=bg.copy();t.alpha_composite(Image.open(n+'11.png'));t.resize((1200,1200),Image.LANCZOS).save(n+'11v.png')

for nm,(m,z,U),nd,C,SP in(('surf',s,a[lab==0],(128,808),10000),('und',u,a[lab==1],(128,808),10000),('crazy',k,c,(10464,-7788),2700)):
    X=((nd[:,0]-C[0])/SP*N+N/2).astype(int);Y=(N/2-(nd[:,1]-C[1])/SP*N).astype(int);print(nm,'nodes on floor %',round(float(m[Y,X].mean()*100),2))
