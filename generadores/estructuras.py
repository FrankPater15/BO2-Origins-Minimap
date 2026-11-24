import sys,re
S,L,O=sys.argv[1:4]
import numpy as np
from PIL import Image,ImageDraw,ImageFont
D=__import__('os').environ['MM_DOCS']+'/';src=open(L,encoding='utf8').read()
def sec(n):
    b=src[src.index(n):];return b[:b.index(chr(10)+'}')]
und=[(float(a),float(b),int(c)) for a,b,c in re.findall(r'[{] (-?[0-9.]+), (-?[0-9.]+), ([12]) [}]',sec('MM.Under = {'))]
box=[tuple(map(int,t)) for t in re.findall(r'[{] ([0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+) [}]',sec('MM.BigCaves = {'))]
base=Image.open(S+'/mm/base11.png').convert('RGBA');at=[Image.open(D+'generadores/atlas15_%d.png'%i).convert('RGBA') for i in(1,2)]
F=lambda s:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',s)
NAM={1:'CRIPTA',2:'CUEVA DE RAYO',3:'CUEVA DE VIENTO',4:'CUEVA DE HIELO',5:'CUEVA DE FUEGO',6:'IGLESIA / ALDEA',7:'LABORATORIO + G1',8:'BUNKER OESTE',9:'TRINCHERA ESTE',10:'GRANJA - G5',11:'ESTACION DEL TANQUE',12:'PASO JUNTO AL TANQUE',13:'PASILLO DE G2 A G3',14:'PASILLO AL SUR DE G3',15:'TRINCHERA SURESTE'}
CO={1:(77,242,204),2:(204,128,255),3:(242,230,128),4:(102,204,255),5:(255,102,64)}
N=420;ar=Image.open(D+'hud_zombierank_4_ded.png').resize((27,27),Image.BILINEAR)
def lay(dst,im,mx,my,w,cx,cy,r,a):
    n=im.width;u=w/n
    q=im.transform((N,N),Image.EXTENT,((cx-r-mx)/u+n/2,n/2-(cy+r-my)/u,(cx+r-mx)/u+n/2,n/2-(cy-r-my)/u),Image.BILINEAR)
    q.putalpha(q.getchannel('A').point(lambda v:int(v*a)));dst.alpha_composite(q)
W=5*(N+30)+30;H=3*(N+110)+20;im=Image.new('RGBA',(W,H),(24,28,33,255))
for i in range(15):
    p=i+1;ux,uy,a=und[i];_,l,r,b,t=box[i];A=np.array(at[a-1]);U=10000/2048
    X0,X1,Y0,Y1=[int(v) for v in(1024+(l-ux)/U,1024+(r-ux)/U,1024-(t-uy)/U,1024-(b-uy)/U)]
    al=A[Y0:Y1,X0:X1,3]>200;ys,xs=np.where(al);k=((ys-ys.mean())**2+(xs-xs.mean())**2).argmin()
    px,py=ux+(X0+xs[k]-1024)*U,uy-(Y0+ys[k]-1024)*U
    rg=750 if p==1 else 1000 if p<6 else 1300
    m=Image.new('RGBA',(N,N),(22,30,36,255));lay(m,base,128,808,10000,px,py,rg,.3);lay(m,at[a-1],ux,uy,10000,px,py,rg,.95)
    m.alpha_composite(ar,(N//2-13,N//2-13));d=ImageDraw.Draw(m)
    for q,x,y in(('N',N/2,18),('S',N/2,N-18),('E',N-18,N/2),('O',18,N/2)):d.text((x,y),q,font=F(26),fill=(255,217,77),anchor='mm')
    x=30+(i%5)*(N+30);y=20+(i//5)*(N+110);d=ImageDraw.Draw(im);d.rectangle((x-4,y-4,x+N+3,y+N+3),fill=(140,191,204));im.paste(m,(x,y))
    d.rectangle((x-4,y+N+10,x+N+3,y+N+60),fill=(10,15,20));d.text((x+N/2,y+N+35),'%d · %s'%(p,NAM[p]),font=F(27),fill=CO.get(p,(255,200,120)),anchor='mm')
im.convert('RGB').save(O)
