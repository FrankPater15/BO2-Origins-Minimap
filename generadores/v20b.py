import sys,io,os,struct
T=sys.argv[1];M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
ns={'__name__':'arte'};src=open(G+'arte.py',encoding='utf8').read()
i=src.index('def panzer():');j=src.index('def dot():')
src=src[:i]+'''def panzer():
    # orange diamond with an exclamation mark: cannot be mistaken for a zombie dot
    A=Art();m=L(poly((512,90),(934,512),(512,934),(90,512)));A.put(blur(grow(m,60),10),K,.98);A.grad(m,(255,205,70),(255,96,0));A.bevel(m,24,.5)
    q=L(both(poly((440,270),(584,270),(552,590),(472,590)),ell(512,690,66)));A.put(q,(30,10,0));return A
'''+src[j:]
open(G+'arte.py','w',encoding='utf8').write(src)
exec(compile(src,'arte','exec'),ns);im=ns['panzer']().out(64);im.save(G+'icono_panzer.png')
b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5');h=open(T+'/images/grenadeicon.iwi','rb').read(64)
for p in(M,T):
    with open(p+'/images/hud_zombierank_5_ded.iwi','wb') as f:f.write(h+b.getvalue()[128:128+4096])
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';s=open(lp,newline='').read();g=open(gp,newline='').read()
def R(t,a,c):
    assert t.count(a)==1,(t.count(a),a);return t.replace(a,c)
s=R(s,'image(e, MM.ZombieMat, 10.5, 1, 1, 1, 1)','image(e, MM.DotMat, 7, 1, 0.1, 0.08, 1)')
s=R(s,'-10.4, -5.2)','-8.8, -3.6)');s=R(s,'5.2, 10.4)','3.6, 8.8)')
s=R(s,'image(view, MM.ZombieMat, 10, 1, 1, 1, 0)','image(view, MM.DotMat, 7, 1, 0.1, 0.08, 0)')
s=R(s,'(o.h == "4" and 9) or 5)','(o.h == "4" and 8) or 3.5)')
s=R(s,'{ "Zombi", pic(MM.ZombieMat, 18) }','{ "Zombi", pic(MM.DotMat, 11, 1, 0.1, 0.08) }')
s=R(s,'MM.ZombieMat = "menu_mp_lobby_icon_film"\n','');assert 'ZombieMat' not in s
g=R(g,'\tprecacheshader( "menu_mp_lobby_icon_film" );\n','')
for p,v in((lp,s),(gp,g)):
    with open(p,'w',newline='') as f:f.write(v)
print('ok')
