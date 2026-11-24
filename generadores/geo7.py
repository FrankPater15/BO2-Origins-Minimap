import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
pat=np.array([0,1,2,2,3,0,4,5,6,6,7,4],'<u2').tobytes()
E=124011000+d[124011000:124020000].tobytes().find(pat)
w=np.frombuffer(d[E:124419572].tobytes(),'<u2'); w=w[:len(w)//3*3]; T=w.reshape(-1,3).astype(int)
cnt=T.max()+1; s=E-12*cnt; V=np.frombuffer(d[s:E].tobytes(),'<f4').reshape(-1,3)
print(E,cnt,s,V.min(0),V.max(0),len(T)); np.save('V.npy',V);np.save('Tr.npy',T)
