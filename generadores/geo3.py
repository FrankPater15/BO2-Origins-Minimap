import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
g=lambda a,b,t:np.frombuffer(d[a:b].tobytes(),t)
print(g(124036331,124390001,'<u2')[:6], g(124036330,124390000,'<u2')[:6])
off=0 if np.median(np.abs(np.diff(g(124036330,124066330,'<u2').astype(int))))<np.median(np.abs(np.diff(g(124036331,124066331,'<u2').astype(int)))) else 1
for o in range(124006300+off,124012000,200):
    w=g(o,o+200,'<u2').astype(int); 
    if np.median(np.abs(np.diff(w)))<300: print('E near',o); break
print(g(o-260,o+60,'<u2').tolist())
w=g(124036330+off,124390000+off,'<u2'); print(off,w.max(),np.sort(np.unique(w))[-5:])
w=g(o+400,124460000+off,'<u2').astype(int); med=[(o+400+2*i,int(np.median(np.abs(np.diff(w[i:i+500])))),int(w[i:i+500].max())) for i in range(0,len(w)-500,2500)]
print(med)
a=g(124390000+off,124400000+off,'<u2'); 
E0=o
best=[]
for E in range(o-240,o+60,1):
    if (E-off)%2: continue
    t=g(E,E+6*3000,'<u2').reshape(-1,3).astype(int)
    cnt=t.max()+1
    if cnt>45000: continue
    for c in range(38000,40500):
        pass
# search vertex base: minimise edge length
T=g(124036330+off,124036330+off+6*9000,'<u2').astype(int)
out=[]
for ph in range(3):
    t=T[ph:ph+26997].reshape(-1,3)
    for s in range(123535200,123537000,1):
        v=g(s,s+12*39200,'<f4').reshape(-1,3) if (s-123536400)%4==0 or True else None
        q=v[t[:400]]
        with np.errstate(all='ignore'): L=np.linalg.norm(q[:,0]-q[:,1],axis=1)
        m=np.median(L)
        if np.isfinite(m): out.append((float(m),float(np.percentile(L,90)),s,ph))
out.sort(); print(out[:8])
