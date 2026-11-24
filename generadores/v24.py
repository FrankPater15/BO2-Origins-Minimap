import sys,io,os,re
T=sys.argv[1];M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc'
s=open(lp,newline='').read();g=open(gp,newline='').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a);s=s.replace(a,b)
R('\t\t{ "Baston: circulo con vara (cripta)" },\n\t\t{ "Portal: remolino (Crazy Place)" },\n','\t\t{ "Baston (cripta y Crazy Place)", pic("menu_mp_pip_blue", 20) },\n\t\t{ "Portal (Crazy Place)", pic("menu_mp_pip_outline", 20) },\n')
R('bar(lg, -628, -318, -334, 196,','bar(lg, -628, -318, -334, 178,');R('local y = -277 + (i - 1) * 21.8','local y = -279 + (i - 1) * 21')
a='\tprecacheshader( "zombies_rank_5" );\n';assert g.count(a)==1;g=g.replace(a,a+'\tprecacheshader( "menu_mp_pip_blue" );\n\tprecacheshader( "menu_mp_pip_outline" );\n')
ns={'__name__':'arte'};exec(compile(open(G+'arte.py',encoding='utf8').read(),'arte','exec'),ns);h=open(T+'/images/grenadeicon.iwi','rb').read(64)
for f,a in(('menu_mp_pip_blue',ns['staff'](ns['ELEM']['hielo'])),('menu_mp_pip_outline',ns['portal'](ns['ELEM']['rayo']))):
    b=io.BytesIO();a.out(64).save(b,format='DDS',pixel_format='DXT5')
    for p in(M,T):open(p+'/images/%s.iwi'%f,'wb').write(h+b.getvalue()[128:128+4096])
open(lp,'w',newline='').write(s);open(gp,'w',newline='').write(g);print('ok')
