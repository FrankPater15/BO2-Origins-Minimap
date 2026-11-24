import sys,zipfile,os
m=sys.argv[1]
with zipfile.ZipFile(m+'/mod.iwd','w',zipfile.ZIP_DEFLATED) as z:
    for d in('ui_mp','images'):
        for r,_,fs in os.walk(m+'/'+d):
            for f in fs: p=os.path.join(r,f); z.write(p,os.path.relpath(p,m))
    print(z.namelist())
