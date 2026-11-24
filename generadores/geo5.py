import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
V=np.load('V.npy');T=np.load('Tr.npy')
# phase by edge sharing
q=V[T];n=np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]);l=np.linalg.norm(n,axis=1);print('deg',(l<1).mean(),'up',(n[:,2]/np.maximum(l,1e-6)>.7).mean(),'down',(n[:,2]/np.maximum(l,1e-6)<-.7).mean())
R=[]
for L in open('scan.log',errors='ignore'):
    if 'MM;' in L:
        try:
            v=list(map(int,L.split('MM;')[1].strip().rstrip(';').split(';')))
            if len(v)==27:R.append(v[:3])
        except ValueError:pass
R=np.unique(np.array(R,float),axis=0)
E=[]
for p in R[::4]:
    a,b,c=(q[:,k,:2]-p[:2] for k in range(3))
    s=[x[:,0]*y[:,1]-x[:,1]*y[:,0] for x,y in((a,b),(b,c),(c,a))]
    i=((s[0]>0)&(s[1]>0)&(s[2]>0))|((s[0]<0)&(s[1]<0)&(s[2]<0))
    z=[(s[1]*q[:,0,2]+s[2]*q[:,1,2]+s[0]*q[:,2,2])/(s[0]+s[1]+s[2]+1e-9)][0][i]
    if len(z): E.append(np.abs(z-p[2]).min())
    else:E.append(999)
E=np.array(E);print('median',np.median(E),(E<10).mean(),(E<40).mean())
