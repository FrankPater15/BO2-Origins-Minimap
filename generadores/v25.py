"""v25: attacked generator on top of zombies, fitted name plates, crypt ring without tips. usage: T [install]"""
import sys,os,re,shutil
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';G=os.path.dirname(os.path.abspath(__file__))+'/'
lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';s=open(lp,newline='').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a);s=s.replace(a,b)
# 1. one extra badge above the zombies, only for the generator in danger
R('	local key = st .. (st == 1','	local key = f[3] .. st .. (st == 1')
R('	for i = ai + 1, MM.MaxAllies do\n		show(self.allies[i], 0)','''	-- generator in danger, drawn over the zombies
	local alertFix = not crazy and self.alert and MM.GenFix and MM.GenFix[self.alert]
	if alertFix then
		dressGen(self.alertGen, alertFix, self.gens, self.packet)
		local ex, ey = project(alertFix[1], alertFix[2])
		place(self.alertGen, math.max(-half + 11, math.min(half - 11, ex)), math.max(-half + 11, math.min(half - 11, ey)), 7, 0)
		show(self.alertGen, 1)
	else
		show(self.alertGen, 0)
	end
	for i = ai + 1, MM.MaxAllies do
		show(self.allies[i], 0)''')
R('	for i = ai + 1, MM.MaxAllies do\n		show(big.allies[i], 0)','''	local alertFix = not crazy and self.alert and MM.GenFix and MM.GenFix[self.alert]
	if alertFix then
		dressGen(big.alertGen, alertFix, self.gens, self.packet)
		put(big.alertGen, alertFix[1], alertFix[2], 7)
	else
		show(big.alertGen, 0)
	end
	for i = ai + 1, MM.MaxAllies do
		show(big.allies[i], 0)''')
R('	root.fixed = {}\n','''	MM.GenFix = {}
	for i = 1, #MM.Fixed do
		if string.sub(MM.Fixed[i][3], 1, 1) == "G" then
			MM.GenFix[MM.Fixed[i][3]] = MM.Fixed[i]
		end
	end
	root.fixed = {}
''')
a='	-- you: smaller than before';assert s.count(a)==1
R(a,'	root.alertGen = fixedIcon(clip, "G1", 1)\n'+a)
R('	big.me = image(view, MM.ArrowMat','	big.alertGen = fixedIcon(view, "G1", 0.95)\n	big.me = image(view, MM.ArrowMat')
# 2. plates fitted to the real font (measured in game), slightly bigger text
R('string.len(d[3]) * 2.7 + 4','string.len(d[3]) * 2.2 + 4')
R('bar(e, -w, -7, w, 7, 0.02','bar(e, -w, -7.5, w, 7.5, 0.02')
R('local t = text(e, 11, 74)','local t = text(e, 13, 73)')
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x,y=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print(x,y);assert x==y
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1])
# 3. crypt ring
p=G+'v24b_extra.txt';e=open(p,encoding='utf8').read();a="cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(75,75)));mm[hole>0]=0"
if a in e:
    e=e.replace(a,"cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(75,75)));hull=cv2.convexHull(np.argwhere(mm>0)[:,::-1].astype(np.int32));cv2.fillConvexPoly(mm,hull,1);mm[hole>0]=0").replace('(0,0),7)>.5','(0,0),9)>.5')
    open(p,'w',encoding='utf8',newline='\n').write(e)
if go:
    b=T+'/respaldo_hud/zm_minimapa_v24';assert not os.path.exists(b);shutil.copytree(M,b)
    with open(lp,'w',newline='') as fh:fh.write(s)
    print('instalado')
