import sys,itertools,time; sys.path.insert(0,'../agent_map/_lib'); sys.path.insert(0,'../agent_map')
import numpy as np, cv2, layers
np.seterr(all='ignore')
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
B=np.load('B.npy');F=B.view('<f4');V=np.load('V.npy').astype(float);T=np.load('Tr.npy')
name=sys.argv[1]
CX,CY,SP,X0,X1=dict(main=(128,808,10000,360,1740),crazy=(10464,-7788,2700,0,2048))[name]
GEO=int(150/(SP/2048));N=2048;U=SP/N;ZS=12;Z0=-820;NZ=125 if name=='main' else 90
if name=='crazy': Z0=-700
W=X1-X0
xs=CX+((np.arange(X0,X1)+.5)/N-.5)*SP; ys=CY-((np.arange(N)+.5)/N-.5)*SP
sol=np.zeros((N,W,NZ),bool); t0=time.time()
px=lambda x:(x-CX)/SP*N+N/2-X0
py=lambda y:N/2-(y-CY)/SP*N
CUT=int(open('cut.txt').read());pm=0xa629fbe9;used=0
for k in range(len(B)):
    c=int(B[k,3])
    if k>=CUT or not c&0x10001: continue
    lo,hi=F[k,:3].astype(float),F[k,4:7].astype(float)
    a,b=int(np.ceil(px(lo[0])-.5)),int(np.floor(px(hi[0])-.5)); e,f=int(np.ceil(py(hi[1])-.5)),int(np.floor(py(lo[1])-.5))
    if a>b: a=b=int(px((lo[0]+hi[0])/2))
    if e>f: e=f=int(py((lo[1]+hi[1])/2))
    a=max(a,0);b=min(b,W-1);e=max(e,0);f=min(f,N-1)
    if a>b or e>f or lo[2]>Z0+NZ*ZS or hi[2]<Z0: continue
    n=int(B[k,21]); q=540208+120000000+int(B[k,22])-pm
    gx,gy=np.meshgrid(xs[a:b+1],ys[e:f+1]); zl=np.full(gx.shape,lo[2]);zh=np.full(gx.shape,hi[2]);ok=np.ones(gx.shape,bool)
    v=np.frombuffer(d[q:q+12*n].tobytes(),'<f4').reshape(-1,3).astype(float) if n else None
    box=n==8 and all(((np.abs(v[:,i]-lo[i])<.6)|(np.abs(v[:,i]-hi[i])<.6)).all() for i in range(3))
    if n>3 and not box:
        if n>40: v=v[np.linspace(0,n-1,40).astype(int)];n=40
        ii=np.array(list(itertools.combinations(range(n),3)))
        p0=v[ii[:,0]];nn=np.cross(v[ii[:,1]]-p0,v[ii[:,2]]-p0);l=np.linalg.norm(nn,axis=1);g=l>.5;nn=nn[g]/l[g][:,None];p0=p0[g]
        D=nn@v.T-(nn*p0).sum(1)[:,None]
        P=[]
        for s in(1,-1):
            m=(s*D<.6).all(1); P.append(np.c_[s*nn[m],(s*(nn*p0).sum(1))[m]])
        P=np.unique(np.concatenate(P).round(2),axis=0)
        for A,Bn,C,dd in P:
            r=dd+.3-A*gx-Bn*gy
            if C>.02: zh=np.minimum(zh,r/C)
            elif C<-.02: zl=np.maximum(zl,r/C)
            else: ok&=r>-2.5
    ok&=zh>=zl
    z0=np.clip(np.round((zl-Z0)/ZS).astype(int),0,NZ);z1=np.clip(np.round((zh-Z0)/ZS).astype(int),0,NZ)
    z1=np.maximum(z1,np.minimum(z0+1,NZ))
    if not ok.any(): continue
    kz=np.arange(z0[ok].min(),z1[ok].max())
    if len(kz): sol[e:f+1,a:b+1,kz[0]:kz[-1]+1]|=ok[...,None]&(kz>=z0[...,None])&(kz<z1[...,None])
    used+=1
print('brushes',used,time.time()-t0,flush=True)
steep=np.zeros_like(sol)
Q=V[T];nm=np.cross(Q[:,1]-Q[:,0],Q[:,2]-Q[:,0]);ar=np.linalg.norm(nm,axis=1)/2;nz=np.abs(nm[:,2])/np.maximum(2*ar,1e-9)
xl,xh=xs[0]-50,xs[-1]+50
m=(Q[...,0].max(1)>xl)&(Q[...,0].min(1)<xh)&(Q[...,1].max(1)>ys[-1])&(Q[...,1].min(1)<ys[0])&(ar<4e6)
for k in np.flatnonzero(m):
    A,b1,c1=Q[k]; h=U*.6
    nn=int(np.ceil(max(np.linalg.norm(b1-A),np.linalg.norm(c1-A),np.linalg.norm(c1-b1))/h))+1
    i,j=np.meshgrid(np.arange(nn+1),np.arange(nn+1));g=i+j<=nn
    P=A+(i[g]/nn)[:,None]*(b1-A)+(j[g]/nn)[:,None]*(c1-A)
    x=np.floor(px(P[:,0])).astype(int);y=np.floor(py(P[:,1])).astype(int);z=np.floor((P[:,2]-Z0)/ZS-.5).astype(int)
    o=(x>=0)&(x<W)&(y>=0)&(y<N)&(z>=0)&(z<NZ)
    sol[y[o],x[o],z[o]]=1
    if nz[k]<.6: steep[y[o],x[o],z[o]]=1
print('tris',m.sum(),time.time()-t0,flush=True)
pts=np.load('reach_main.npy').astype(int)
y,x,z=pts.T
roof=np.full(len(pts),999,int)
for h in range(6,60):
    zz=z+h;k=(zz<NZ)&(roof==999)
    i=np.flatnonzero(k);i=i[sol[y[i],x[i],zz[i]]];roof[i]=h
np.save('roof_main.npy',roof.astype(np.int16));print('cubierto',(roof<60).mean(),(roof<30).mean(),time.time()-t0)
im=np.zeros((N,W,3),np.uint8);im[y,x]=(70,70,70);k=roof<45;im[y[k],x[k]]=np.c_[np.clip(255-roof[k]*4,60,255),np.full(k.sum(),160),np.full(k.sum(),60)]
cv2.imwrite('roof.png',im[:,:,::-1])
