import sys,re
L,O=sys.argv[1:3]
from PIL import Image,ImageDraw,ImageFont
D=__import__('os').environ['MM_DOCS']+'/';src=open(L,encoding='utf8').read()
def sec(n):
    b=src[src.index(n):];return b[:b.index(chr(10)+'}')]
num='(-?[0-9.]+)'
und=[(float(a),float(b),int(c)) for a,b,c in re.findall('[{] %s, %s, ([12]) [}]'%(num,num),sec('MM.Under = {'))]
box=[tuple(map(int,t)) for t in re.findall('[{] ([0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+) [}]',sec('MM.BigCaves = {'))]
lab=re.findall(r'[{] (-?[0-9]+), (-?[0-9]+), "([^"]+)"(?:, ([0-9.]+), ([0-9.]+), ([0-9.]+))? [}]',sec('MM.BigLabels'))
fix=re.findall(r'[{] (-?[0-9]+), (-?[0-9]+), "([^"]+)" [}]',sec('MM.Fixed = {'))
Z=2;N=960*Z;k=1.5*Z;F=lambda s:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',int(s*k))
im=Image.new('RGBA',(N,N),(8,11,15,255));im.alpha_composite(Image.open(D+'generadores/base17.png').resize((N,N),Image.BILINEAR))
pt=lambda x,y:((x-128)*N/10000+N/2,(808-y)*N/10000+N/2);U=10000/2048
at=[Image.open(D+'generadores/atlas16_%d.png'%i).convert('RGBA') for i in(1,2)]
for n,l,r,b,t in box:
    if not 2<=n<=5:continue
    ux,uy,a=und[n-1];c=at[a-1].crop([round(v) for v in(1024+(l-ux)/U,1024-(t-uy)/U,1024+(r-ux)/U,1024-(b-uy)/U)])
    X0,Y0=pt(l,t);X1,Y1=pt(r,b);c=c.resize((round(X1-X0),round(Y1-Y0)),Image.BILINEAR);c.putalpha(c.getchannel('A').point(lambda v:int(v*.9)));im.alpha_composite(c,(round(X0),round(Y0)))
d=ImageDraw.Draw(im,'RGBA')
for x,y,t,r,g,b in lab:
    X,Y=pt(int(x),int(y));w=(len(t)*2.7+4)*k;d.rectangle((X-w,Y-7*k,X+w,Y+7*k),fill=(5,8,10,191));d.text((X,Y),t,font=F(9),anchor='mm',fill=tuple(int(float(v)*255) for v in(r,g,b)) if r else (255,242,204))
PK={'J':(235,70,60),'R':(90,165,255),'S':(70,215,100),'M':(255,195,60)}
for x,y,t in fix:
    if t=='K':continue
    X,Y=pt(int(x),int(y));q=.95*k;ov=lambda l,tp,r,b,c:d.ellipse((X+l*q,Y+tp*q,X+r*q,Y+b*q),fill=c);br=lambda l,tp,r,b,c:d.rectangle((X+l*q,Y+tp*q,X+r*q,Y+b*q),fill=c)
    if t=='W':
        br(-2.6,-8,2.6,-3,(0,0,0));ov(-6.4,-5.2,6.4,8,(0,0,0));ov(-5,-3.8,5,6.5,(158,64,242));br(-1.8,-7.2,1.8,-3.2,(158,64,242));br(-2.6,-8.2,2.6,-6.6,(255,217,77));d.text((X,Y+1.4*q),'?',font=F(8),fill='white',anchor='mm')
    elif t in PK:
        z=int(19*q);ic=Image.open(D+'medir/perk2/specialty_%s_zombies.png'%{'J':'juggernaut','R':'quickrevive','S':'fastreload','M':'marathon'}[t]).resize((z,z),Image.LANCZOS);im.alpha_composite(ic,(int(X-z/2),int(Y-z/2)))
    else:
        ov(-7,-7,7,7,(0,0,0));ov(-6,-6,6,6,(240,240,240));ov(-4.9,-4.9,4.9,4.9,(18,23,30));d.text((X,Y),t,font=F(6.5),fill='white',anchor='mm')
for t,X,Y in(('N',N/2,36),('S',N/2,N-36),('E',N-36,N/2),('O',36,N/2)):d.text((X,Y),t,font=F(15),fill=(255,217,77),anchor='mm')
o=Image.new('RGB',(N+12,N+12),(140,191,204));o.paste(im.convert('RGB'),(6,6));o.save(O)
