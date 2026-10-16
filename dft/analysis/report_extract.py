#!/usr/bin/env python3
"""Collect the numbers for the structure and frequency report into one small folder.

Usage (inside the project folder on S3DF):
    python3 <repo>/dft/analysis/report_extract.py . [lists/all.txt]
Writes report/report_data.log (JSON) and report/xyz/<REF>.xyz (stage-2 geometries),
so `s3df pull report` brings back a few MB. Standard library only, Python 3.6+.

Per complex: charge, multiplicity, atom count, donors; Zn-L distances in the crystal
(stage-1 input), r2SCAN-3c (stage 1) and B3LYP (stage 2); L-Zn-L angles and tau4;
stage-2 energy, lowest frequencies and imaginary modes; and for every Zn-L bond the
harmonic mean-square relative displacement from the stage-2 normal modes,

    sigma2(T) = sum_k  C / nu_k * coth(h c nu_k / 2 k_B T) * q_k^2,   C = h / (8 pi^2 c amu) = 16.8576 amu A^2 cm^-1
    q_k = (u_k,L / sqrt(m_L) - u_k,Zn / sqrt(m_Zn)) . R_hat

with nu_k the frequency of mode k (cm^-1), u_k its mass-weighted orthonormal eigenvector,
m the atomic masses (amu) and R_hat the unit vector Zn->L. Imaginary modes are skipped.
The bond's effective (Einstein) frequency follows from the T -> 0 limit:
    nu_eff = C / (mu * sigma2(0)),  mu = m_Zn m_L / (m_Zn + m_L).
"""
import sys, os, re, json, math

C = 16.8576            # amu A^2 cm^-1
HC_K = 1.438777        # h c / k_B in cm K
BOHR = 0.529177210903


def read_xyz(p):
    L = open(p).read().split("\n")
    n = int(L[0])
    return [(s.split()[0], float(s.split()[1]), float(s.split()[2]), float(s.split()[3])) for s in L[2:2 + n]]


def read_inp_geom(p):
    t = open(p).read().split("\n")
    i = next(k for k, l in enumerate(t) if l.strip().startswith("* xyz"))
    out = []
    for l in t[i + 1:]:
        if l.strip() == "*":
            break
        s = l.split()
        out.append((s[0], float(s[1]), float(s[2]), float(s[3])))
    return out


def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in (1, 2, 3)))


def angle(a, b, c):
    u = [a[i] - b[i] for i in (1, 2, 3)]
    v = [c[i] - b[i] for i in (1, 2, 3)]
    x = sum(p * q for p, q in zip(u, v)) / math.sqrt(sum(p * p for p in u) * sum(q * q for q in v))
    return math.degrees(math.acos(max(-1.0, min(1.0, x))))


def read_hess(p):
    t = open(p).read()
    sec = {}
    for m in re.finditer(r"^\$(\w+)\s*\n", t, re.M):
        sec[m.group(1)] = m.end()

    def block(name):
        s = sec[name]
        e = t.find("\n$", s)
        return t[s:e].split("\n")
    at = [l for l in block("atoms") if l.strip() and not l.lstrip().startswith("#")]
    n = int(at[0])
    masses = [float(l.split()[1]) for l in at[1:1 + n]]
    fr = block("vibrational_frequencies")
    nf = int(fr[0])
    freqs = [float(l.split()[1]) for l in fr[1:1 + nf]]
    nm = block("normal_modes")
    dim = int(nm[0].split()[0])
    modes = [[0.0] * dim for _ in range(dim)]   # modes[k][i]: component i of mode k
    cols = None
    for l in nm[1:]:
        s = l.split()
        if not s or s[0].startswith("#"):
            continue
        if all(x.isdigit() for x in s):
            cols = [int(x) for x in s]
            continue
        r = int(s[0])
        for c, v in zip(cols, s[1:]):
            modes[c][r] = float(v)
    return masses, freqs, modes


