"""Usage: python3 imag_modes.py <path to dft dir> REF [REF ...]

For each stage-2 run, prints every imaginary mode, the six atoms that move most,
the Zn amplitude, whether the mode is a methyl rotation, and <S**2> for UKS runs.
Standard library only and Python 3.6 compatible, so it runs with the system python3 on S3DF.
"""
import sys, re, math

D = sys.argv[1]


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def mode_vectors(t, n):
    blk = t.split("NORMAL MODES")[-1].split("IR SPECTRUM")[0].split("\n")
    M = {}
    cols = None
    for l in blk:
        s = l.split()
        if s and all(x.isdigit() for x in s):
            cols = [int(x) for x in s]
            continue
        if cols and len(s) == len(cols) + 1 and s[0].isdigit():
            i = int(s[0])
            for c, v in zip(cols, s[1:]):
                M.setdefault(c, [0.0] * (3 * n))[i] = float(v)
    return M


for r in sys.argv[2:]:
    base = f"{D}/stage2_b3lyp/{r}/{r}"
    try:
        t = open(base + ".out", errors="ignore").read()
        L = open(base + ".xyz").read().split("\n")
    except OSError as e:
        print(r, "missing file:", e)
        continue
    n = int(L[0])
    A = [(l.split()[0], *map(float, l.split()[1:4])) for l in L[2:2 + n]]
    el = [a[0] for a in A]
    zn = el.index("Zn")
    fb = t.split("VIBRATIONAL FREQUENCIES")[-1].split("NORMAL MODES")[0]
    fr = [(int(a), float(b)) for a, b in re.findall(r"^\s*(\d+):\s+(-?\d+\.\d+) cm\*\*-1", fb, re.M)]
    M = mode_vectors(t, n)
    s2 = re.findall(r"Expectation value of <S\*\*2>\s*:\s*(-?\d+\.\d+)", t)
    head = f"{r}: {n} atoms" + (f", <S**2> = {s2[-1]}" if s2 else "")
    print(head)
    for k, f in fr:
        if f >= 0:
            continue
        v = M.get(k, [0.0] * (3 * n))
        amp = [math.sqrt(v[3 * i] ** 2 + v[3 * i + 1] ** 2 + v[3 * i + 2] ** 2) for i in range(n)]
        top = sorted(range(n), key=lambda i: -amp[i])[:6]
        # methyl rotation: the moving H atoms share one carbon that carries three H
        Hs = [i for i in top if el[i] == "H" and amp[i] > 0.2]
        cs = set()
        for h in Hs:
            c = min((j for j in range(n) if el[j] == "C"), key=lambda j: dist(A[h][1:], A[j][1:]))
            nH = sum(1 for j in range(n) if el[j] == "H" and dist(A[c][1:], A[j][1:]) < 1.2)
            cs.add((c, nH))
        methyl = len(Hs) >= 2 and len(cs) == 1 and list(cs)[0][1] == 3
        print(f"   {f:9.1f} cm-1  top: " + " ".join(f"{el[i]}{i}:{amp[i]:.2f}" for i in top)
              + f"  Zn amp {amp[zn]:.3f}  {'methyl rotation' if methyl else 'not a methyl rotation'}")
