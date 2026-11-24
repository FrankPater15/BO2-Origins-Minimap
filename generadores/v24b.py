"""v24b: church floors by outline (its roof is a model, not solid geometry) and smoother upper crypt. usage: S T [install]"""
import sys,os,io,re,shutil
G=os.path.dirname(os.path.abspath(__file__))+'/'
EXTRA=open(G+'v24b_extra.txt',encoding='utf8').read()
src=open(G+'v23.py',encoding='utf8').read().split('# ---- GSC')[0]
a="ar=sys.argv;sys.argv=['x',S,T];n15="
assert src.count(a)==1
src=src.replace(a,EXTRA+a)
src=src.replace("G+'atlas23_%d.png'","G+'atlas24_%d.png'").replace("atlas23_1.png","atlas24_1.png").replace('zonas_v23','zonas_v24').replace('techos_v23','techos_v24')
exec(compile(src,'v23','exec'))
gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';g=open(gp,newline='').read();s=open(lp,newline='').read()
i=g.index('mml_cells_setup()\n{');j=g.index('mml_inside( org )');rows=[';'.join('%d,%d,%d,%d'%c for c in cells[k:k+25]) for k in range(0,len(cells),25)]
g=g[:i]+'mml_cells_setup()\n{\n'+''.join('\tmml_row( "%s" );\n'%r for r in rows)+'}\n\n'+g[j:]
i=s.index('MM.Under = {');j=s.index('MM.UnderWorld');s=s[:i]+'MM.Under = {\n'+''.join('\t{ %.1f, %.1f, %d },\n'%t for t in tiles)+'}\n'+s[j:]
i=s.index('MM.BigCaves = {');j=s.index('-- x, y, name, colour');s=s[:i]+'MM.BigCaves = {\n'+''.join('\t{ %d, %d, %d, %d, %d },\n'%((q+1,)+tuple(bx)) for q,bx in enumerate(boxes))+'}\n'+s[j:]
if go:
    for f_,a_ in(('hud_zombierank_5',A[0]),('icon_facebook',A[1])):
        h=open(M+'/images/%s.iwi'%f_,'rb').read(64);b=io.BytesIO();Image.fromarray(a_).save(b,format='DDS',pixel_format='DXT5');o=h+b.getvalue()[128:128+2048*2048]
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f_,'wb') as fh:fh.write(o)
    for p,q in((lp,s),(gp,g)):
        with open(p,'w',newline='') as fh:fh.write(q)
    print('instalado')
