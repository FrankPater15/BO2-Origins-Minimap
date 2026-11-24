src=open(__import__('sys').argv[1]+'/mm/v11.py',encoding='utf8').read().split('icons(base,items,tr); base.save')[0]
exec(src)  # own generator code, up to before anything is written
N=2048;tr=lambda x,y:((x-128)/10000*N+N/2,N/2-(y-808)/10000*N)
im=Image.new('RGBA',(N,N),(10,14,18,255))
im.alpha_composite(Image.open(Q+'surf11.png').resize((N,N),Image.LANCZOS))
# tint every cave by element
u=np.array(Image.open(Q+'und11.png').resize((N,N),Image.LANCZOS));al=u[...,3]
mask=cv2.resize(um.astype(np.uint8)*255,(N,N),interpolation=cv2.INTER_AREA)
n,lab=cv2.connectedComponents((mask>110).astype(np.uint8))
E_={'FUEGO':((2930,4400),(255,90,50)),'HIELO':((1423,-1690),(90,200,255)),'VIENTO':((3350,1250),(235,225,120)),'RAYO':((-3270,-300),(190,110,255))}
out=np.zeros((N,N,4),np.uint8);ys,xs=np.where(lab>0)
for nm,((x,y),c) in E_.items():
    X,Y=tr(x,y);k=((xs-X)**2+(ys-Y)**2).argmin();l=lab[ys[k],xs[k]];print(nm,'dist px',((xs[k]-X)**2+(ys[k]-Y)**2)**.5,'area',(lab==l).sum())
    m=cv2.GaussianBlur((lab==l).astype(np.float32),(0,0),1.2);lum=u[...,:3].mean(2)/110.
    for q in range(3):
        out[...,q]=np.where(m>.02,np.clip(c[q]*np.clip(lum,.55,1.1),0,255),out[...,q])
    out[...,3]=np.maximum(out[...,3],(m*235).astype(np.uint8))
im.alpha_composite(Image.fromarray(out))
K=2;icons(im,items,tr)
d=ImageDraw.Draw(im)
def f(s,b=True):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),s)
def label(x,y,t,c=(255,255,255),s=25,to=None):
    X,Y=tr(x,y)
    if to:
        P=tr(*to);d.line((X,Y)+P,fill=c+(255,),width=3);d.ellipse((P[0]-6,P[1]-6,P[0]+6,P[1]+6),fill=c+(255,))
    b=d.multiline_textbbox((X,Y),t,font=f(s),anchor='mm',align='center');d.rounded_rectangle((b[0]-11,b[1]-7,b[2]+11,b[3]+7),8,fill=(8,11,15,255),outline=c+(255,),width=2)
    d.multiline_text((X,Y),t,font=f(s),fill=c+(255,),anchor='mm',align='center')
W=(240,240,235);T=(255,215,130)
label(1700,5600,'LABORATORIO\n(inicio)',W,to=(2650,5350))
label(-3050,4500,'ESTACIÓN DEL TANQUE\n(búnker)',W,to=(-273,4537))
label(-3400,3350,'BÚNKER DEL TANQUE · G2',W,to=(-450,3480))
label(-2900,2350,'TRINCHERA CENTRAL · G3',W,to=(400,2250))
label(3400,2600,'TRINCHERAS',W,to=(2300,3050))
label(1500,-5 +1650,'TIERRA DE NADIE',T,to=(1300,900))
label(-2700,1650,'TIERRA DE NADIE',T,to=(-1250,700))
label(-100,-560,'MID · EXCAVACIÓN\n(Pack-a-Punch arriba, cripta abajo)',(255,150,230),22,to=(0,0))
label(4050,-300,'ZONA DE JUGGERNOG\nG4',W,23,to=(2700,330))
label(-3900,750,'GRANJA\nG5',W,23,to=(-2500,560))
label(-2550,-2500,'ALDEA',T,to=(-500,-2420))
label(-2550,-3000,'ESTACIÓN DEL TANQUE\n(iglesia)',W,23,to=(377,-2880))
label(2700,-2750,'IGLESIA',T,30,to=(608,-2652))
label(2500,-3850,'DETRÁS DE LA IGLESIA\nG6',W,23,to=(1000,-3850))
label(4050,4150,'CUEVA DE FUEGO',E_['FUEGO'][1],27,to=(2930,4400))
label(3900,1850,'CUEVA DE VIENTO',E_['VIENTO'][1],27,to=(3350,1250))
label(-3600,-1150,'CUEVA DE RAYO',E_['RAYO'][1],27,to=(-3270,-330))
label(2950,-1850,'CUEVA DE HIELO',E_['HIELO'][1],27,to=(1423,-1690))
x0,x1=tr(-4850,0)[0],tr(4980,0)[0]
im.crop((int(x0),0,int(x1),N)).convert('RGB').save(sys.argv[3] if 0 else sys.argv[4])
