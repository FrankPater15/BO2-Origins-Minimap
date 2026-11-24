import sys,os
B=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,B+'/_lib')
import numpy as np,cv2
def load():
    R=[]
    for l in open(B+'/../mm/scan.log',errors='ignore'):
        if 'MM;' in l:
            try:
                v=list(map(int,l.split('MM;')[1].strip().rstrip(';').split(';')))
                if len(v)==27:R.append(v)
            except ValueError: pass
    a=np.unique(np.array(R),axis=0).astype(float);c=a[:,0]>8000
    return a[~c],a[c]
def links(a,maxd=200):
    dx=a[None,:,0]-a[:,None,0];dy=a[None,:,1]-a[:,None,1];D=np.hypot(dx,dy);dz=abs(a[:,None,2]-a[None,:,2])
    # clear along the two bracketing rays (wall clearance at least the distance, small slack)
    an=(np.degrees(np.arctan2(dy,dx))%360)/15;k=np.floor(an).astype(int)%24;f=an-np.floor(an)
    d=a[:,3:];i=np.arange(len(a))[:,None]
    near=np.where(f<.5,d[i,k],d[i,(k+1)%24]); 
    # near-coincident nodes have no meaningful bearing
    ok=(near+20>=D)|(D<35);ok&=ok.T
    L=(D<maxd)&(dz<np.maximum(30,.75*D))&ok;np.fill_diagonal(L,False)
    return L,D,dz
def ground(a):
    use=np.hypot(a[:,0],a[:,1])>1000
    g=np.array([np.median(a[use&(np.hypot(a[:,0]-x,a[:,1]-y)<1100),2]) for x,y in a[:,:2]])
    for R_ in(900,700):
      for _ in range(3):
        u=use&(abs(a[:,2]-g)<110)
        n=[]
        for x,y in a[:,:2]:
            r=np.hypot(a[:,0]-x,a[:,1]-y);q=u&(r<R_)
            if q.sum()<8:q=u&(r<np.sort(r[u])[15])
            w=np.exp(-(r[q]/(R_*.45))**2);X=np.c_[np.ones(q.sum()),a[q,0]-x,a[q,1]-y]
            s=np.sqrt(w)[:,None];A=(X*s).T@(X*s)+np.diag([1e-6,3e4*w.sum(),3e4*w.sum()]);n.append(np.linalg.solve(A,(X*w[:,None]).T@a[q,2])[0])
        g=np.array(n)
    return g
def cov(a,D):
    z=a[:,2];d=z[None,:]-z[:,None]
    return ((D<120)&(d>95)).any(1),((D<120)&(d<-95)).any(1)
if __name__=='__main__':
    a,c=load();L,D,dz=links(a);g=ground(a);rel=a[:,2]-g;ab,be=cov(a,D)
    print(np.c_[np.arange(-650,300,25)[:-1],np.histogram(rel,np.arange(-650,300,25))[0]].T.tolist())
    n=1600;im=np.zeros((n,n,3),np.uint8);im2=im.copy()
    P=lambda x,y:(int((x-128)/10000*n+n/2),int(n/2-(y-808)/10000*n))
    for i,j in zip(*np.where(np.triu(L))):cv2.line(im,P(*a[i,:2]),P(*a[j,:2]),(60,60,60),1)
    cm=cv2.applyColorMap(np.clip(128+rel*.6,0,255).astype(np.uint8)[:,None],cv2.COLORMAP_TURBO)[:,0]
    for i in np.argsort(a[:,2]):
        cv2.circle(im,P(*a[i,:2]),4,cm[i].tolist(),-1)
    cv2.imwrite(B+'/dbg_rel.png',im)
