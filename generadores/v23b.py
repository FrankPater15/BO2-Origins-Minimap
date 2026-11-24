import sys
lp=sys.argv[1];s=open(lp,newline='').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a);s=s.replace(a,b)
R('\tbig.labels = group(view, frame, 1)\n','\t-- pointers go under every name plate\n\tbig.lines = group(view, frame, 1)\n\tbig.labels = group(view, frame, 1)\n')
R('local line = bar(big.labels,','local line = bar(big.lines,');R('local tip = image(big.labels,','local tip = image(big.lines,')
R('\tshow(big.labels, crazy and 0 or 1)\n','\tshow(big.labels, crazy and 0 or 1)\n\tshow(big.lines, crazy and 0 or 1)\n')
open(lp,'w',newline='').write(s);print('ok')
