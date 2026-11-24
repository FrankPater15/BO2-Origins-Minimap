import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from layers import *
import json,struct,io
from PIL import Image
N=4096
XF=dict(main=(128.0,808.0,10000.0),crazy=(10464.0,-7788.0,2700.0))
def tf(name):
    cx,cy,s=XF[name]
    return lambda p:np.c_[(p[:,0]-cx)/s*N+N/2,N/2-(p[:,1]-cy)/s*N]
def comps(L):
    n=len(L);lab=-np.ones(n,int);k=0
    for i in range(n):
        if lab[i]<0:
            st=[i];lab[i]=k
            while st:
                q=st.pop()
                for j in np.where(L[q]&(lab<0))[0]:lab[j]=k;st.append(j)
            k+=1
    return lab
def segments(p,tol=7,gap=62,minlen=70):
    """greedy straight-line extraction over ray-hit points"""
    out=[];used=np.zeros(len(p),bool);cell={}
    for i,q in enumerate(p):cell.setdefault((int(q[0]//130),int(q[1]//130)),[]).append(i)
    nb=lambda q:np.array([i for dx in(-1,0,1) for dy in(-1,0,1) for i in cell.get((int(q[0]//130)+dx,int(q[1]//130)+dy),[])])
    ths=np.arange(0,180,3)*np.pi/180;U=np.c_[np.cos(ths),np.sin(ths)]
    best=np.zeros(len(p));bt=np.zeros(len(p))
    for i in range(len(p)):
        m=p[nb(p[i])]-p[i];m=m[np.hypot(*m.T)<130]
        c=(abs(m[:,0:1]*U[:,1]-m[:,1:2]*U[:,0])<tol).sum(0);j=c.argmax();best[i]=c[j];bt[i]=ths[j]
    for i in np.argsort(-best):
        if used[i] or best[i]<4:continue
        o=p[i].copy();u=np.array([np.cos(bt[i]),np.sin(bt[i])]);sel=[]
        for it in range(3):
            v=p-o;t=v@u;ok=np.where((abs(v[:,0]*u[1]-v[:,1]*u[0])<tol)&~used)[0]
            if len(ok)<4:sel=[];break
            ok=ok[np.argsort(t[ok])];tt=t[ok];k=min(np.searchsorted(tt,0),len(tt)-1)
            br=np.where(np.diff(tt)>gap)[0];a0=br[br<k];b0=br[br>=k]
            sel=ok[(a0[-1]+1 if len(a0) else 0):(b0[0]+1 if len(b0) else len(ok))]
            if len(sel)<4:break
            q=p[sel];o=q.mean(0);u=np.linalg.svd(q-o,full_matrices=False)[2][0]
        if len(sel)<4:continue
        t=(p[sel]-o)@u;ln=np.ptp(t)
        if ln<minlen or len(sel)<ln/34:continue
        used[sel]=True;out.append((o+u*t.min(),o+u*t.max()))
    return np.array(out).reshape(-1,2,2)
def hits(a,lim=420):
    th=np.arange(24)*np.pi/12;d=a[:,3:];ok=(d<lim)&(d>12)
    x=a[:,:1]+d*np.cos(th);y=a[:,1:2]+d*np.sin(th)
    return np.c_[x[ok],y[ok]]
def dedupe(seg):
    keep=[]
    for s in sorted(seg,key=lambda s:-np.hypot(*(s[1]-s[0]))):
        u=(s[1]-s[0])/np.hypot(*(s[1]-s[0]));dup=False
        for k in keep:
            ku=k[1]-k[0];kl=np.hypot(*ku);ku=ku/kl
            if abs(ku@u)>.985:
                v=s-k[0];t=v@ku;n=abs(v[:,0]*ku[1]-v[:,1]*ku[0])
                if n.max()<22 and t.min()>-25 and t.max()<kl+25:dup=True;break
        if not dup:keep.append(s)
    return np.array(keep).reshape(-1,2,2)
def line(m,q,w,aa=cv2.LINE_8):
    q=np.round(q).astype(int);cv2.line(m,tuple(map(int,q[0])),tuple(map(int,q[1])),255,max(1,int(w)),aa)
def floor(a,L,D,seg,T,scale):
    n=len(a);m=np.zeros((N,N),np.uint8)
    poly=lambda pts:cv2.fillPoly(m,[np.round(T(pts)*16).astype(np.int32)],255,cv2.LINE_8,4)
    th=np.arange(24)*np.pi/12
    for i in range(n):
        ne=np.where(L[i])[0];ne=ne[ne>i]
        for x in range(len(ne)):
            for y in ne[x+1:]:
                if L[ne[x],y]:poly(a[[i,ne[x],y],:2])
        d=a[i,3:];r=np.where(d<230,d,64)
        for k in range(24):
            j=(k+1)%24;e=th[k]+np.pi/12;p,q=d[k],d[j]
            if p<230 and q<230 and abs(p-q)<max(45,.45*min(p,q)):v0,v1=p,q
            else:v0=v1=min(r[k],r[j])
            poly(np.array([[a[i,0],a[i,1]],[a[i,0]+v0*np.cos(th[k]),a[i,1]+v0*np.sin(th[k])],[a[i,0]+v1*np.cos(e),a[i,1]+v1*np.sin(e)]]))
        for j in ne:line(m,T(a[[i,j],:2]),90*scale)
    k=lambda w:cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(w*scale)|1,)*2)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k(44));m=cv2.morphologyEx(m,cv2.MORPH_OPEN,k(36))
    cut=np.zeros_like(m)
    for s in seg:line(cut,T(s),9*scale)
    # a node-to-node link proves an opening: never carve a wall across it
    for i,j in zip(*np.where(np.triu(L)&(D<150))):cv2.line(cut,*[tuple(map(int,q)) for q in np.round(T(a[[i,j],:2]))],0,int(60*scale))
    m[cut>0]=0
    out=np.zeros_like(m);cs,h=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE);polys=[]
    for c,hh in zip(cs,h[0]):
        hole=hh[3]>=0
        if cv2.contourArea(c)/scale**2<(2500 if hole else 9000):continue
        polys.append((hole,cv2.approxPolyDP(c,13*scale,True)))
    for hole,c in polys:
        if not hole:cv2.fillPoly(out,[c],255)
    for hole,c in polys:
        if hole:cv2.fillPoly(out,[c],0)
    return out
def zfield(a,T):
    p=T(a[:,:2])/8;yy,xx=np.mgrid[:512,:512]+.5;num=np.zeros((512,512));den=num+1e-300
    for (x,y),z in zip(p,a[:,2]):
        w=np.exp(-((xx-x)**2+(yy-y)**2)/(2*9));num+=w*z;den+=w
    return cv2.resize((num/den).astype(np.float32),(N,N),interpolation=cv2.INTER_LINEAR)
def layer(a,name):
    T=tf(name);scale=N/XF[name][2];L,D,dz=links(a);lab=comps(L);ok=np.bincount(lab)[lab]>=3
    drop=a[~ok];a=a[ok];L=L[ok][:,ok];D=D[ok][:,ok]
    z=a[:,2];cv=((D<130)&(z[None]-z[:,None]>100)).any(1)
    p=hits(a[~cv]);seg=dedupe(segments(p));m=floor(a,L,D,seg,T,scale)
    near=cv2.dilate(m,np.ones((int(26*scale)|1,)*2,np.uint8));wl=np.zeros_like(m)
    for s in seg:line(wl,T(s),10*scale)
    raw=wl.copy();wl[near==0]=0
    # a wall cannot cross a walkable link: erase there, then keep remnants on the floor edge or long enough inside
    for i,j in zip(*np.where(np.triu(L))):cv2.line(wl,*[tuple(map(int,q)) for q in np.round(T(a[[i,j],:2]))],0,max(1,int(30*scale)))
    edge=cv2.morphologyEx(m,cv2.MORPH_GRADIENT,np.ones((int(14*scale)|1,)*2,np.uint8))>0
    nc,lab2,st,_=cv2.connectedComponentsWithStats(wl,connectivity=8)
    big=np.hypot(st[:,2],st[:,3])>150*scale;big[0]=False
    wl=np.where(edge|big[lab2],wl,0).astype(np.uint8);wl[edge&(raw==0)]=0
    # final trim: no specks under 60 units
    nc,lab2,st,_=cv2.connectedComponentsWithStats(wl,connectivity=8);sm=np.hypot(st[:,2],st[:,3])<60*scale;wl[sm[lab2]]=0
    wl=cv2.GaussianBlur(wl,(0,0),.8)
    print(name,'nodes',len(a),'dropped',len(drop),'hits',len(p),'segs',len(seg),flush=True)
    return dict(m=m,w=wl,raw=raw,z=zfield(a,T),nodes=a,scale=scale)
def ramp(z,stops):
    zs=[s[0] for s in stops];return np.stack([np.interp(z,zs,[s[1][c] for s in stops]) for c in range(3)],-1)
def over(base,rgb,al):
    al=al.astype(np.float32)[...,None];rgb=np.asarray(rgb,np.float32);b,ba=base[...,:3],base[...,3:]
    o=al+ba*(1-al);base[...,:3]=(rgb*al+b*ba*(1-al))/np.maximum(o,1e-6);base[...,3:]=o
def bg(al=.62):
    b=np.zeros((N,N,4),np.float32);b[...,:3]=(10,15,21);b[...,3]=al;return b
SURF=[(-450,(72,98,112)),(-250,(92,122,130)),(0,(122,146,142)),(200,(160,170,150)),(400,(200,198,168))]
UND=[(-750,(62,34,30)),(-400,(112,60,36)),(-100,(150,86,42)),(150,(184,118,58))]
F=lambda x:x.astype(np.float32)/255
def paint(b,l,stops,fa,edge,wallc):
    m=l['m'];s=l['scale']
    over(b,(0,0,0),F(cv2.GaussianBlur(cv2.dilate(m,np.ones((int(24*s)|1,)*2,np.uint8)),(0,0),16*s))*.55)
    over(b,ramp(l['z'],stops),F(cv2.GaussianBlur(m,(0,0),1.1))*fa)
    over(b,(0,0,0),F(cv2.GaussianBlur(255-m,(0,0),13*s))*.55*(m>0))
    w=max(3,int(13*s))
    o=F(cv2.GaussianBlur(cv2.subtract(cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(w*2+1,)*2)),m),(0,0),1.1))
    real=cv2.dilate(l['raw'],np.ones((int(46*s)|1,)*2,np.uint8))>0
    over(b,edge,o*np.where(real,0,.55));over(b,wallc,o*np.where(real,.98,0));over(b,wallc,F(l['w'])*.95)
def save(b,name):
    im=Image.fromarray(np.clip(np.dstack([b[...,:3],b[...,3]*255])+.5,0,255).astype(np.uint8),'RGBA')
    im.save(f'{B}/{name}_4096.png');h=open(B+'/../mm/icon_twitter.iwi','rb').read()[:64]
    im.resize((2048,)*2,Image.LANCZOS).save(f'{B}/{name}_2048.png')
    for n in(512,1024):
        q=im.resize((n,n),Image.LANCZOS);q.save(f'{B}/{name}_{n}.png')
        e=io.BytesIO();q.save(e,'DDS',pixel_format='DXT5');d=e.getvalue();assert d[84:88]==b'DXT5'
        body=d[128:128+n*n];assert len(body)==n*n;hd=bytearray(h)
        if n==1024:
            # offset 6/8 = u16 width/height; 0x20 = file size; 0x24..0x3c repeat payload size (as in the 512 reference)
            struct.pack_into('<HH',hd,6,n,n);struct.pack_into('<I',hd,0x20,64+n*n)
            for o in range(0x24,0x40,4):struct.pack_into('<I',hd,o,n*n)
        out=bytes(hd)+body;assert len(out)==struct.unpack_from('<I',hd,0x20)[0] and struct.unpack_from('<HH',hd,6)==(n,n)
        open(f'{B}/{name}_{n}.iwi','wb').write(out)
def test(nodes,m,name):
    p=tf(name)(nodes[:,:2]);cx,cy,s=XF[name]
    back=np.c_[(p[:,0]-N/2)*s/N+cx,(N/2-p[:,1])*s/N+cy];err=abs(back-nodes[:,:2]).max()
    i=np.clip(p.astype(int),0,N-1);return float((m[i[:,1],i[:,0]]>0).mean()*100),float(err),int(((p<0)|(p>=N)).any(1).sum())
def main():
    a,c=load();L,D,_=links(a);g=ground(a)
    g=np.where(a[:,1]<1500,np.maximum(g,90),g);rel=a[:,2]-g
    u=rel<-120;grow=rel<-75          # hysteresis along walkable links
    for _ in range(30):u=u|(grow&(L&u[None,:]).any(1))
    for _ in range(2):               # isolated flips take the neighbours' label
        s=L@u.astype(int);n=L.sum(1);u=np.where((n>2)&(s>=.8*n),True,np.where((n>2)&(s<=.2*n),False,u))
    print('surface',(~u).sum(),a[~u,2].min(),a[~u,2].max(),'under',u.sum(),a[u,2].min(),a[u,2].max(),flush=True)
    Su,Un,Cr=layer(a[~u],'main'),layer(a[u],'main'),layer(c,'crazy')
    SC=((150,165,170),(238,244,246));UC=((190,140,90),(255,206,140))
    b=bg();paint(b,Su,SURF,.93,*SC);save(b,'surface')
    b=bg();paint(b,Un,UND,.95,*UC);save(b,'underground')
    paint(b,Su,SURF,.93,*SC);s=Su['scale']
    hid=F(cv2.bitwise_and(Un['m'],Su['m']));over(b,(196,104,36),cv2.GaussianBlur(hid,(0,0),1)*.30)
    ol=F(cv2.morphologyEx(Un['m'],cv2.MORPH_GRADIENT,np.ones((int(13*s)|1,)*2,np.uint8)))
    over(b,(224,128,44),cv2.GaussianBlur(ol,(0,0),1)*(Su['m']>0)*.85);save(b,'combined')
    b=bg();paint(b,Cr,[(-463,(84,70,120)),(-240,(128,108,158)),(-15,(186,166,206))],.93,(160,150,180),(244,238,252));save(b,'crazyplace')
    rep={};U_=Su['m']|Un['m'];im={}
    for k,n,m,nm in(('surface',a[~u],Su['m'],'main'),('underground',a[u],Un['m'],'main'),('combined',a,U_,'main'),('crazyplace',c,Cr['m'],'crazy')):
        r=test(n,m,nm);v=dict(nodes=len(n),pct_nodes_on_floor=round(r[0],2),roundtrip_max_err_units=r[1],nodes_outside_image=r[2])
        for q in(512,1024):
            mm=cv2.resize(m,(q,q),interpolation=cv2.INTER_AREA)>127;i=(tf(nm)(n[:,:2])*q/N).astype(int);v[f'pct_on_floor_{q}']=round(float(mm[i[:,1],i[:,0]].mean()*100),2)
        print(k,v);cx,cy,s=XF[nm];im[k]=dict(center=[cx,cy],span=s,units_per_px={str(q):s/q for q in(512,1024,2048,4096)},verify=v)
    print('kept-only pct',[round(test(l['nodes'],l['m'],nm)[0],2) for l,nm in((Su,'main'),(Un,'main'),(Cr,'crazy'))])
    ys,xs=np.where(U_>0);print('bbox px',xs.min(),xs.max(),ys.min(),ys.max())
    json.dump(dict(formula='px=(x-cx)/span*N+N/2; py=N/2-(y-cy)/span*N; inverse x=(px-N/2)*span/N+cx; y=(N/2-py)*span/N+cy. N=image size, origin top-left pixel edge, +Y up, +X right',images=im),open(B+'/transforms.json','w'),indent=1)
main()
