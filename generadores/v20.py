"""v20: illustrated icon set (arte.py)"""
import sys,io,os,re,struct,shutil
S,T=sys.argv[1:3];go=len(sys.argv)>3;M=T+'/mods/zm_minimapa';Q=S+'/mm/';G=os.path.dirname(os.path.abspath(__file__))+'/'
sys.path.insert(0,S+'/agent_map/_lib')
import numpy as np,cv2
from PIL import Image,ImageDraw
ns={'__name__':'arte'};exec(compile(open(G+'arte.py',encoding='utf8').read(),'arte','exec'),ns)
ICONS,ELEM,staff,portal=ns['ICONS'],ns['ELEM'],ns['staff'],ns['portal']
FILES=dict(dot='hud_zombierank_3_ded',arrow='hud_zombierank_4_ded',panzer='hud_zombierank_5_ded',zombie='menu_mp_lobby_icon_film',gen='menu_mp_lobby_icon_customgamemode',box='menu_mp_lobby_icon_clip',pap='menu_mp_lobby_icon_screenshot',wunder='menu_mp_lobby_views',foot='menu_mp_lobby_like',tick='menu_mp_lobby_icon_highlight')
hdr=open(T+'/images/grenadeicon.iwi','rb').read(64);assert struct.unpack_from('<HH',hdr,6)==(64,64)
def dxt(im,h):
    n=im.size[0];b=io.BytesIO();im.save(b,format='DDS',pixel_format='DXT5');d=b.getvalue();assert d[84:88]==b'DXT5' and struct.unpack_from('<HH',h,6)==(n,n)
    return h+d[128:128+n*n]
out={}
for k,f in FILES.items():
    im=ICONS[k]().out(64);im.save(G+'icono_%s.png'%k);out[f]=dxt(im,hdr)
def paste(im,x,y,art,size,op=1):
    a=art.out(256).resize((size,size),Image.LANCZOS)
    if op<1:a.putalpha(a.getchannel('A').point(lambda v:int(v*op)))
    im.alpha_composite(a,(int(round(x-size/2)),int(round(y-size/2))))
# ---- atlas 1: crypt staffs and Crazy Place
def mydraw(im,tr,items,r):
    for x,y,t,c in items:
        X,Y=tr(x,y);paste(im,X,Y,staff(c) if t=='staff' else portal(c),int(r*2.75))
v15=open(G+'v15.py',encoding='utf8').read().split('# ---- lookup cells')[0]
v15=v15.replace("draw(t,tr,[(0,-480,'K',(120,255,170))],15);","").replace("G+'atlas15_%d.png'","G+'atlas20_%d.png'")
a="N=2048;U=10000/N\n";assert v15.count(a)==1;v15=v15.replace(a,a+"draw=MYDRAW\n")
ar=sys.argv;sys.argv=['x',S,T];n15={'__file__':__file__,'MYDRAW':mydraw};exec(compile(v15,'v15','exec'),n15);sys.argv=ar
A=Image.fromarray(n15['A'][0]);tc=n15['tc'];cx,cy=tc(8)
ct=lambda x,y:(cx+(x-10464)/2700*660,cy-(y+7788)/2700*660)
for x,y,e in((11322,-8813,'viento'),(9425,-8620,'fuego'),(9552,-6905,'rayo'),(11367,-6900,'hielo')):paste(A,*ct(x,y),portal(ELEM[e]),62)
for x,y,e in((10576,-8142,'viento'),(10104,-8142,'fuego'),(10104,-7670,'rayo'),(10576,-7670,'hielo')):paste(A,*ct(x,y),staff(ELEM[e]),62)
A.save(G+'atlas20_1.png')
with open(M+'/images/hud_zombierank_5.iwi','rb') as fh:out['hud_zombierank_5']=dxt(A,fh.read(64))
# ---- base map: only the stomp zones stay printed
src=open(Q+'v11.py',encoding='utf8').read().split('icons(base,items,tr); base.save')[0].replace("Image.open(Q+'surf11.png')","Image.open(SURF)")
SURF=G+'surf17.png';sys.argv=['x',S,T,M];exec(src);sys.argv=ar
ft=ICONS['foot']();ft.c=ft.c*np.array([1,.66,.2],np.float32)
for x,y in feet:
    X,Y=tr(x,y);l=Image.new('RGBA',(256,256),(0,0,0,0));ImageDraw.Draw(l).ellipse((10,10,246,246),fill=(255,150,30,60),outline=(255,170,50,235),width=16)
    l=l.resize((30,30),Image.LANCZOS);base.alpha_composite(l,(int(round(X-15)),int(round(Y-15))));paste(base,X,Y,ft,23)
base.save(G+'base20.png')
with open(M+'/images/icon_twitter.iwi','rb') as fh:out['icon_twitter']=dxt(base,fh.read(64))
# ---- Lua
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc'
s=open(lp,newline='').read();g=open(gp,newline='').read()
def R(a,b,c=1):
    global s
    assert s.count(a)==c,(s.count(a),a);s=s.replace(a,b)
