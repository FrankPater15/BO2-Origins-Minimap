import sys,io,os,re,shutil
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(G+'arte.py',encoding='utf8').read()
if 'def bottle(' not in src:
    i=src.index('def wunder():');j=src.index('def foot():');w=src[i:j]
    w=w.replace('def wunder():','def bottle(c,cap1,cap2,sym):').replace('c=(170,70,255);A=Art()','A=Art()')
    w=w.replace('(226,170,255),(92,14,170)','lerp(c,W,.55),lerp(c,K,.5)').replace('(235,150,255))','lerp(c,W,.45))').replace('(255,225,255),.7)','lerp(c,W,.8),.7)')
    w=w.replace('(255,130,150),(170,10,40)','cap1,cap2').replace('(20,4,36))','lerp(c,K,.88))').replace('(222,208,235))','(222,216,214))').replace('(96,20,168))','lerp(c,K,.42))')
    a=w.index('    q=glyph(512,742,300)');w=w[:a]+'    sym(A);return A\n'
    w+='''def white(A,m,col=(255,250,235),end=(228,220,200)):
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
'''
    src=src[:i]+w+src[j:]
    src=src.replace('dot=dot,tick=tick)','dot=dot,tick=tick,jugg=jugg,revive=revive,speed=speed,stamin=stamin,mule=mule)')
    open(G+'arte.py','w',encoding='utf8').write(src)
ns={'__name__':'arte'};exec(compile(src,'arte','exec'),ns);h=open(T+'/images/grenadeicon.iwi','rb').read(64)
F=dict(wunder='menu_mp_lobby_views',jugg='menu_mp_lobby_icon_film',revive='menu_mp_lobby_views_bg',speed='menu_mp_fileshare_custom',stamin='menu_mp_pip_red',mule='menu_mp_pip_green')
out={}
for k,f in F.items():
    a=ns['ICONS'][k]();a.out(256).save(G+'grande_%s.png'%k);im=a.out(64);im.save(G+'icono_%s.png'%k);b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5');out[f]=h+b.getvalue()[128:128+4096]
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc';s=open(lp,newline='').read();g=open(gp,newline='').read()
i=s.index('-- icons that belong to the game');j=s.index('-- fixed places: x, y, kind')
s=s[:i]+'-- own bottles, one per perk\nMM.PerkMat = {\n'+''.join('\t%s = "%s",\n'%(k,F[v]) for k,v in dict(J='jugg',R='revive',S='speed',M='stamin',K='mule').items())+'}\n'+s[j:]
assert s.count('image(e, mat, 19 * k, 1, 1, 1, 1)')==1;s=s.replace('image(e, mat, 19 * k, 1, 1, 1, 1)','image(e, mat, 22 * k, 1, 1, 1, 1)')
s=s.replace('image(e, MM.WunderMat, 21 * k','image(e, MM.WunderMat, 22 * k')
g,n=re.subn(r'\tprecacheshader\( "specialty_[a-z]+_zombies" \);\n','',g);assert n==5
a='\tprecacheshader( "zombies_rank_5" );\n';g=g.replace(a,a+''.join('\tprecacheshader( "%s" );\n'%f for k,f in F.items() if k!='wunder'))
# bottles above generators, perks above bottles of the random machine
m=s.index('MM.Fixed = {\n')+len('MM.Fixed = {\n');e=s.index('\n}',m);rows=s[m:e].split('\n');rows.sort(key=lambda r:0 if '"G' in r else 1);s=s[:m]+'\n'.join(rows)+s[e:]
t=re.sub('--.*','',re.sub('"[^"]*"','',s));assert len(re.findall(r'\b(function|if|do)\b',t))==len(re.findall(r'\bend\b',t)) and t.count('{')==t.count('}')
print(s[m:m+500])
if go:
    b_=T+'/respaldo_hud/zm_minimapa_v21';assert not os.path.exists(b_);shutil.copytree(M,b_)
    for f,d in out.items():
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(d)
    for p,v in((lp,s),(gp,g)):
        with open(p,'w',newline='') as fh:fh.write(v)
    print('instalado')
