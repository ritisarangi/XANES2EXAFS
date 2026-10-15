"""Usage: python3 dft/analysis/imag_modes.py <path to dft dir> REF [REF ...]
Prints each imaginary mode and the atoms that move most."""
import sys,re,numpy as np
D=sys.argv[1]
for r in sys.argv[2:]:
    t=open(f"{D}/stage2_b3lyp/{r}/{r}.out",errors="ignore").read()
    xyz=open(f"{D}/stage2_b3lyp/{r}/{r}.xyz").read().split("\n");n=int(xyz[0]);el=[l.split()[0] for l in xyz[2:2+n]]
    fb=t.split("VIBRATIONAL FREQUENCIES")[-1].split("NORMAL MODES")[0]
    fr=[(int(a),float(b)) for a,b in re.findall(r"^\s*(\d+):\s+(-?\d+\.\d+) cm\*\*-1",fb,re.M)]
    nm=t.split("NORMAL MODES")[-1].split("IR SPECTRUM")[0].split("\n")
    M=np.zeros((3*n,3*n)); cols=None
    for l in nm:
        s=l.split()
        if s and all(x.isdigit() for x in s): cols=[int(x) for x in s]; continue
        if cols and len(s)==len(cols)+1 and s[0].isdigit():
            i=int(s[0]); M[i,cols]=[float(x) for x in s[1:]]
    for k,f in fr:
        if f<0:
            v=M[:,k].reshape(n,3); a=np.linalg.norm(v,axis=1); top=np.argsort(-a)[:6]
            print(r,f"{f:.1f}","top atoms:",[f"{el[i]}{i}:{a[i]:.2f}" for i in top],"Zn amp",round(a[el.index('Zn')],3))
    print(r,"lowest 4:",[f for k,f in fr if abs(f)>0.01][:4])
    print(r,"run time",re.findall(r"TOTAL RUN TIME.*",t)[-1])