R('MM.PanzerMat = "zombies_rank_5_ded"\n','MM.PanzerMat = "zombies_rank_5_ded"\n-- unused lobby pictures, replaced by our own drawings\n'+''.join('MM.%sMat = "%s"\n'%(k.capitalize(),FILES[k]) for k in('zombie','gen','box','pap','wunder','foot','tick')))
R('MM.Fixed = {\n','MM.Fixed = {\n\t{ -5, -8, "P" },\n')
R('\t\tdot(e, 2.4, 1, 0.13, 0.1)\n','\t\timage(e, MM.ZombieMat, 10.5, 1, 1, 1, 1)\n')
R('setTopBottom(false, false, -8.4, -3.4)','setTopBottom(false, false, -10.4, -5.2)');R('setTopBottom(false, false, 3.4, 8.4)','setTopBottom(false, false, 5.2, 10.4)')
i=s.index('\t\toval(parent, -4.5 * k');j=s.index('\tend\n',i);s=s[:i]+'\t\timage(parent, MM.FootMat, 21 * k, cr, cg, cb, 1)\n'+s[j:]
i=s.index('\t\tlocal mat = MM.PerkMat[kind]');j=s.index('\t\treturn e\n',i)
s=s[:i]+'''		local mat = MM.PerkMat[kind]
		if mat then
			image(e, mat, 19 * k, 1, 1, 1, 1)
		elseif kind == "W" then
			image(e, MM.WunderMat, 21 * k, 1, 1, 1, 1)
		elseif kind == "P" then
			image(e, MM.PapMat, 20 * k, 1, 1, 1, 1)
		else
			image(e, MM.GenMat, 20 * k, 1, 1, 1, 1)
			local q = text(e, 10, 2)
			q:setText(kind)
		end
'''+s[j:]
# box and captured mark on the minimap
R('\t\tdot(e.box, 6, 0.08, 0.1, 0.13)\n','\t\timage(e.box, MM.BoxMat, 19, 1, 1, 1, 1)\n')
i=s.index('\t\t-- green square with a white tick');j=s.index('\t\te.label = text(e, 11, 1)');s=s[:i]+'\t\timage(e.cap, MM.TickMat, 11, 1, 1, 1, 1)\n'+s[j:]
R('e.label:setText(kind == "H" and "" or o.t)','e.label:setText("")')
R('project(o.x + 105, o.y + 105)','project(o.x + 130, o.y + 130)')
# full map
R('big.feet[i] = image(view, MM.DotMat, 14, 1, 0.8, 0.15, 0)','big.feet[i] = image(view, MM.FootMat, 18, 1, 0.8, 0.15, 0)')
R('big.caps[i] = image(view, "white", 8, 0.15, 0.85, 0.3, 0)','big.caps[i] = image(view, MM.TickMat, 11, 1, 1, 1, 0)')
i=s.index('\tdot(big.box, 6, 0.08');j=s.index('\tfor i = 1, MM.MaxZombies do\n\t\tbig.zombies',i);s=s[:i]+'\timage(big.box, MM.BoxMat, 19, 1, 1, 1, 1)\n'+s[j:]
R('big.zombies[i] = image(view, MM.DotMat, 7, 1, 0.13, 0.1, 0)','big.zombies[i] = image(view, MM.ZombieMat, 10, 1, 1, 1, 0)')
R('(o.h == "4" and 9) or 3.4)','(o.h == "4" and 9) or 5)');R('\t\t\tput(e, o.x, o.y, 7)\n','\t\t\tput(e, o.x, o.y, 9)\n')
R('put(big.caps[ci], o.x + 130, o.y + 130, 4)','put(big.caps[ci], o.x + 150, o.y + 130, 5.5)')
# legend
i=s.index('\tlocal function ring(e, r, cr');j=s.index('\tfor i = 1, #rows do\n\t\tlocal y = -273');
s=s[:i]+'''	local function pic(mat, size, r, g, b)
		return function(e)
			image(e, mat, size, r or 1, g or 1, b or 1, 1)
		end
	end
	local rows = {
		{ "Tu", pic(MM.ArrowMat, 18) },
		{ "Otro jugador (un color cada uno)", pic(MM.ArrowMat, 17, 1, 0.85, 0.2) },
		{ "Zombi", pic(MM.ZombieMat, 18) },
		{ "Panzer Soldat", pic(MM.PanzerMat, 21) },
		{ "Zona donde pisa un robot", pic(MM.FootMat, 18, 1, 0.66, 0.2) },
		{ "Pie de robot", pic(MM.FootMat, 20, 1, 0.8, 0.15) },
		{ "Pie bajando: sal de ahi", pic(MM.FootMat, 20, 1, 0.12, 0.08) },
		{ "Generador", pic(MM.GenMat, 20) },
		{ "Generador capturado", pic(MM.TickMat, 18) },
		{ "Caja misteriosa", pic(MM.BoxMat, 20) },
		{ "Pack-a-Punch", "P" },
		{ "Wunderfizz (ventaja al azar)", "W" },
		{ "Juggernog", "J" },
		{ "Quick Revive", "R" },
		{ "Speed Cola", "S" },
		{ "Stamin-Up", "M" },
		{ "Mule Kick (en la cripta)", "K" },
		{ "Baston: circulo con vara (cripta)" },
		{ "Portal: remolino (Crazy Place)" },
	}
'''+s[j:]
R('\t\tif type(rows[i][2]) == "string" then','\t\tif rows[i][2] == nil then\n\t\t\te = group(lg, 7, 1)\n\t\t\timage(e, MM.DotMat, 14, 0.4, 0.8, 1, 1)\n\t\telseif type(rows[i][2]) == "string" then')
a='\tprecacheshader( "zombies_rank_5" );\n';assert g.count(a)==1
g=g.replace(a,a+''.join('\tprecacheshader( "%s" );\n'%FILES[k] for k in('zombie','gen','box','pap','wunder','foot','tick')))
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x,y=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print('bloques',x,y);assert x==y
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1]),q
open(G+'v20_prev.lua','w',newline='').write(s)
if go:
    b=T+'/respaldo_hud/zm_minimapa_v19';assert not os.path.exists(b);shutil.copytree(M,b)
    for f,d in out.items():
        for p in(M,T):
            with open(p+'/images/%s.iwi'%f,'wb') as fh:fh.write(d)
    for p,v in((lp,s),(gp,g)):
        with open(p,'w',newline='') as fh:fh.write(v)
    print('instalado')
