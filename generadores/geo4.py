import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
np.seterr(all='ignore')
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
g=lambda a,b,t:np.frombuffer(d[a:b].tobytes(),t)
T=g(124036330,124036330+6*60000,'<u2').astype(int)
out=[]
for s in range(123535594,123536594,4):
    v=g(s,s+12*39000,'<f4').reshape(-1,3).astype(float)
    for ph in range(3):
        t=T[ph:ph+150000][:len(T[ph:ph+150000])//3*3].reshape(-1,3)[::7]
        q=v[t]; L=np.linalg.norm(q[:,0]-q[:,1],axis=1)+np.linalg.norm(q[:,2]-q[:,1],axis=1)
        ok=np.isfinite(L)&(L>1)
        if ok.mean()>.97: out.append((float(np.median(L)),float(np.percentile(L,90)),s,ph))
out.sort();print(out[:6])
s,ph=out[0][2:]
# E: first index triple: walk back while edges sane
v=g(s,s+(124016000-s)//12*12,'<f4')[:(124016000-s)//12*3].reshape(-1,3).astype(float)
e=124036330+2*ph
def sane(o):
    t=g(o,o+6,'<u2').astype(int); 
    if t.max()>=41000 or len(set(t))<3: return False
    q=v[t]; return np.linalg.norm(q[0]-q[1])<6000 and np.linalg.norm(q[0]-q[2])<6000
a=e
miss=0
last=a
while a>123990000:
    a-=6
    if sane(a): last=a; miss=0
    else:
        miss+=1
        if miss>4: break
print('E',last,'verts',(last-s)/12)
a=e;miss=0;end=a
while a<124470000:
    if sane(a): end=a+6;miss=0
    else:
        miss+=1
        if miss>6: break
    a+=6
print('end',end,'tris',(end-last)/6)
open('tri.txt','w').write(f'{s} {last} {end}')
V=v[:int((last-s)//12)].astype('f4'); t=g(last,end,'<u2').reshape(-1,3).astype(int); t=t[(t<len(V)).all(1)]
np.save('V.npy',V);np.save('Tr.npy',t);print(V.min(0),V.max(0),len(t))
