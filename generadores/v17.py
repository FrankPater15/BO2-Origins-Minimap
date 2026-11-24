"""v17: base map with real depth (local height, ledges, ramps, wall shadow)"""
import sys,io,os,struct,shutil,json
S,T=sys.argv[1:3];install=len(sys.argv)>3;M=T+'/mods/zm_minimapa';Q=S+'/mm/';G=os.path.dirname(os.path.abspath(__file__))+'/';DOC=G+'../'
v15=open(G+'v15.py',encoding='utf8').read().split("AMB=(255")[0]
ar=sys.argv;sys.argv=['x',S,T];ns={'__file__':__file__};exec(compile(v15,'v15','exec'),ns);sys.argv=ar
import numpy as np,cv2
from PIL import Image
N=2048;U=10000/N;Y,X,wz,part=ns['Y'],ns['X'],ns['wz'],ns['part']
sm=np.load(Q+'sm.npy').astype(np.uint8)
k=~np.isin(part,(1,2,-2,3,4,5))
z=np.full((N,N),-9999.,np.float32);np.maximum.at(z,(Y[k],X[k]),wz[k].astype(np.float32))
ok=((z>-9000)&(sm>0)).astype(np.uint8)
# fill holes of the floor from the nearest known height
_,lbl=cv2.distanceTransformWithLabels(1-ok,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
val=np.zeros(lbl.max()+1,np.float32);yy,xx=np.where(ok>0);val[lbl[yy,xx]]=z[yy,xx];zf=val[lbl]
zf=cv2.medianBlur(zf,5)
f=sm.astype(np.float32)
def mblur(a,s):return cv2.GaussianBlur(a*f,(0,0),s)/np.maximum(cv2.GaussianBlur(f,(0,0),s),1e-4)
zs=mblur(zf,1.6)                      # removes the 12u voxel steps
# height relative to the surroundings (about 700u)
rel=zs-mblur(zf,120/U*3)
rel2=zs-mblur(zf,260/U)
# keep the soft north-south colour
t=np.clip((zs+330)/620,0,1)[...,None]
low=np.array([60,112,140],np.float32);mid=np.array([118,140,128],np.float32);high=np.array([196,176,124],np.float32)
col=np.where(t<.5,low+(mid-low)*t*2,mid+(high-mid)*(t*2-1))
br=1+np.clip(rel/150,-1,1)*.42+np.clip(rel2/90,-1,1)*.16
gy,gx=np.gradient(mblur(zf,2.2));sl=np.hypot(gx,gy)/U
br+=np.clip((gx+gy)*-.02,-.3,.3)
# wall shadow: corridors look sunk, from the north-west light
d=cv2.distanceTransform(sm,cv2.DIST_L2,5);br-=.22*np.exp(-d/5.)
sh=np.zeros_like(f)
for q in range(2,10,2):
    w=np.roll(np.roll(1-f,q,0),q,1);sh=np.maximum(sh,w*(1-q/13))
br-=.22*cv2.GaussianBlur(sh,(0,0),1.5)
# ledges: sudden drop that cannot be walked up (>30u within 15u)
hi=cv2.dilate(zf*f-9999*(1-f),np.ones((5,5)));lo=cv2.erode(zf*f+9999*(1-f),np.ones((5,5)))
drop=((hi-lo>34)&(hi>-5000)&(lo<5000)&(sm>0));er=cv2.erode(sm,np.ones((7,7)));drop&=er>0
drop&=~((sl<1.05)&(hi-lo<52))
low_side=drop&(zf-lo<(hi-lo)*.5)
upper=drop&~low_side
nc,l,st,_=cv2.connectedComponentsWithStats(drop.astype(np.uint8),connectivity=8);sm_=st[:,4]<60;sm_[0]=False;bad=sm_[l];low_side&=~bad;upper&=~bad
# shadow thrown on the lower floor
cast=cv2.GaussianBlur(cv2.dilate(low_side.astype(np.float32),np.ones((5,5))),(0,0),3.2)
lowmask=(zs<cv2.dilate(zs,np.ones((13,13)))-25)
br-=np.where(lowmask,np.clip(cast*1.1,0,.5),0)
# ramps and stairs: rungs across the slope
ramp=((sl>.22)&(sl<1.15)&(er>0)&~drop).astype(np.uint8)
ramp=cv2.morphologyEx(ramp,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
nc,l,st,_=cv2.connectedComponentsWithStats(ramp);b2=st[:,4]<150;b2[0]=False;ramp[b2[l]]=0
step=np.abs(((zs/22)%1)-.5)*2          # 1 at a contour
rung=(np.clip((step-.5)/.3,0,1)*ramp)
br-=rung*.2;br+=ramp*.05
out=col*np.clip(br,.28,1.32)[...,None]
out[upper]=out[upper]*.35+np.array([250,244,220])*.65
out[low_side]=out[low_side]*.35
out=np.clip(out,0,255)
aa=cv2.GaussianBlur(f,(0,0),.9);edge=np.clip(cv2.dilate(aa,np.ones((5,5)))-cv2.erode(aa,np.ones((3,3))),0,1)[...,None]
out=out*(1-edge*.8)+np.array([222,228,222])*edge*.8
al=np.clip(cv2.dilate(aa,np.ones((5,5))),0,1)
# soft dark halo behind the walls lifts the map off the background
halo=cv2.GaussianBlur(al,(0,0),7)*.75
A=np.clip(al+halo*(1-al),0,1);rgb=out*(al/np.maximum(A,1e-4))[...,None]
surf=Image.fromarray(np.dstack([rgb,A*255]).astype(np.uint8));surf.save(G+'surf17.png')
src=open(Q+'v11.py',encoding='utf8').read().split('icons(base,items,tr); base.save')[0].replace("Image.open(Q+'surf11.png')","Image.open(SURF)")
SURF=G+'surf17.png';sys.argv=['x',S,T,M];exec(src);sys.argv=ar
items=[i for i in items if i[2] in('foot','P')];icons(base,items,tr);base.save(G+'base17.png')
a=Image.new('RGB',(2068,1024),(8,11,15));n_=Image.new('RGBA',(1024,1024),(8,11,15,255));o_=n_.copy();o_.alpha_composite(Image.open(G+'base16.png'));n_.alpha_composite(base);a.paste(o_.convert('RGB'),(0,0));a.paste(n_.convert('RGB'),(1044,0))
a.crop((190,0,2068,1024)).save(DOC+'profundidad.png')
z_=Image.new('RGB',(1500,1500),(8,11,15))
for i,(im,) in enumerate(((o_,),(n_,))):
    for j,bx in enumerate(((380,400,680,700),(400,60,700,360))):z_.paste(im.convert('RGB').crop(bx).resize((740,740),Image.BICUBIC),(i*760,j*760))
z_.save(DOC+'profundidad_detalle.png');print('escalones',int(upper.sum()),'rampas',int(ramp.sum()))
if install:
    R=T+'/respaldo_hud/zm_minimapa_v16';assert not os.path.exists(R);shutil.copytree(M,R)
    with open(M+'/images/icon_twitter.iwi','rb') as fh:h=fh.read(64)
    b=io.BytesIO();base.save(b,format='DDS',pixel_format='DXT5');dd=b.getvalue();assert dd[84:88]==b'DXT5'
    for p in(M,T):
        with open(p+'/images/icon_twitter.iwi','wb') as fh:fh.write(h+dd[128:128+1024*1024])
    print('instalado')
