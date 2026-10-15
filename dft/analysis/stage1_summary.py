"""Usage: python3 dft/analysis/stage1_summary.py <path to dft dir>"""
import os,re,json,csv,sys,math
D=os.path.abspath(sys.argv[1]); X=next(p for p in [os.path.join(os.path.dirname(D),"structures","dft_ready_xyz"),os.path.join(os.path.dirname(D),"dft_ready_xyz")] if os.path.isdir(p))
refs=[l.strip() for l in open(f"{D}/lists/all.txt") if l.strip()]
def rx(p):
    L=open(p).read().split("\n"); n=int(L[0]); return [(l.split()[0],*map(float,l.split()[1:4])) for l in L[2:2+n]]
def d(a,b): return math.dist(a[1:],b[1:])
rows=[]
for r in refs:
    o=f"{D}/stage1_r2scan/{r}/{r}.out"; t=open(o,errors="ignore").read() if os.path.exists(o) else ""
    ok="ORCA TERMINATED NORMALLY" in t and "OPTIMIZATION RUN DONE" in t
    cyc=t.count("GEOMETRY OPTIMIZATION CYCLE"); E=re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)",t)
    rt=re.findall(r"TOTAL RUN TIME: (\d+) days (\d+) hours (\d+) minutes",t)
    hrs=round(int(rt[-1][0])*24+int(rt[-1][1])+int(rt[-1][2])/60,2) if rt else ""
    st="converged" if ok else ("running" if "ORCA TERMINATED NORMALLY" not in t and "ERROR" not in t and "aborting" not in t.lower() else "failed")
    m=json.load(open(f"{D}/stage2_b3lyp/{r}/{r}.meta"))
    row=dict(refcode=r,stage1=st,cycles=cyc,E_Eh=E[-1] if E else "",hours=hrs,natoms=m["natoms"],charge=m["charge"])
    xo=f"{D}/stage1_r2scan/{r}/{r}.xyz"
    if ok and os.path.exists(xo):
        A=rx(f"{X}/{r}.xyz"); B=rx(xo); z=m["zn_index"]
        dr=[d(B[z],B[i])-d(A[z],A[i]) for i in m["donors"]]
        row["max_dZnL"]=round(max(dr,key=abs),3); row["max_ZnL_opt"]=round(max(d(B[z],B[i]) for i in m["donors"]),3)
        # new close contacts to Zn (non-donor heavy atom within 2.6)
        row["new_ZnX"]=";".join(f"{B[i][0]}{i}:{d(B[z],B[i]):.2f}" for i in range(len(B)) if i!=z and i not in m["donors"] and B[i][0]!="H" and d(B[z],B[i])<2.6)
        row["CN_opt"]=sum(1 for i in m["donors"] if d(B[z],B[i])<2.8)
        row["CN_xtal"]=len(m["donors"])
    if st=="failed":
        row["why"]=" | ".join(l.strip() for l in t.split("\n") if re.search(r"ERROR|error|abort|SCF NOT CONVERGED|not converge",l))[:300] or t.strip().split("\n")[-1][:200]
    rows.append(row)
keys=["refcode","stage1","cycles","E_Eh","hours","natoms","charge","CN_xtal","CN_opt","max_dZnL","max_ZnL_opt","new_ZnX","why"]
with open(f"{D}/stage1_summary.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); [w.writerow({k:x.get(k,"") for k in keys}) for x in rows]
import collections
print(collections.Counter(x["stage1"] for x in rows))
for x in rows:
    if x["stage1"]!="converged": print(x["refcode"],x["stage1"],x["cycles"],x.get("why",""))
cv=[x for x in rows if x["stage1"]=="converged"]
h=sorted(x["hours"] for x in cv if x["hours"]!="") or [0]; print("hours median",h[len(h)//2],"max",h[-1],"total",round(sum(h)))
print("CN changed:",[(x["refcode"],x["CN_xtal"],x["CN_opt"]) for x in cv if x.get("CN_opt")!=x.get("CN_xtal")])
big=sorted(cv,key=lambda x:-abs(x.get("max_dZnL",0)))[:15]; print("largest Zn-L change:",[(x["refcode"],x["max_dZnL"]) for x in big])
print("new Zn contacts:",[(x["refcode"],x["new_ZnX"]) for x in cv if x.get("new_ZnX")])
