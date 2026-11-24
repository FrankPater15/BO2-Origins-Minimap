from PIL import Image,ImageDraw,ImageFont
D=__import__('os').environ['MM_DOCS']+'/';k=1.5;F=lambda s:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',int(s*k))
im=Image.new('RGBA',(1920,1080),(24,27,29,255));m=Image.open(D+'mapa_v17.png').resize((966,966),Image.LANCZOS);im.paste(m,(477,57));d=ImageDraw.Draw(im,'RGBA')
X=lambda x:960+x*k;Yy=lambda y:540+y*k
d.rectangle((X(-628),Yy(-318),X(-334),Yy(196)),fill=(8,11,15,235));d.rectangle((X(-628),Yy(-318),X(-334),Yy(-316)),fill=(140,191,204))
d.text((X(-614),Yy(-301)),'SIGNIFICADO',font=F(16),fill=(255,217,77),anchor='lm')
C=lambda *c:tuple(int(v*255) for v in c)
def dot(x,y,r,c,ri=1):
    for q,cc in((r+.8,(0,0,0)),((r+.8)*.755,c)):d.ellipse((x-q*k,y-q*k,x+q*k,y+q*k),fill=cc)
def ring(x,y,r,c):dot(x,y,r+.8,c);dot(x,y,r*.64,(18,23,30))
def spr(n,x,y,s,c=(1,1,1)):
    q=(Image.open(D+n) if n.endswith('.png') else n).convert('RGBA').resize((int(s*k),)*2,Image.LANCZOS);R,G,B,A=q.split();q=Image.merge('RGBA',[z.point(lambda v,m=m:int(v*m)) for z,m in zip((R,G,B),c)]+[A]);im.alpha_composite(q,(int(x-q.width/2),int(y-q.height/2)))
def br(x,y,l,t,r,b,c):d.rectangle((x+l*k,y+t*k,x+r*k,y+b*k),fill=c)
def let(x,y,t,c,s=9):d.text((x,y),t,font=F(s),fill=c,anchor='mm')
H='hud_zombierank_%d_ded.png';pk=lambda n:lambda x,y:spr('medir/perk2/specialty_%s_zombies.png'%n,x,y,19)
def foot(x,y):ring(x,y,7.5,C(1,.65,.15));br(x,y,-3.4,-3,-.8,3,C(1,.68,.23));br(x,y,.8,-3,3.4,3,C(1,.68,.23))
def wf(x,y):
    br(x,y,-2.6,-8,2.6,-3,(0,0,0));d.ellipse((x-6.4*k,y-5.2*k,x+6.4*k,y+8*k),fill=(0,0,0));d.ellipse((x-5*k,y-3.8*k,x+5*k,y+6.5*k),fill=(158,64,242));br(x,y,-1.8,-7.2,1.8,-3,(158,64,242));br(x,y,-2.6,-8.2,2.6,-6.6,(255,217,77));let(x,y+2,'?','white',8)
def staff(x,y):ring(x,y,7.5,C(.35,.78,1));d.line((x-5,y+5,x+4,y-4),fill=(235,225,205),width=3);d.ellipse((x+1.5,y-7.5,x+7,y-2),fill=C(.35,.78,1))
def portal(x,y):dot(x,y,7.5,C(.76,.45,1));dot(x,y,4,(18,23,30));dot(x,y,2.4,C(.76,.45,1))
rows=[('Tu',lambda x,y:spr(H%4,x,y,18)),('Otro jugador (un color cada uno)',lambda x,y:spr(H%4,x,y,16,(1,.85,.2))),('Zombi',lambda x,y:dot(x,y,3.5,C(1,.13,.1))),('Panzer Soldat',lambda x,y:spr(H%5,x,y,20)),('Zona donde pisa un robot',foot),('Pie de robot',lambda x,y:dot(x,y,6,C(1,.8,.15))),('Pie bajando: sal de ahi',lambda x,y:dot(x,y,6,C(1,.12,.08))),('Generador',lambda x,y:(ring(x,y,7,(242,242,242)),let(x,y,'G','white'))),('Generador capturado',lambda x,y:(br(x,y,-5,-5,5,5,(0,0,0)),br(x,y,-4,-4,4,4,C(.15,.85,.3)))),('Caja misteriosa',lambda x,y:(dot(x,y,7,(20,25,33)),let(x,y,'B',C(.3,.85,1)))),('Pack-a-Punch',lambda x,y:(ring(x,y,7,C(1,.5,.9)),let(x,y,'P',C(1,.5,.9)))),('Wunderfizz (ventaja al azar)',wf),('Juggernog',pk('juggernaut')),('Quick Revive',pk('quickrevive')),('Speed Cola',pk('fastreload')),('Stamin-Up',pk('marathon')),('Mule Kick (en la cripta)',pk('mulekick')),('Baston (cripta y Crazy Place)',staff),('Portal (Crazy Place)',portal)]
for i,(t,f) in enumerate(rows):
    y=Yy(-273+i*25);f(X(-604),y);d.text((X(-584),y),t,font=F(12),fill=(235,240,242),anchor='lm')
im.convert('RGB').save(D+'mapa_leyenda_2.png')
