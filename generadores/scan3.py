import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r'); n=len(d)
# runs of plausible float coords at each 4-byte phase
for ph in range(4):
    f=np.frombuffer(d[ph:ph+(n-ph)//4*4].tobytes(),'<f4')
    a=np.abs(f); ok=((a<20000)&(a>.05))|(f==0)
    # smooth over 300 floats
    c=np.concatenate([[0],np.cumsum(ok)]); w=240; r=(c[w:]-c[:-w])>=w-2
    nz=np.concatenate([[0],np.cumsum((f!=0)&ok)]); r&=(nz[w:]-nz[:-w])>w*.6
    ed=np.flatnonzero(np.diff(np.concatenate([[0],r.astype(int),[0]])))
    for s,e in zip(ed[::2],ed[1::2]):
        L=e-s+w
        if L>20000:
            o=s*4+ph; best=None
            for st in(3,4,5,6,7,8,9,10,11,14):
                for k in range(st):
                    x=f[s+k:s+L:st]; v=np.abs(np.diff(x)).mean()
                    if best is None: best=[]
                    best.append((round(float(v),1),st,k))
            print(ph,o,L,sorted(best)[:2],f[s+300:s+312].round(1).tolist(),flush=True)
    del f,a,ok,c,r,nz
