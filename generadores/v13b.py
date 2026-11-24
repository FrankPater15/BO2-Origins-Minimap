import sys,re,os
import numpy as np
from PIL import Image
S,M=sys.argv[1:3];lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
s=open(lp,newline='').read();U=10000/1024
def rep(a,c):
    global s
    assert s.count(a)==1,(s.count(a),a);s=s.replace(a,c)
blk=s[s.index('MM.Under = {'):];under=[tuple(map(float,t)) for t in re.findall(r'\{ (-?[\d.]+), (-?[\d.]+) \}',blk[:blk.index('\n}')])]
A=np.array(Image.open(S+'/mm/atlas11.png'));rows=''
for i,n in((2,'rayo'),(3,'viento'),(4,'hielo'),(5,'fuego')):
    cx,cy=round(((i%3)+.5)*2048/3),round(((i//3)+.5)*2048/3)
    ys,xs=np.where(A[cy-160:cy+160,cx-160:cx+160,3]>10);ys+=cy-160;xs+=cx-160
    wx=lambda p:under[i][0]+(p-1024)*U
    wy=lambda p:under[i][1]-(p-1024)*U
    l,r,t,b=wx(xs.min()-2),wx(xs.max()+3),wy(ys.min()-2),wy(ys.max()+3)
    print(n,[round(v) for v in(l,r,b,t)]);rows+='\t{ %d, %d, %d, %d, %d },\n'%(i+1,l,r,b,t)
rep('MM.BigLabels = {\n','-- caves drawn whole on the full map: atlas tile, left, right, bottom, top (world)\nMM.BigCaves = {\n'+rows+'}\nMM.BigLabels = {\n')
rep('{ 2500, -1850, "CUEVA DE HIELO"','{ 2340, -2000, "CUEVA DE HIELO"')
rep('{ 3850, 4450, "CUEVA DE FUEGO"','{ 3930, 4450, "CUEVA DE FUEGO"')
rep('{ -3500, -850, "CUEVA DE RAYO"','{ -3250, -850, "CUEVA DE RAYO"')
rep('{ 3350, 1750, "CUEVA DE VIENTO"','{ 3350, 1780, "CUEVA DE VIENTO"')
rep('\tbig.labels = group(view, frame, 1)\n','''	-- each cave: a small clip box showing only its own tile of the atlas
	big.caves = group(big, frame, 1)
	local bk = MM.BigSize / MM.World
	for i = 1, #MM.BigCaves do
		local d = MM.BigCaves[i]
		local mx, my = (d[2] + d[3]) / 2, (d[4] + d[5]) / 2
		local box = group(big.caves, 10, 1)
		box:setLeftRight(false, false, (d[2] - MM.CenterX) * bk, (d[3] - MM.CenterX) * bk)
		box:setTopBottom(false, false, (MM.CenterY - d[5]) * bk, (MM.CenterY - d[4]) * bk)
		box:setUseStencil(true)
		local img = image(box, MM.CrazyMaterial, MM.UnderWorld * bk, 1, 1, 1, 0.9)
		local un = MM.Under[d[1]]
		place(img, (un[1] - mx) * bk, (my - un[2]) * bk, MM.UnderWorld * bk / 2, 0)
	end
	-- everything on top of the caves
	view = group(big, frame, 1)
	big.labels = group(view, frame, 1)
''')
rep('\tshow(big.labels, crazy and 0 or 1)\n','\tshow(big.labels, crazy and 0 or 1)\n\tshow(big.caves, crazy and 0 or 1)\n')
t=re.sub('--.*','',re.sub('"[^"]*"','',s))
assert len(re.findall(r'\b(function|if|do)\b',t))==len(re.findall(r'\bend\b',t))
for x in('()','{}','[]'):assert t.count(x[0])==t.count(x[1])
with open(lp,'w',newline='') as f:f.write(s)
print('ok')
