import sys,io,os
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(G+'arte.py',encoding='utf8').read()
i=src.index('def mark(');j=src.index('def pap():')
src=src[:i]+'''def glyph(x,y,size,turn=0):
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
'''+src[j:]
i=src.index('def wunder():');j=src.index('def foot():')
src=src[:i]+'''def wunder():
    # long-neck glass soda bottle, crown cap, round label
    c=(170,70,255);A=Art();A.put(np.clip(1-np.hypot((XX-512)/430,(YY-600)/560),0,1)**1.2*.85,c)
    half=[(62,95),(66,250),(84,360),(140,450),(196,540),(210,620),(210,930),(186,985)]
    pts=[(512-x,y) for x,y in half]+[(512+x,y) for x,y in reversed(half)];m=blur(L(poly(*pts)),8).point(lambda v:255 if v>127 else 0)
    A.put(blur(grow(m,50),12),K,.97);A.grad(m,(226,170,255),(92,14,170))
    A.put(arr(m)*np.clip(1-np.abs(XX-512)/150,0,1)*.45,(235,150,255));A.bevel(m,30,.55)
    A.put(blur(L(rr(340,560,368,950,14)),7),W,.75);A.put(blur(L(rr(466,130,484,380,9)),5),W,.75)
    for x,y,r in ((640,560,13),(660,610,9),(620,500,10),(400,500,9),(655,925,12)):A.put(L(ell(x,y,r)),(255,225,255),.7)
    cap=L(both(rr(428,42,596,112,20),*[ell(438+i*25,112,15) for i in range(7)]));A.put(grow(cap,14),K,.9);A.grad(cap,(255,130,150),(170,10,40));A.bevel(cap,12,.5)
    A.put(L(ell(512,745,215)),(20,4,36));A.grad(L(ell(512,745,196)),(255,253,245),(222,208,235));A.put(L(ell(512,745,158)),(96,20,168))
    q=glyph(512,742,300);A.grad(q,(255,246,160),(255,196,30));return A
'''+src[j:]
open(G+'arte.py','w',encoding='utf8').write(src)
ns={'__name__':'arte'};exec(compile(src,'arte','exec'),ns);h=open(T+'/images/grenadeicon.iwi','rb').read(64)
for k,f in (('box','menu_mp_lobby_icon_clip'),('wunder','menu_mp_lobby_views')):
    a=ns['ICONS'][k]();a.out(256).save(G+'grande_%s.png'%k);im=a.out(64);im.save(G+'icono_%s.png'%k)
    if go:
        b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5')
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(h+b.getvalue()[128:128+4096])
print('ok',go)
