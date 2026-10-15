"""Usage: python3 dft/analysis/znl_stats.py <path to dft dir>"""
import os,json,math,sys,statistics as S,collections,csv
D=os.path.abspath(sys.argv[1]); X=next(p for p in [os.path.join(os.path.dirname(D),"structures","dft_ready_xyz"),os.path.join(os.path.dirname(D),"dft_ready_xyz")] if os.path.isdir(p))
def rx(p):
    L=open(p).read().split("\n"); n=int(L[0]); return [(l.split()[0],*map(float,l.split()[1:4])) for l in L[2:2+n]]
d=lambda a,b: math.dist(a[1:],b[1:])
rows=list(csv.DictReader(open(f"{D}/stage1_summary.csv")))
by=collections.defaultdict(list); per=[]
for r in rows:
    if r["stage1"]!="converged": continue
    R=r["refcode"]; A=rx(f"{X}/{R}.xyz"); B=rx(f"{D}/stage1_r2scan/{R}/{R}.xyz"); m=json.load(open(f"{D}/stage2_b3lyp/{R}/{R}.meta")); z=m["zn_index"]
    dd=[]
    for i in m["donors"]:
        x=d(B[z],B[i])-d(A[z],A[i]); by[A[i][0]].append(x); by["all"].append(x); dd.append(abs(x))
    per.append(max(dd))
def q(v,p): v=sorted(v); return v[int(p*(len(v)-1))]
print("elem n median_signed median_abs p90_abs max_abs")
for k,v in sorted(by.items(),key=lambda t:-len(t[1])):
    a=[abs(x) for x in v]; print(k,len(v),f"{S.median(v):+.3f}",f"{S.median(a):.3f}",f"{q(a,.9):.3f}",f"{max(a):.3f}")
print("per-structure max|d|: median",f"{S.median(per):.3f}","p90",f"{q(per,.9):.3f}","n>0.1",sum(p>0.1 for p in per))
for R in ["WONYUW","ADOLOU","GECLUZ","MOYBAD","LIVNAG","IQETOP"]:
    A=rx(f"{X}/{R}.xyz"); B=rx(f"{D}/stage1_r2scan/{R}/{R}.xyz"); m=json.load(open(f"{D}/stage2_b3lyp/{R}/{R}.meta")); z=m["zn_index"]
    print(R,[(A[i][0],round(d(A[z],A[i]),2),round(d(B[z],B[i]),2)) for i in m["donors"]])
