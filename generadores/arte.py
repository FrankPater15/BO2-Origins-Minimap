"""Original icon set. Everything is drawn here, nothing comes from the game."""
import math,os
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont
Z=1024
def L(fn):
    m=Image.new('L',(Z,Z),0);fn(ImageDraw.Draw(m));return m
def arr(m):return np.asarray(m,np.float32)/255
def blur(m,r):return m.filter(ImageFilter.GaussianBlur(r))
def grow(m,r):return blur(m,r*.55).point(lambda v:min(255,int(v*9)) if v>6 else 0)
class Art:
    def __init__(s):s.c=np.zeros((Z,Z,3),np.float32);s.a=np.zeros((Z,Z),np.float32)
    def put(s,m,col,op=1):
        m=(m.astype(np.float32) if isinstance(m,np.ndarray) else arr(m))*op
        col=np.asarray(col,np.float32);col=col if col.ndim==3 else col[None,None]
        a=m+s.a*(1-m);s.c=(col*m[...,None]+s.c*(s.a*(1-m))[...,None])/np.maximum(a,1e-6)[...,None];s.a=a
    def grad(s,m,top,bot,op=1):
        ys=np.nonzero(np.asarray(m).max(1))[0];y0,y1=(ys[0],ys[-1]+1) if len(ys) else (0,Z)
        t=np.clip((np.arange(Z,dtype=np.float32)-y0)/(y1-y0),0,1)[:,None,None]
        s.put(m,np.broadcast_to(np.array(top)*(1-t)+np.array(bot)*t,(Z,Z,3)),op)
    def bevel(s,m,size=26,k=.5):
        h=arr(blur(m,size));gy,gx=np.gradient(h);l=np.clip((gx+gy)*size*1.6,-1,1);mm=arr(m)
        s.put(mm*np.clip(l,0,1)*k,(255,255,255));s.put(mm*np.clip(-l,0,1)*k,(0,0,0))
    def out(s,n=64):
        rgb=s.c*s.a[...,None];k=Z//n;a=s.a.reshape(n,k,n,k).mean((1,3));c=rgb.reshape(n,k,n,k,3).mean((1,3))
        return Image.fromarray(np.dstack([np.clip(c/np.maximum(a,1e-4)[...,None],0,255),np.clip(a,0,1)*255]).astype(np.uint8))
def ell(x,y,rx,ry=None):
    ry=ry or rx
    return lambda d:d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
def poly(*p):return lambda d:d.polygon(p,fill=255)
def rr(a,b,c,e,r):return lambda d:d.rounded_rectangle((a,b,c,e),r,fill=255)
def both(*fs):
    def f(d):
        for q in fs:q(d)
    return f
