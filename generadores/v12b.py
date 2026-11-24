import sys,re
M=sys.argv[1];lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua'
s=open(lp,newline='').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a;s=s.replace(a,b)
i=s.index('\t-- north marker');j=s.index('\tlocal half = MM.Size / 2\n',i)
s=s[:i]+'''	-- compass letters, sliding along the square border: N, E, S, O
	for i = 1, 4 do
		local nx, ny = -c, -s
		if i == 2 then
			nx, ny = s, -c
		elseif i == 3 then
			nx, ny = c, s
		elseif i == 4 then
			nx, ny = -s, c
		end
		local k = (MM.Size / 2 - 9) / math.max(math.abs(nx), math.abs(ny))
		place(self.compass[i], nx * k, ny * k, i == 1 and 8 or 7, 0)
	end

'''+s[j:]
i=s.index('\troot.north = LUI.UIText.new()');j=s.index('\t-- info panel under the map')
s=s[:i]+'''	root.compass = {}
	local letters = { "N", "E", "S", "O" }
	for i = 1, 4 do
		local e = LUI.UIText.new()
		e:setFont(CoD.fonts.Default)
		e:setAlignment(LUI.Alignment.Center)
		e:setText(letters[i])
		if i == 1 then
			e:setRGB(1, 0.85, 0.3)
		else
			e:setRGB(1, 0.85, 0.3)
		end
		root:addElement(e)
		root.compass[i] = e
	end

'''+s[j:]
assert 'north' not in s.replace('-- north','')
t=re.sub('--.*','',re.sub('"[^"]*"','',s))
assert len(re.findall(r'\b(function|if|do)\b',t))==len(re.findall(r'\bend\b',t))
for a,b in('()','{}'):assert t.count(a)==t.count(b)
open(lp,'w',newline='\n').write(s);print('ok')
