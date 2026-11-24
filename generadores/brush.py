import sys; sys.path.insert(0,'../agent_map/_lib')
import numpy as np
d=np.memmap('../agent_lui/ff/zm_tomb.bin',dtype=np.uint8,mode='r')
A,B=118000000,127500000
for ph in range(4):
    b=d[A+ph:B].tobytes(); b=b[:len(b)//4*4]
    f=np.frombuffer(b,'<f4'); u=np.frombuffer(b,'<u4')
    m=len(f)-30; i=np.arange(m)
    with np.errstate(all='ignore'):
        ok=np.ones(m,bool)
        for k in range(3):
            lo=f[i+k];hi=f[i+4+k]; ok&=(np.abs(lo)<40000)&(np.abs(hi)<40000)&(hi-lo>0.01)
        ok&=(u[i+7]<200)
        idx=np.flatnonzero(ok)
    from collections import Counter
    if len(idx)<500: print(ph,len(idx)); continue
    c=Counter(np.diff(idx)).most_common(4); print(ph,len(idx),c, A+ph+4*idx[0])
    s=c[0][0]
    # longest chains
    S=set(idx.tolist()); ch=[]
    for x in idx:
        if x-s not in S:
            k=x
            while k+s in S:k+=s
            if (k-x)//s>30: ch.append((A+ph+4*int(x),int((k-x)//s+1)))
    print(s,sorted(ch,key=lambda t:-t[1])[:10])
    for o,_ in sorted(ch,key=lambda t:-t[1])[:1]:
        for q in range(4):
            r=d[o+q*s*4:o+q*s*4+s*4].tobytes(); print(np.frombuffer(r,'<f4')[:8].round(1), [hex(v) for v in np.frombuffer(r,'<u4')])
