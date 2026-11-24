import sys,re
from PIL import Image,ImageDraw,ImageFont
S,L,O=sys.argv[1:4]
src=open(L,encoding='utf8').read();blk=src[src.index('MM.BigLabels'):];blk=blk[:blk.index('\n}')]
lab=re.findall(r'\{ (-?\d+), (-?\d+), "([^"]+)"(?:, ([\d.]+), ([\d.]+), ([\d.]+))? \}',blk)
W,H=1920,1080;k=1.5;F=lambda s:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',int(s*k))
im=Image.new('RGBA',(W,H),(32,35,36,255));d=ImageDraw.Draw(im,'RGBA')
f=480;cx,cy=W//2,H//2
d.rectangle((cx-f-3,cy-f-3,cx+f+3,cy+f+3),fill=(140,191,204));d.rectangle((cx-f,cy-f,cx+f,cy+f),fill=(8,11,15))
im.alpha_composite(Image.open(S+'/mm/base11.png').resize((960,960),Image.BILINEAR),(cx-f,cy-f))
pt=lambda x,y:(cx+(x-128)*.096,cy+(808-y)*.096)
ub=src[src.index('MM.Under = {'):];under=[tuple(map(float,t)) for t in re.findall(r'\{ (-?[\d.]+), (-?[\d.]+) \}',ub[:ub.index('\n}')])]
cb=src[src.index('MM.BigCaves'):];at=Image.open(S+'/mm/atlas11.png').convert('RGBA');tint={3:(190,110,255),4:(235,225,120),5:(90,200,255),6:(255,90,50)}
for q in re.findall(r'\{ (\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) \}',cb[:cb.index('\n}')]):
    n,l,r,b,t=map(int,q);U=10000/1024;ux,uy=under[n-1];c=at.crop([round(v) for v in(1024+(l-ux)/U,1024-(t-uy)/U,1024+(r-ux)/U,1024-(b-uy)/U)])
    R,G,B_,Al=c.split();lum=Image.merge('RGB',(R,G,B_)).convert('L')
    c=Image.merge('RGBA',[lum.point(lambda v,m=m:min(255,int(m*min(1.15,max(.5,v/110))))) for m in tint[n]]+[Al.point(lambda v:int(v*.9))])
    X0,Y0=pt(l,t);X1,Y1=pt(r,b);im.alpha_composite(c.resize((round(X1-X0),round(Y1-Y0)),Image.BILINEAR),(round(X0),round(Y0)))
for x,y,t,r,g,b in lab:
    X,Y=pt(int(x),int(y));w=(len(t)*2.7+4)*k
    d.rectangle((X-w,Y-7*k,X+w,Y+7*k),fill=(5,8,10,191))
    d.text((X,Y),t,font=F(9),anchor='mm',fill=tuple(int(float(v)*255) for v in (r,g,b)) if r else (255,242,204))
IC={n:Image.open(__import__('os').environ['MM_DOCS']+'/hud_zombierank_%s_ded.png'%n) for n in '345'}
def spr(x,y,n,s,c=(1,1,1),rot=0):
    q=IC[n].resize((int(s*k),)*2,Image.BILINEAR).rotate(rot,resample=Image.BILINEAR,expand=True);R,G,B,A=q.split()
    q=Image.merge('RGBA',[z.point(lambda v,m=m:int(v*m)) for z,m in zip((R,G,B),c)]+[A]);X,Y=pt(x,y);im.alpha_composite(q,(int(X-q.width/2),int(Y-q.height/2)))
for x,y in((300,2200),(520,2330),(1180,1900),(-600,2850),(1150,2500),(-100,900),(-1250,200)):spr(x,y,'3',7,(1,.13,.1))
spr(250,2450,'5',18);spr(1400,900,'4',14,(1,.85,.2),-120);spr(-80,2550,'4',16)
for t,X,Y in(('N',cx,cy-f+18),('S',cx,cy+f-18),('E',cx+f-18,cy),('O',cx-f+18,cy)):d.text((X,Y),t,font=F(15),fill=(255,217,77),anchor='mm')
im.convert('RGB').save(O)
