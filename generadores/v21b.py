import sys,io,os
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(G+'arte.py',encoding='utf8').read()
i=src.index('def box():');j=src.index('def pap():')
src=src[:i]+'''def mark(A,x,y,size,col):
    q=L(lambda d:d.text((x,y),'?',font=ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf',size),fill=255,anchor='mm'));A.put(grow(q,34),K,.95);A.put(q,col)
def box():
    # wooden crate with a big question mark
    A=Art();m=L(rr(70,150,954,900,60));A.put(blur(grow(m,50),14),K,.97);A.grad(m,(214,150,84),(112,62,26));A.bevel(m,22,.5)
    for y in (335,525,715):A.put(L(rr(150,y-8,874,y+8,6)),(60,30,12),.8)
    for a,b,c,d_ in ((70,150,200,900),(824,150,954,900),(70,150,954,270),(70,780,954,900)):
        p=L(rr(a,b,c,d_,34));A.put(grow(p,8),(50,24,8),.7);A.grad(p,(240,184,112),(142,82,36));A.bevel(p,14,.4)
    for x in (135,889):
        for y in (210,840):A.put(L(ell(x,y,24)),(70,60,55));A.put(L(ell(x-6,y-7,9)),(220,215,205))
    mark(A,512,515,620,(110,228,255));return A
'''+src[j:]
i=src.index('def wunder():');j=src.index('def foot():')
src=src[:i]+'''def wunder():
    # brown beer bottle with a question mark on the label
    A=Art();b=both(rr(425,60,599,420,40),poly((425,300),(599,300),(752,520),(272,520)),rr(272,480,752,975,70));m=L(b)
    A.put(blur(grow(m,54),14),K,.97);A.grad(m,(214,128,44),(92,40,8));A.bevel(m,34,.55)
    A.put(blur(L(rr(318,540,352,930,16)),8),W,.45);A.put(blur(L(rr(455,130,478,360,10)),6),W,.45)
    c=L(rr(402,40,622,135,26));A.put(grow(c,10),K,.8);A.grad(c,(255,235,150),(185,125,25));A.bevel(c,12,.5)
    l=L(rr(272,540,752,915,10));A.grad(l,(255,248,225),(226,202,150));A.put(L(both(rr(272,548,752,566,4),rr(272,889,752,907,4))),(176,30,30))
    q=L(lambda d:d.text((512,728),'?',font=ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf',390),fill=255,anchor='mm'));A.put(q,(176,16,22));return A
'''+src[j:]
open(G+'arte.py','w',encoding='utf8').write(src)
ns={'__name__':'arte'};exec(compile(src,'arte','exec'),ns);h=open(T+'/images/grenadeicon.iwi','rb').read(64)
for k,f in (('box','menu_mp_lobby_icon_clip'),('wunder','menu_mp_lobby_views')):
    im=ns['ICONS'][k]().out(64);im.save(G+'icono_%s.png'%k)
    if go:
        b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5')
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(h+b.getvalue()[128:128+4096])
print('ok',go)