def sigma2(masses, freqs, modes, zn, L, R, temps):
    rhat = [R[L][i] - R[zn][i] for i in (1, 2, 3)]
    nr = math.sqrt(sum(x * x for x in rhat))
    rhat = [x / nr for x in rhat]
    out = {T: 0.0 for T in temps}
    s0 = 0.0
    for k, nu in enumerate(freqs):
        if nu <= 1.0:
            continue
        v = modes[k]
        # mass-weighted eigenvector: sqrt(m) * cartesian displacement, then normalise
        mw = [v[3 * a + j] * math.sqrt(masses[a]) for a in range(len(masses)) for j in range(3)]
        nrm = math.sqrt(sum(x * x for x in mw))
        if nrm == 0:
            continue
        q = sum(((mw[3 * L + j] / math.sqrt(masses[L])) - (mw[3 * zn + j] / math.sqrt(masses[zn]))) * rhat[j] for j in range(3)) / nrm
        base = C / nu * q * q
        s0 += base
        for T in temps:
            x = HC_K * nu / (2.0 * T)
            out[T] += base / math.tanh(x)
    return s0, out


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2] if len(sys.argv) > 2 else "lists/all.txt"
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip()]
    outdir = os.path.join(dft, "report")
    os.makedirs(os.path.join(outdir, "xyz"), exist_ok=True)
    data = []
    for ref in refs:
        rec = {"ref": ref}
        try:
            meta = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
            zn, donors = meta["zn_index"], meta["donors"]
            rec.update(charge=meta["charge"], mult=meta["mult"], natoms=meta["natoms"],
                       donor_elems=[meta["donor_elems"][i] for i in range(len(donors))])
            X = read_inp_geom(os.path.join(dft, "stage1_r2scan", ref, ref + ".inp"))
            s1x = os.path.join(dft, "stage1_r2scan", ref, ref + ".xyz")
            S1 = read_xyz(s1x) if os.path.exists(s1x) else None
            s2x = os.path.join(dft, "stage2_b3lyp", ref, ref + ".xyz")
            out2 = os.path.join(dft, "stage2_b3lyp", ref, ref + ".out")
            t2 = open(out2, errors="ignore").read() if os.path.exists(out2) else ""
            ok2 = "ORCA TERMINATED NORMALLY" in t2 and "VIBRATIONAL FREQUENCIES" in t2
            rec["stage2_ok"] = ok2
            if not ok2:
                data.append(rec)
                continue
            B = read_xyz(s2x)
            open(os.path.join(outdir, "xyz", ref + ".xyz"), "w").write(open(s2x).read())
            E = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", t2)
            rec["E_b3lyp"] = float(E[-1]) if E else None
            rec["r_xtal"] = [round(dist(X[zn], X[L]), 4) for L in donors]
            rec["r_r2scan"] = [round(dist(S1[zn], S1[L]), 4) for L in donors] if S1 else None
            rec["r_b3lyp"] = [round(dist(B[zn], B[L]), 4) for L in donors]
            angs = [round(angle(B[donors[a]], B[zn], B[donors[b]]), 2)
                    for a in range(len(donors)) for b in range(a + 1, len(donors))]
            rec["angles_b3lyp"] = angs
            if len(donors) == 4:
                top = sorted(angs)[-2:]
                rec["tau4"] = round((360.0 - sum(top)) / 141.0, 3)
            masses, freqs, modes = read_hess(os.path.join(dft, "stage2_b3lyp", ref, ref + ".hess"))
            vib = freqs[6:] if len(freqs) > 6 else freqs
            rec["n_imag"] = sum(1 for f in freqs if f < -1.0)
            rec["imag"] = [round(f, 1) for f in freqs if f < -1.0]
            rec["lowest_real"] = [round(f, 1) for f in sorted(f for f in freqs if f > 1.0)[:5]]
            s2_10, s2_300, nu_eff = [], [], []
            for L in donors:
                s0, st = sigma2(masses, freqs, modes, zn, L, B, (10.0, 300.0))
                mu = masses[zn] * masses[L] / (masses[zn] + masses[L])
                s2_10.append(round(st[10.0], 6))
                s2_300.append(round(st[300.0], 6))
                nu_eff.append(round(C / (mu * s0), 2) if s0 > 0 else None)
            rec["sigma2_10K"] = s2_10
            rec["sigma2_300K"] = s2_300
            rec["nu_eff"] = nu_eff
        except Exception as e:  # keep going; the report lists the failures
            rec["error"] = "%s: %s" % (type(e).__name__, e)
        data.append(rec)
    json.dump(data, open(os.path.join(outdir, "report_data.log"), "w"))
    ok = sum(1 for r in data if r.get("sigma2_10K"))
    bad = [r["ref"] for r in data if "error" in r]
    print("complexes: %d, with frequencies and sigma2: %d, errors: %d %s" % (len(data), ok, len(bad), " ".join(bad[:10])))
    sz = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(outdir) for f in fs)
    print("report folder: %.1f MB" % (sz / 1e6))


if __name__ == "__main__":
    main()
