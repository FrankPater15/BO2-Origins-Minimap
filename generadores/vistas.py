import sys,re
from PIL import Image,ImageDraw,ImageFont
S,L,O=sys.argv[1:4]
D=__import__('os').environ['MM_DOCS']+'/'
src=open(L,encoding='utf8').read()
def sec(n):
    b=src[src.index(n):];return b[:b.index('\n}')]
under=[tuple(map(float,t)) for t in re.findall(r'\{ (-?[\d.]+), (-?[\d.]+) \}',sec('MM.Under = {'))]
caves=[tuple(map(int,t)) for t in re.findall(r'\{ (\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) \}',sec('MM.BigCaves = {'))]
lab=re.findall(r'\{ (-?\d+), (-?\d+), "([^"]+)"(?:, ([\d.]+), ([\d.]+), ([\d.]+))? \}',sec('MM.BigLabels'))
F=lambda s:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',int(s))
base=Image.open(S+'/mm/base11.png').convert('RGBA');atlas=Image.open(S+'/mm/atlas11.png').convert('RGBA')
for i,t in {2:(190,110,255),3:(235,225,120),4:(90,200,255),5:(255,90,50)}.items():
    cx,cy=round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3);bx=(cx-160,cy-160,cx+160,cy+160);c=atlas.crop(bx);A=c.getchannel('A')
    lum=c.convert('RGB').convert('L');atlas.paste(Image.merge('RGBA',[lum.point(lambda v,m=m:min(255,int(m*min(1.15,max(.5,v/110))))) for m in t]+[A]),bx)
def fade(im,a):
    im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:int(v*a)));return im
def layer(dst,im,mx,my,world,cx,cy,rng,a):
    """im is square, centred on mx,my, covering 'world' units; dst shows rng units around cx,cy"""
    n=im.width;u=world/n
    box=tuple((v) for v in((cx-rng-mx)/u+n/2,n/2-(cy+rng-my)/u,(cx+rng-mx)/u+n/2,n/2-(cy-rng-my)/u))
    q=im.transform(dst.size,Image.EXTENT,box,Image.BILINEAR);dst.alpha_composite(fade(q,a))
IC={n:Image.open(D+'hud_zombierank_%s_ded.png'%n) for n in '345'}
def spr(im,X,Y,n,s,c=(1,1,1),rot=0):
    q=IC[n].resize((int(s),)*2,Image.BILINEAR).rotate(rot,resample=Image.BILINEAR,expand=True);R,G,B,A=q.split()
    q=Image.merge('RGBA',[z.point(lambda v,m=m:int(v*m)) for z,m in zip((R,G,B),c)]+[A]);im.alpha_composite(q,(max(0,int(X-q.width/2)),max(0,int(Y-q.height/2))))
Y_=(255,217,77);N=640
def mini(crazy,px,py,zs,place,col):
    k=N/200;m=Image.new('RGBA',(N,N),(22,30,36,255));rng=900 if crazy else 1750
    if crazy:layer(m,atlas,6455.1,-3779.1,12020.9,px,py,rng,.95)
    else:
        layer(m,base,128,808,10000,px,py,rng,.3);u=under[4];layer(m,atlas,u[0],u[1],20000,px,py,rng,.95)
    pt=lambda x,y:(N/2+(x-px)/rng*N/2,N/2-(y-py)/rng*N/2)
    for x,y in zs:spr(m,*pt(x,y),'3',6.4*k,(1,.13,.1))
    spr(m,N/2,N/2,'4',13*k)
    d=ImageDraw.Draw(m)
    for t,X,Y in(('N',N/2,29),('S',N/2,N-29),('E',N-29,N/2),('O',29,N/2)):d.text((X,Y),t,font=F(15*k),fill=Y_,anchor='mm')
    o=Image.new('RGBA',(N+12,N+12+170),(24,28,33,255));d=ImageDraw.Draw(o)
    d.rectangle((0,0,N+11,N+11),fill=(140,191,204));o.paste(m,(6,6))
    d.rectangle((0,N+24,N+11,N+105),fill=(10,15,20));d.text((N/4,N+64),'ZOMBIS 12',font=F(44),fill=(255,89,77),anchor='mm');d.text((N*.75,N+56),'VIDA 100',font=F(44),fill='white',anchor='mm');d.rectangle((N/2+12,N+88,N-6,N+97),fill=(77,230,102))
    d.rectangle((0,N+115,N+11,N+170),fill=(10,15,20));d.text((N/2,N+143),place,font=F(38),fill=col,anchor='mm')
    return o
B=960
def bigm(crazy,px,py,zs):
    m=Image.new('RGBA',(B,B),(8,11,15,255));ox,oy,sp=(10464,-7788,2700) if crazy else (128,808,10000);f=B/sp
    pt=lambda x,y:((x-ox)*f+B/2,(oy-y)*f+B/2);d=ImageDraw.Draw(m,'RGBA')
    if crazy:layer(m,atlas,6455.1,-3779.1,12020.9,ox,oy,sp/2,1)
    else:
        layer(m,base,128,808,10000,ox,oy,sp/2,1);U=10000/1024
        for n,l,r,b,t in caves:
            u=under[n-1];c=atlas.crop([round(v) for v in(1024+(l-u[0])/U,1024-(t-u[1])/U,1024+(r-u[0])/U,1024-(b-u[1])/U)])
            X0,Y0=pt(l,t);X1,Y1=pt(r,b);m.alpha_composite(fade(c.resize((round(X1-X0),round(Y1-Y0)),Image.BILINEAR),.9),(round(X0),round(Y0)))
        for x,y,t,r,g,b in lab:
            X,Y=pt(int(x),int(y));w=(len(t)*2.7+4)*1.5;d.rectangle((X-w,Y-10,X+w,Y+10),fill=(5,8,10,191));d.text((X,Y),t,font=F(13.5),anchor='mm',fill=tuple(int(float(v)*255) for v in(r,g,b)) if r else (255,242,204))
    for x,y in zs:spr(m,*pt(x,y),'3',10,(1,.13,.1))
    spr(m,*pt(px,py),'4',24)
    for t,X,Y in(('N',B/2,18),('S',B/2,B-18),('E',B-18,B/2),('O',18,B/2)):d.text((X,Y),t,font=F(22),fill=Y_,anchor='mm')
    o=Image.new('RGBA',(B+6,B+6),(140,191,204,255));o.paste(m,(3,3));return o
W=40+652+40+966+40;H=2*(966+90)+20
im=Image.new('RGBA',(W,H),(24,28,33,255));d=ImageDraw.Draw(im)
ice=((1423,-1800),[(1430,-1620),(1440,-2250),(1520,-2400)]);cz=((10464,-7900),[(10100,-7700),(10900,-8300),(10700,-7350),(9800,-8300)])
for r,(n,cr,(p,z),pl,c) in enumerate((('CUEVA DE HIELO',0,ice,'CUEVA DE HIELO',(102,204,255)),('CRAZY PLACE',1,cz,'CRAZY PLACE',(255,242,204)))):
    y=70+r*1056
    d.text((40,y-30),n+' · minimapa',font=F(32),fill='white',anchor='lm');d.text((732,y-30),n+' · mapa grande (M)',font=F(32),fill='white',anchor='lm')
    im.paste(mini(cr,*p,z,pl,c),(40,y));im.paste(bigm(cr,*p,z),(732,y))
im.convert('RGB').save(O)
