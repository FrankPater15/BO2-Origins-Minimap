import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np, collections
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
o=121570750
while True:   # back up to the array start
    r=np.frombuffer(d[o-96:o].tobytes(),'<f4'); 
    if not((r[4:7]>=r[:3]).all() and (np.abs(r[:7])<60000).all() and np.frombuffer(d[o-96:o].tobytes(),'<u4')[7]<300): break
    o-=96
n=0
B=[]
while True:
    b=d[o+96*n:o+96*n+96].tobytes(); f=np.frombuffer(b,'<f4');u=np.frombuffer(b,'<u4')
    if u[7]>300 or u[21]>600 or not(np.abs(f[:3])<70000).all():break
    B.append(u);n+=1
B=np.array(B);F=B.view('<f4'); print('start',o,'n',n,'end',o+96*n,'numverts',B[:,21].sum())
p=B[:,22];ok=B[:,21]>0;print(hex(p[ok].min()),hex(p[ok].max()))
print(collections.Counter(hex(x) for x in B[:,3]).most_common(14))
# calibrate file base: base s.t. verts fall exactly in bounds
W=np.flatnonzero(ok)[:400]; w=W[5]
best=[]
lo,hi=120300000,121570000
tgt=F[w,:3].astype('<f4').tobytes()
raw=d[lo:hi].tobytes()
pm=int(p[ok].min())
def score(base):
    s=0
    for k in W[::10]:
        q=base+int(p[k])-pm; v=np.frombuffer(d[q:q+12*int(B[k,21])].tobytes(),'<f4').reshape(-1,3)
        s+=np.allclose(v.min(0),F[k,:3],atol=1) and np.allclose(v.max(0),F[k,4:7],atol=1)
    return s
x=F[w,0].astype('<f4').tobytes(); i=-1;c=collections.Counter()
nv=int(B[w,21])
while (i:=raw.find(x,i+1))>=0:
    for k in range(nv):
        c[lo+i-12*k-(int(p[w])-pm)]+=1
for base in c:
    s=score(base)
    if s>5: print('base',base,s,len(W[::10]))
np.save('B.npy',B)
open('bo.txt','w').write(str(o+96*n))
