import re,json
d=open('../agent_lui/ff/zm_tomb.bin','rb').read()
i=d.find(b'"classname" "worldspawn"'); print(i)
j=d.rfind(b'{',0,i); e=d.find(b'\0',i); t=d[j:e].decode('latin1'); print(len(t))
E=[dict(re.findall(r'"([^"]*)"\s+"([^"]*)"',b)) for b in re.findall(r'\{([^{}]*)\}',t)]
json.dump(E,open('ents.json','w')); print(len(E))
for x in E:
    s=' '.join(x.values()).lower()
    if any(k in s for k in('vending','perk','generator_','zombie_chest','magic_box','random_perk','pap','zm_perk','capture')) : print({k:v for k,v in x.items() if k in('classname','targetname','script_noteworthy','origin','model','script_string')})
