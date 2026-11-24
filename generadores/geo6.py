import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
np.seterr(all='ignore')
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
g=lambda a,b,t:np.frombuffer(d[a:b].tobytes(),t)
w=g(124011000,124017000,'<u2').astype(int)
bad=[i for i in range(len(w)-60) if np.abs(np.diff(w[i:i+60])).max()>3000]
o=124011000+2*(bad[-1]);print(o);print(g(o-80,o+200,'<u2').tolist()); print(g(o-60+(124006318-o)%4,o+100+(124006318-o)%4,'<f4').round(2).tolist())
w=g(124414000,124424000,'<u2'); k=np.flatnonzero(w>41000); print('end',124414000+2*k[0], w[k[0]-20:k[0]+10].tolist()); print('max',g(124040000,124414000+2*k[0],'<u2').max())
