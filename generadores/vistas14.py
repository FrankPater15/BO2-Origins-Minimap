import sys
S,L,O=sys.argv[1:4]
s=open(__import__('os').environ['MM_DOCS']+'/generadores/vistas.py',encoding='utf8').read()
i=s.index('for i,t in {2:');j=s.index('def fade');s=s[:i]+s[j:]
s=s.replace("S+'/mm/atlas11.png'","D+'generadores/atlas14.png'")
import re
src=open(L,encoding='utf8').read();v={k:float(re.search(r'(?m)^MM\.%s = (\S+)'%k,src).group(1)) for k in('CrazyX','CrazyY','CrazyWorld')}
s=s.replace('6455.1,-3779.1,12020.9','%f,%f,%f'%(v['CrazyX'],v['CrazyY'],v['CrazyWorld']))
s=s.replace("rng=900 if crazy else 1750","part=place_part(place);rng=900 if crazy else (750 if part==2 else 1000)").replace("u=under[4];layer(m,atlas,u[0],u[1],20000","u=under[part-1];layer(m,atlas,u[0],u[1],10000")
s=s.replace("def mini(","place_part=lambda p:{'CRIPTA':2,'CUEVA DE HIELO':5}.get(p,0)\ndef mini(")
s=s.replace("def bigm(crazy,px,py,zs):","def bigm(crazy,px,py,zs,part=0):").replace("layer(m,base,128,808,10000,ox,oy,sp/2,1);U=10000/1024","layer(m,base,128,808,10000,ox,oy,sp/2,.3 if part else 1);U=10000/2048")
s=s.replace("            u=under[n-1];c=atlas","            if (n!=part) if part else not 3<=n<=6: continue\n            u=under[n-1];c=atlas")
i=s.index('W=40+652');s=s[:i]+'''
W=40+652+40+966+40;H=3*1056+10
im=Image.new('RGBA',(W,H),(24,28,33,255));d=ImageDraw.Draw(im)
for r,(p,z,cr,pl,c) in enumerate((((60,-250),[(250,60),(-60,-330)],0,'CRIPTA',(77,242,204)),((1423,-1800),[(1430,-1620),(1440,-2250)],0,'CUEVA DE HIELO',(102,204,255)),((10340,-7906),[(9850,-7500),(10900,-8300)],1,'CRAZY PLACE',(217,166,255)))):
    y=70+r*1056
    d.text((40,y-30),pl+' · minimapa',font=F(32),fill='white',anchor='lm');d.text((732,y-30),pl+' · mapa grande (M)',font=F(32),fill='white',anchor='lm')
    im.paste(mini(cr,*p,z,pl,c),(40,y));im.paste(bigm(cr,*p,z,place_part(pl)),(732,y))
im.convert('RGB').save(O)
'''
exec(s)
