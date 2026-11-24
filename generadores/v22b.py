import sys,io,os
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
ns={'__name__':'arte'};exec(compile(open(G+'arte.py',encoding='utf8').read(),'arte','exec'),ns);h=open(T+'/images/grenadeicon.iwi','rb').read(64)
for k,f in dict(wunder='menu_mp_lobby_views',jugg='menu_mp_lobby_icon_film',revive='menu_mp_lobby_views_bg',speed='menu_mp_fileshare_custom',stamin='menu_mp_pip_red',mule='menu_mp_pip_green').items():
    a=ns['ICONS'][k]();a.out(256).save(G+'grande_%s.png'%k);im=a.out(64);im.save(G+'icono_%s.png'%k);b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5')
    if go:
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(h+b.getvalue()[128:128+4096])
print('ok',go)
