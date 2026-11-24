import sys,re,os,shutil
T=sys.argv[1];go=len(sys.argv)>2;M=T+'/mods/zm_minimapa';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';gp=M+'/scripts/zm/zm_tomb/minimapa_lui.gsc'
s=open(lp,newline='').read();g=open(gp,newline='').read()
def R(t,a,b,c=1):
    assert t.count(a)==c,(t.count(a),a);return t.replace(a,b)
i=s.index('\tlocal newYaw = yaw\n');j=s.index('\tlocal rad = yaw')
s=s[:i]+'''	-- measured on video: positions reach the screen one frame after setZRot, so the
	-- pictures are turned with an older yaw (mm_giro 1: one frame, 3: two frames)
	local turnYaw = yaw
	if self.giro == 1 then
		turnYaw = me.yaw1 or yaw
	elseif self.giro == 3 then
		turnYaw = me.yaw2 or me.yaw1 or yaw
	end
	me.yaw2 = me.yaw1
	me.yaw1 = yaw
'''+s[j:]
s=R(s,'e:setZRot((90 - newYaw) * rs)','e:setZRot((90 - turnYaw) * rs)');s=R(s,'self.spin:setZRot((90 - newYaw) * rs)','self.spin:setZRot((90 - turnYaw) * rs)')
assert 'newYaw' not in s
g=R(g,'\t// 100 unit cells; the offset keeps the values positive\n','''	// the dig site: every floor under the platform belongs to the crypt
	if ( org[ 2 ] < 250 && org[ 0 ] * org[ 0 ] + org[ 1 ] * org[ 1 ] < 230400 )
		return 1;
	// 100 unit cells; the offset keeps the values positive
''')
g=R(g,'0 plain, 1 compensate rotation delay, 2 container','0 plain, 1 turn pictures one frame later, 2 container, 3 two frames')
t=re.sub('--.*','',re.sub('"[^"]*"','',s));assert len(re.findall(r'\b(function|if|do)\b',t))==len(re.findall(r'\bend\b',t))
for q in('()','{}'):assert t.count(q[0])==t.count(q[1]) and g.count(q[0])==g.count(q[1])
print('verificado')
if go:
    b=T+'/respaldo_hud/zm_minimapa_v18';assert not os.path.exists(b);shutil.copytree(M,b)
    for p,v in((lp,s),(gp,g)):
        with open(p,'w',newline='') as f:f.write(v)
    print('instalado')
