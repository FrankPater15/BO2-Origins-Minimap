import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
g=lambda a,b,t:np.frombuffer(d[a:b].tobytes(),t)
print(g(124006250,124006350,'<f4').round(1).tolist()); print(g(124006318-12,124006318+120,'<u2').tolist())
# window max/mins of indices
for o in range(124006330,124470000,30000): 
    w=g(o,o+30000,'<u2'); print(o,w.min(),w.max(),np.median(np.abs(np.diff(w.astype(int)))))
# first bad float walking backwards
v=g(124006318-12*45000+0,124006318,'<f4'); 
for lim in(30000,):
    bad=np.flatnonzero(~((np.abs(v)<lim)&((np.abs(v)>1e-4)|(v==0)))); print(len(v),bad[-5:],(len(v)-bad[-1])/3)
print(v[bad[-1]-3:bad[-1]+10])
for o in range(123528000,123537000,600): print(o,g(o+(124006318-o)%4,o+(124006318-o)%4+32,'<f4').round(2).tolist())