def lerp(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
W=(255,255,255);K=(0,0,0);FONT='C:/Windows/Fonts/arialbd.ttf'
YY,XX=np.mgrid[0:Z,0:Z].astype(np.float32)
def badge(A,col,shape=None,R=430):
    m=L(shape or ell(512,512,R));A.put(blur(grow(m,40),14),K,.95);A.grad(m,lerp(col,W,.5),lerp(col,K,.45));A.bevel(m,20,.55)
    n=Z*80//100;sm=m.resize((n,n),Image.LANCZOS);i=Image.new('L',(Z,Z),0);i.paste(sm,((Z-n)//2,)*2)
    A.put(i,K);A.grad(i,lerp(col,(14,18,26),.62),(8,11,17))
    g=np.clip(1-np.hypot(XX-512,YY-640)/430,0,1)**2;A.put(arr(i)*g*.65,col)
    A.put(arr(i)*np.clip(1-np.hypot((XX-512)/420,(YY-230)/170),0,1)*.28,W)
def arrow():
    A=Art();p=[(512,60),(905,935),(512,735),(119,935)];m=L(poly(*p));A.put(blur(grow(m,58),10),K,.98)
    A.put(L(poly((512,60),(119,935),(512,735))),W);A.put(L(poly((512,60),(905,935),(512,735))),(165,170,178))
    A.put(L(lambda d:d.line(p+p[:1],fill=255,width=16,joint='curve')),W,.8);return A
def zombie():
    A=Art();m=L(both(ell(512,430,345,340),rr(300,560,724,860,90)));A.put(blur(grow(m,62),12),K,.98)
    A.grad(m,(255,105,80),(170,12,10));A.bevel(m,40,.45)
    A.put(L(both(poly((300,380),(480,440),(460,560),(320,545)),poly((724,380),(544,440),(564,560),(704,545)))),(22,2,2))
    A.put(L(both(ell(402,500,44),ell(622,500,44))),(255,225,90));A.put(L(poly((512,570),(560,665),(464,665))),(40,3,3))
    A.put(L(rr(350,715,674,825,30)),(30,3,3))
    A.put(L(both(*[poly((365+i*62,715),(405+i*62,715),(385+i*62,775)) for i in range(5)])),(255,225,200));return A
def gen():
    A=Art();badge(A,(235,235,235),poly(*[(512+455*math.cos(math.pi/6+i*math.pi/3),512+455*math.sin(math.pi/6+i*math.pi/3)) for i in range(6)]));return A
def glyph(x,y,size,turn=0):
    m=L(lambda d:d.text((512,512),'?',font=ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf',size),fill=255,anchor='mm')).rotate(turn)
    o=Image.new('L',(Z,Z),0);o.paste(m,(x-512,y-512));return o
def box():
    # long wooden chest, two yellow marks, the second one upside down
    A=Art();A.put(np.clip(1-np.hypot((XX-512)/560,(YY-500)/430),0,1)**1.3*.55,(255,215,60))
    lid=L(poly((130,190),(894,190),(1000,420),(24,420)));front=L(rr(24,405,1000,850,26));m=L(both(poly((130,190),(894,190),(1000,420),(24,420)),rr(24,405,1000,850,26)))
    A.put(blur(grow(m,48),12),K,.97);A.grad(lid,(206,128,72),(150,82,40));A.grad(front,(172,94,46),(84,40,16));A.bevel(lid,16,.4);A.bevel(front,20,.45)
    for y in (545,700):A.put(L(rr(40,y-6,984,y+6,4)),(48,22,8),.8)
    A.put(L(rr(24,405,1000,430,8)),(52,24,8),.9)
    for x in (70,490,890):A.grad(L(rr(x,395,x+48,855,10)),(110,66,40),(58,30,14))
    for x,t in ((290,0),(738,180)):
        q=glyph(x,630,390,t);A.put(grow(q,26),(30,14,0),.95);A.grad(q,(255,240,110),(255,190,10))
    return A
def pap():
    # upgrade machine: cabinet with two rollers and a big arrow
    A=Art();c=(225,80,200);A.put(np.clip(1-np.hypot(XX-512,YY-512)/520,0,1)**1.3*.7,c)
    m=L(both(rr(110,250,914,930,90),rr(300,90,724,300,60)));A.put(blur(grow(m,46),12),K,.97);A.grad(m,lerp(c,W,.45),lerp(c,K,.5));A.bevel(m,26,.5)
    w=L(rr(200,350,824,700,50));A.put(grow(w,10),K,.6);A.grad(w,(14,16,30),(44,24,60))
    for y in (430,620):
        m=L(rr(220,y-58,804,y+58,56));A.grad(m,(225,232,240),(90,96,110));A.bevel(m,16,.4)
    m=L(poly((512,325),(712,535),(596,535),(596,725),(428,725),(428,535),(312,535)));A.put(grow(m,26),K,.95);A.grad(m,(255,250,170),(255,170,30));A.bevel(m,14,.35)
    A.grad(L(ell(512,185,62)),(255,250,190),(255,180,40));A.grad(L(rr(300,775,724,850,36)),(50,20,50),(25,10,28));return A
def bottle(c,cap1,cap2,sym):
    # long-neck glass soda bottle, crown cap, round label
    A=Art();A.put(np.clip(1-np.hypot((XX-512)/430,(YY-600)/560),0,1)**1.2*.85,c)
    half=[(60,95),(62,260),(72,350),(104,440),(146,530),(160,620),(160,945),(140,990)]
    pts=[(512-x,y) for x,y in half]+[(512+x,y) for x,y in reversed(half)];m=blur(L(poly(*pts)),8).point(lambda v:255 if v>127 else 0)
    A.put(blur(grow(m,50),12),K,.97);A.grad(m,lerp(c,W,.55),lerp(c,K,.5))
    A.put(arr(m)*np.clip(1-np.abs(XX-512)/150,0,1)*.45,lerp(c,W,.45));A.bevel(m,30,.55)
    A.put(blur(L(rr(380,560,404,600,12)),7),W,.75);A.put(blur(L(rr(466,130,484,380,9)),5),W,.75)
    for x,y,r in ((600,570,12),(625,615,8),(580,500,9),(440,480,8),(610,965,9)):A.put(L(ell(x,y,r)),lerp(c,W,.8),.7)
    cap=L(both(rr(428,42,596,112,20),*[ell(438+i*25,112,15) for i in range(7)]));A.put(grow(cap,14),K,.9);A.grad(cap,cap1,cap2);A.bevel(cap,12,.5)
    A.put(L(ell(512,760,176)),lerp(c,K,.88));A.grad(L(ell(512,760,160)),(255,253,245),(222,216,214));A.put(L(ell(512,760,132)),lerp(c,K,.42))
    # the symbol is drawn on its own and shrunk to the label
    q=Art();sym(q);im=q.out(1024);n=840;im=im.resize((n,n),Image.LANCZOS);f=Image.new('RGBA',(Z,Z),(0,0,0,0));f.paste(im,(int(512-512*n/Z),int(760-745*n/Z)))
    a=np.asarray(f,np.float32);A.put(a[...,3]/255,a[...,:3]);return A
def white(A,m,col=(255,250,235),end=(228,220,200)):
    A.put(grow(m,14),K,.75);A.grad(m,col,end)
def wunder():return bottle((170,70,255),(255,130,150),(170,10,40),lambda A:A.grad(glyph(512,742,300),(255,246,160),(255,196,30)))
def sh_shield(A):
    white(A,L(poly((512,618),(625,655),(618,760),(580,822),(512,872),(444,822),(406,760),(399,655))));A.put(L(both(rr(488,665,536,820,8),rr(440,712,584,760,8))),(205,20,25))
def sh_heart(A):
    white(A,L(both(ell(458,705,66),ell(566,705,66),poly((399,735),(625,735),(512,868)))));A.put(L(lambda d:d.line([(395,745),(455,745),(482,690),(520,800),(548,745),(630,745)],fill=255,width=26,joint='curve')),(20,110,210))
def sh_speed(A):
    for x in (430,540):white(A,L(poly((x-40,635),(x+30,635),(x+115,742),(x+30,850),(x-40,850),(x+45,742))))
def sh_wing(A):
    white(A,L(both(poly((420,780),(400,690),(600,630),(640,650),(560,712)),poly((430,800),(520,722),(618,712),(540,772)),poly((440,838),(500,786),(585,778),(520,840)))))
def sh_shoe(A):
    m=L(lambda d:(d.arc((412,640,612,850),150,390,fill=255,width=58),d.rectangle((418,780,470,858),fill=255),d.rectangle((554,780,606,858),fill=255)));white(A,m)
    A.put(L(both(*[ell(x,y,11) for x,y in ((442,745),(470,690),(512,668),(554,690),(582,745))])),(20,70,45))
GOLD=((255,236,150),(190,130,25))
def jugg():return bottle((228,28,34),*GOLD,sh_shield)
def revive():return bottle((40,160,255),*GOLD,sh_heart)
def speed():return bottle((40,200,70),*GOLD,sh_speed)
def stamin():return bottle((255,176,20),*GOLD,sh_wing)
def mule():return bottle((20,150,120),*GOLD,sh_shoe)
def foot():
    A=Art();m=L(both(ell(512,360,285,310),ell(512,820,215,165),rr(345,560,679,760,60)));A.put(blur(grow(m,60),12),K,.97);A.grad(m,W,(190,190,190));A.bevel(m,34,.4)
    A.put(L(both(*[rr(330,170+i*95,694,212+i*95,18) for i in range(5)],rr(390,770,634,808,16),rr(390,845,634,883,16))),(45,38,30),.9);return A
def panzer():
    # orange diamond with an exclamation mark: cannot be mistaken for a zombie dot
    A=Art();m=L(poly((512,90),(934,512),(512,934),(90,512)));A.put(blur(grow(m,60),10),K,.98);A.grad(m,(255,205,70),(255,96,0));A.bevel(m,24,.5)
    q=L(both(poly((440,270),(584,270),(552,590),(472,590)),ell(512,690,66)));A.put(q,(30,10,0));return A
def dot():
    A=Art();m=L(ell(512,512,400));A.put(L(ell(512,512,490)),K);A.grad(m,W,(195,195,195));A.put(arr(m)*np.clip(1-np.hypot(XX-400,YY-360)/240,0,1),W,.8);return A
def staff(c):
    A=Art();badge(A,c);s=L(lambda d:d.line([(300,780),(600,410)],fill=255,width=74));A.put(grow(s,22),K,.9);A.grad(s,(255,240,200),(150,110,60))
    cl=L(lambda d:[d.arc((480,170,810,500),a,b,fill=255,width=52) for a,b in((70,200),(-70,20))]);A.put(grow(cl,14),K,.8);A.put(cl,(240,220,170))
    A.put(blur(L(ell(645,335,150)),40),c);A.put(L(ell(645,335,105)),lerp(c,W,.35));A.put(L(ell(615,300,36)),W,.9);return A
def portal(c):
    A=Art();r=np.hypot(XX-512,YY-512);t=np.arctan2(YY-512,XX-512);A.put(L(ell(512,512,500)),K,.9)
    v=np.clip(.2+(.5+.5*np.sin(3*t+r/46))*.8,0,1);col=np.array(c)[None,None]*(v*(.4+.6*r/470))[...,None]+255*(np.clip(1-r/190,0,1)**1.5)[...,None]
    A.put(np.clip((475-r)/8,0,1),np.clip(col,0,255));A.put(np.clip(1-np.abs(r-445)/26,0,1),lerp(c,W,.6));return A
def tick():
    A=Art();badge(A,(60,230,100));m=L(lambda d:d.line([(270,530),(450,710),(770,330)],fill=255,width=120,joint='curve'));A.put(grow(m,20),K,.9);A.grad(m,W,(150,255,170));return A
ICONS=dict(arrow=arrow,zombie=zombie,gen=gen,box=box,pap=pap,wunder=wunder,foot=foot,panzer=panzer,dot=dot,tick=tick,jugg=jugg,revive=revive,speed=speed,stamin=stamin,mule=mule)
ELEM=dict(fuego=(255,90,50),hielo=(90,200,255),viento=(240,225,110),rayo=(195,115,255))
if __name__=='__main__':
    im=Image.new('RGB',(1500,1010),(40,52,58));d=ImageDraw.Draw(im);f=ImageFont.truetype(FONT,20)
    al=dict(ICONS)
    for k,c in ELEM.items():al['baston '+k]=lambda c=c:staff(c)
    al['portal']=lambda:portal(ELEM['rayo'])
    for i,(n,fn) in enumerate(al.items()):
        a=fn().out(64);x,y=20+(i%5)*296,20+(i//5)*330;q=a.resize((224,224),Image.BICUBIC);im.paste(q,(x,y),q)
        for j,s in enumerate((30,20)):
            q=a.resize((s,s),Image.BILINEAR);im.paste(q,(x+236,y+40+j*50),q)
        d.text((x+110,y+250),n,font=f,fill='white',anchor='mm')
    im.save(__import__('os').environ['MM_DOCS']+'/arte.png')
