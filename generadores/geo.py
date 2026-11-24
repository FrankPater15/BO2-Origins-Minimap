import sys,time; sys.path.insert(0,'../agent_map/_lib'); sys.path.insert(0,'../agent_map10')
import numpy as np, cv2
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
# ---- terrain arrays: find the boundary verts|indices
best=None
for E in range(123985000,124020000):
    pass
def isf(o): 
    v=np.frombuffer(d[o:o+12].tobytes(),'<f4'); return np.isfinite(v).all() and (np.abs(v)<30000).all() and ((np.abs(v)>1e-3)|(v==0)).all()
E=123990000
E+=(123536054-E)%12 if False else 0
cands=[]
for ph in range(12):
    o=123990000+ph
    while isf(o) and o<124030000:o+=12
    cands.append((o,ph))
print(sorted(cands)[-4:])
res=[]
for e0 in sorted({o for o,_ in cands if o>123995000}):
  for e in range(e0-40,e0+41):
    for k in (0,):
        t=np.frombuffer(d[e:e+6*60000].tobytes(),'<u2').reshape(-1,3).astype(int); cnt=t.max()+1
        s=e-12*cnt
        v=np.frombuffer(d[s:e].tobytes(),'<f4').reshape(-1,3)
        if not np.isfinite(v).all() or np.abs(v).max()>60000: continue
        q=v[t[:20000]]; L=np.linalg.norm(q[:,0]-q[:,1],axis=1); res.append((float(np.median(L)),e,cnt,s))
res.sort(); print(res[:6])
