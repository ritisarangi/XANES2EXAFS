#!/usr/bin/env python3
"""Copy the minimum set of files Josh and Sam need into a flat, CSD-named share folder.

Usage (inside the project folder):
    python3 <repo>/export/export_share.py . /sdf/data/ssrl/smb/dft/users/tetef01/Riti-CSD-calcs

Copies, for every complex in redox/slopes_final.csv:
    ref/<REFCODE>_ref.xyz, .hess, .inp          stage-2 minimum (all 347)
    partner/<REFCODE>_<run>.xyz, .hess     only the partner runs that supply a bond's slope
Writes index.csv (charge, multiplicity, method per file), bonds.csv (one row per Zn-L bond,
with the partner file it uses) and README.txt. Safe to rerun; files are overwritten.
Standard library only, Python 3.6+.
"""
import sys, os, csv, re, shutil, json

RUNS = {  # slope source -> (run tag, folders searched in order)
    "own_first": ("redox1", ["redox/primary", "redox/fallback"]),
    "own_reverse": ("redox2", ["redox/reverse"]),
    "own_eps1": ("eps1", ["dielectric/eps1"]),
    "own_eps2": ("eps2", ["dielectric/eps2"]),
    "own_eps4": ("eps4", ["dielectric/eps4"]),
}
README = """Zn K-edge DFT set: geometries and analytic Hessians for 347 mononuclear Zn complexes (CSD)
Prepared by Riti Sarangi (SSRL). Generated {date}.
Code: github.com/ritisarangi/XANES2EXAFS (export/export_share.py, redox/combine_slopes.py)

METHOD
  ORCA 6.0.1, B3LYP-D3(BJ), def2-TZVP on Zn and first-shell donors, def2-SVP elsewhere, RIJCOSX,
  TightOpt + analytic Freq. CPCM(water, eps 80) unless noted. Closed-shell runs RKS, doublets UKS.

FOLDERS
  ref/       the reference minimum of every complex (347 xyz, hess, inp)
  partner/   second minima of the same complex, used only to get the slope d ln k / d r
             ({npart} complexes, {nfiles} xyz/hess/inp sets; only runs that supply a slope are included)

FILE NAMES   <REFCODE>_<run>.<ext>
  REFCODE    CSD refcode, upper case (e.g. HUFBAL)
  run  ref     reference minimum, eps 80, RKS singlet
       redox1  one electron toward neutral (q>0 -> q-1, q<0 -> q+1, q=0 -> +1), UKS doublet
       redox2  one electron the other way (q>0 -> q+1, q<0 -> q-1, q=0 -> -1), UKS doublet
       eps1    same charge, gas phase (no CPCM), RKS
       eps2    same charge, CPCM eps 2, RKS (anions with q <= -2)
  ext  .xyz    final optimized geometry, Angstrom, ORCA xyz format
       .hess   ORCA Hessian file: $hessian (Eh/bohr^2, mass-unweighted), $vibrational_frequencies,
               $normal_modes, $atoms (element, mass, coordinates in bohr)
       .inp    ORCA input as first submitted (keywords, charge, multiplicity, per-atom basis);
               runs restarted after preemption used the same input from the last saved geometry
  Atom order is identical in all files of one REFCODE.

FULL OUTPUTS (.out: energies, Mulliken spins, <S^2>) stay in
  /sdf/data/ssrl/smb/xas/users/ritis/Zn_small_molecule_dft/{stage2_b3lyp,redox/primary,redox/reverse,dielectric/eps1,dielectric/eps2}/<REFCODE>/

TABLES
  index.csv  one row per xyz/hess pair: refcode, run, file, charge, multiplicity, method, solvent
  bonds.csv  one row per Zn-L bond (all 347 complexes):
    refcode, bond        bond label Zn-<el><i>; i is the 0-based atom index of the donor in the xyz
    zn_index             0-based atom index of Zn
    element, donor_type  N or S, and donor class (pyridine, pyrazole, aryl/vinyl thiolate, ...)
    r0_A, k0_mdyn_A      Zn-L distance and relaxed (compliance) force constant at ref
    s2_10K_A2, nu0_cm    sigma^2 at 10 K and effective frequency of the bond from ref.hess (my check values)
    slope_per_A          d ln k / d r for the bond
    slope_source         own = from this bond's ref + partner pair; donor_type or element = fit over
                         all own slopes of that class (bond has no clean partner point)
    partner_file         stem of the partner pair the slope came from (blank when borrowed)

  Relaxed force constant: 1/k = sum_modes q_k^2 / (4 pi^2 c^2 nu_k^2), q_k = Zn-L stretch
  projection of normal mode k. Slope = [ln k(partner) - ln k(ref)] / [r(partner) - r(ref)].
  A partner point counts only if the donor stays closed-shell (|Mulliken spin| < 0.05),
  0.01 <= |dr| <= 0.15 A and k falls as r grows. Excluded (rearranged) complexes: {rearr}.
"""


