import sys,re,os,shutil
T=sys.argv[1];M=T+'/mods/zm_minimapa';lp=M+'/ui_mp/t6/zombie/hudtimerzombie.lua';s=open(lp,newline='').read()
a='\troot:registerEventHandler("mm_tick", MM.Update)';assert s.count(a)==1
s=s.replace(a,'''	-- legend, left of the full map
	local lg = group(big, 10, 1)
	bar(lg, -628, -318, -334, 196, 0.03, 0.045, 0.06, 0.92)
	bar(lg, -628, -318, -334, -316, 0.55, 0.75, 0.8, 0.9)
	local function words(t, x, y, size, r, g, b)
		local e = LUI.UIText.new()
		e:setLeftRight(false, false, x, x + 250)
		e:setTopBottom(false, false, y - size / 2, y + size / 2)
		e:setFont(CoD.fonts.Default)
		e:setAlignment(LUI.Alignment.Left)
		e:setText(t)
		e:setRGB(r, g, b)
		lg:addElement(e)
	end
	words("SIGNIFICADO", -614, -301, 18, 1, 0.85, 0.3)
	local function ring(e, r, cr, cg, cb)
		dot(e, r, cr, cg, cb)
		dot(e, r - 1.8, 0.07, 0.09, 0.12)
	end
	local function letter(e, l, cr, cg, cb)
		local q = text(e, 11, 1.5)
		q:setText(l)
		q:setRGB(cr, cg, cb)
	end
	local rows = {
		{ "Tu", function(e) image(e, MM.ArrowMat, 18, 1, 1, 1, 1) end },
		{ "Otro jugador (un color cada uno)", function(e) image(e, MM.ArrowMat, 16, 1, 0.85, 0.2, 1) end },
		{ "Zombi", function(e) dot(e, 3.5, 1, 0.13, 0.1) end },
		{ "Panzer Soldat", function(e) image(e, MM.PanzerMat, 20, 1, 1, 1, 1) end },
		{ "Zona donde pisa un robot", function(e)
			ring(e, 7.5, 1, 0.65, 0.15)
			bar(e, -3.4, -3, -0.8, 3, 1, 0.68, 0.23, 1)
			bar(e, 0.8, -3, 3.4, 3, 1, 0.68, 0.23, 1)
		end },
		{ "Pie de robot", function(e) dot(e, 6, 1, 0.8, 0.15) end },
		{ "Pie bajando: sal de ahi", function(e) dot(e, 6, 1, 0.12, 0.08) end },
		{ "Generador", function(e) ring(e, 7, 0.95, 0.95, 0.95) letter(e, "G", 1, 1, 1) end },
		{ "Generador capturado", function(e)
			bar(e, -5, -5, 5, 5, 0, 0, 0, 1)
			bar(e, -4, -4, 4, 4, 0.15, 0.85, 0.3, 1)
		end },
		{ "Caja misteriosa", function(e) dot(e, 7, 0.08, 0.1, 0.13) letter(e, "B", 0.3, 0.85, 1) end },
		{ "Pack-a-Punch", function(e) ring(e, 7, 1, 0.5, 0.9) letter(e, "P", 1, 0.5, 0.9) end },
		{ "Wunderfizz (ventaja al azar)", "W" },
		{ "Juggernog", "J" },
		{ "Quick Revive", "R" },
		{ "Speed Cola", "S" },
		{ "Stamin-Up", "M" },
		{ "Mule Kick (en la cripta)", "K" },
		{ "Baston (cripta y Crazy Place)", function(e)
			ring(e, 7.5, 0.35, 0.78, 1)
			local st = bar(e, -0.8, -4.5, 0.8, 4.5, 0.92, 0.88, 0.8, 1)
			st:setZRot(-45)
			oval(e, 1, -5, 4.6, -1.4, 0.35, 0.78, 1)
		end },
		{ "Portal (Crazy Place)", function(e)
			dot(e, 7.5, 0.76, 0.45, 1)
			dot(e, 5, 0.07, 0.09, 0.12)
			dot(e, 2.4, 0.76, 0.45, 1)
		end },
	}
	for i = 1, #rows do
		local y = -273 + (i - 1) * 25
		local e
		if type(rows[i][2]) == "string" then
			e = fixedIcon(lg, rows[i][2], 1)
			e:setAlpha(1)
		else
			e = group(lg, 7, 1)
			rows[i][2](e)
		end
		place(e, -604, y, 7, 0)
		words(rows[i][1], -584, y, 14, 0.92, 0.94, 0.95)
	end

'''+a)
t=re.sub('--.*','',re.sub('"[^"]*"','',s));x,y=len(re.findall(r'\b(function|if|do)\b',t)),len(re.findall(r'\bend\b',t));print(x,y);assert x==y
for q in('()','{}','[]'):assert t.count(q[0])==t.count(q[1])
R=T+'/respaldo_hud/zm_minimapa_v17';assert not os.path.exists(R);shutil.copytree(M,R)
with open(lp,'w',newline='') as f:f.write(s)
print('instalado')
