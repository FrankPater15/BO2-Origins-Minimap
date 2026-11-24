import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
A=122378782;Z=126405085
b=d[A:Z].tobytes()
# segment map: classify 2KB pages at all phases
for s in range(0,len(b)-8192,16384):
    best=max(range(4),key=lambda ph:(lambda f:((np.abs(f)<20000)&(np.abs(f)>.05)).mean())(np.nan_to_num(np.frombuffer(b[s+ph:s+ph+8192],'<f4'),nan=1e30)))
    f=np.nan_to_num(np.frombuffer(b[s+best:s+best+8192],'<f4'),nan=1e30); fr=((np.abs(f)<20000)&(np.abs(f)>.05)).mean()
    u=[np.frombuffer(b[s+k:s+k+8192],'<u2').astype(int) for k in(0,1)]
    du=[np.median(np.abs(np.diff(x))) for x in u]
    print(A+s,best,round(float(fr),2),du,u[int(np.argmin(du))][1000:1008].tolist())