def charge_mult(inp):
    if os.path.exists(inp):
        for line in open(inp):
            m = re.match(r"\s*\*\s*xyz\w*\s+(-?\d+)\s+(\d+)", line, re.I)
            if m:
                txt = open(inp).read()
                return int(m.group(1)), int(m.group(2)), ("CPCM" in txt.upper())
    return "", "", ""


def find(dft, folders, ref):
    for f in folders:
        d = os.path.join(dft, f, ref)
        if os.path.exists(os.path.join(d, ref + ".hess")) and os.path.exists(os.path.join(d, ref + ".xyz")):
            return d
    return None


def main():
    dft, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    rows = list(csv.DictReader(open(os.path.join(dft, "redox", "slopes_final.csv"))))
    for sub in ("ref", "partner"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    index, missing, bonds, pairs = [], [], [], set()

    def copy(d, ref, tag, sub):
        for ext in (".xyz", ".hess"):
            shutil.copy2(os.path.join(d, ref + ext), os.path.join(out, sub, "%s_%s%s" % (ref, tag, ext)))
        inp = next((os.path.join(d, n) for n in (ref + "_orig.inp", ref + ".inp") if os.path.exists(os.path.join(d, n))), None)
        if inp:
            shutil.copy2(inp, os.path.join(out, sub, "%s_%s.inp" % (ref, tag)))
        q, m, cpcm = charge_mult(os.path.join(d, ref + ".inp"))
        eps = {"eps1": "gas", "eps2": "CPCM eps 2", "eps4": "CPCM eps 4"}.get(tag, "CPCM eps 80")
        index.append(dict(refcode=ref, run=tag, file="%s/%s_%s" % (sub, ref, tag), charge=q, multiplicity=m,
                          method="UKS" if m not in ("", 1) else "RKS", solvent=eps))

    refs = sorted({r["ref"] for r in rows})
    for ref in refs:
        d = find(dft, ["stage2_b3lyp"], ref)
        if d:
            copy(d, ref, "ref", "ref")
        else:
            missing.append(ref + "_ref")
    zn = {}
    for ref in refs:
        try:
            zn[ref] = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))["zn_index"]
        except Exception:
            zn[ref] = ""
    for r in rows:
        tag = ""
        if r["source"] in RUNS:
            tag, folders = RUNS[r["source"]]
            if (r["ref"], tag) not in pairs:
                d = find(dft, folders, r["ref"])
                if d:
                    copy(d, r["ref"], tag, "partner")
                    pairs.add((r["ref"], tag))
                else:
                    missing.append("%s_%s" % (r["ref"], tag))
                    tag = ""
        bonds.append(dict(refcode=r["ref"], bond=r["bond"], zn_index=zn[r["ref"]], element=r["el"],
                          donor_type=r["donor_type"], r0_A=r["r0"], k0_mdyn_A=r["k0"], s2_10K_A2=r["s2_10K_0"],
                          nu0_cm=r["nu0"], slope_per_A=r["slope"],
                          slope_source="own" if r["source"].startswith("own") else r["source"],
                          partner_file="partner/%s_%s" % (r["ref"], tag) if tag else ""))
    for name, data in (("index.csv", index), ("bonds.csv", bonds)):
        with open(os.path.join(out, name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
    import datetime
    rearr = sorted({r["ref"] for r in rows if r.get("rearranged_complex") == "1"})
    with open(os.path.join(out, "README.txt"), "w") as f:
        f.write(README.format(date=datetime.date.today(), npart=len({p[0] for p in pairs}), nfiles=len(pairs),
                              rearr=", ".join(rearr) or "none"))
    print("ref pairs: %d   partner pairs: %d in %d complexes   bonds: %d"
          % (sum(1 for i in index if i["run"] == "ref"), len(pairs), len({p[0] for p in pairs}), len(bonds)))
    print("missing:", " ".join(missing) or "none")
    print("wrote", out)


if __name__ == "__main__":
    main()
