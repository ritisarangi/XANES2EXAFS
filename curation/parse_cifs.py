"""Parse CSD ConQuest CIFs, build molecules under PBC, classify Zn complexes.

Output: zn_inventory.csv (one row per CIF file) and molecules/<REFCODE>.xyz for
mononuclear, finite, Zn-only-metal complexes.
"""
import sys, os, re, glob, math, json, hashlib, csv
from collections import defaultdict, Counter
import numpy as np

DROP_MINOR = os.environ.get("DROP_MINOR") == "1"
SRC = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(os.path.join(OUT, "molecules"), exist_ok=True)

# Default CSD bond radii (Angstrom); file-provided _atom_type_radius_bond wins.
RAD = dict(H=0.23, B=0.83, C=0.68, N=0.68, O=0.68, F=0.64, Si=1.20, P=1.05, S=1.02,
           Cl=0.99, Br=1.21, I=1.40, Se=1.22, Te=1.47, As=1.21, Zn=1.45, Cu=1.52,
           Ni=1.50, Co=1.33, Fe=1.52, Mn=1.61, Cd=1.69, Hg=1.70, Na=1.66, K=2.03,
           Li=1.28, Mg=1.41, Ca=1.76, Cs=2.44, Rb=2.20, Sn=1.39, Ge=1.17, Al=1.21,
           Ag=1.45, Au=1.36, Pt=1.36, Pd=1.39, Cr=1.39, V=1.53, Ti=1.60, Mo=1.54,
           W=1.62, Ru=1.42, Rh=1.42, Ir=1.32, Re=1.51, Sb=1.39, Bi=1.48, Ga=1.22,
           In=1.42, Tl=1.45, Pb=1.46, Ba=2.15, Sr=1.95, Ln=1.80, D=0.23)
TOL = 0.40
IONIC = {"Li", "Na", "K", "Rb", "Cs", "Mg", "Ca", "Sr", "Ba"}  # never bonded: counterions
TM = {"Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd",
      "Ag","Cd","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","La","Ce","Pr","Nd","Sm","Eu",
      "Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","U","Al","Ga","In","Tl","Sn","Pb","Bi","Sb"}


def num(s):
    s = s.strip()
    if s in (".", "?"):
        return None
    s = re.sub(r"\(.*?\)", "", s)
    try:
        return float(s)
    except ValueError:
        return None


def tokenize(text):
    toks = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(";"):
            buf = [ln[1:]]
            i += 1
            while i < len(lines) and not lines[i].startswith(";"):
                buf.append(lines[i]); i += 1
            toks.append(("\n".join(buf)).strip())
            i += 1
            continue
        s = ln.split("#")[0] if not ("'" in ln or '"' in ln) else ln
        for m in re.finditer(r"'([^']*)'(?=\s|$)|\"([^\"]*)\"(?=\s|$)|(\S+)", s):
            toks.append(m.group(1) if m.group(1) is not None else
                        m.group(2) if m.group(2) is not None else m.group(3))
        i += 1
    return toks


def parse_cif(path):
    toks = tokenize(open(path, errors="replace").read())
    items, loops = {}, []
    i = 0
    while i < len(toks):
        t = toks[i]
        if t.lower() == "loop_":
            names = []
            i += 1
            while i < len(toks) and toks[i].startswith("_"):
                names.append(toks[i].lower()); i += 1
            vals = []
            while i < len(toks) and not toks[i].startswith("_") and toks[i].lower() != "loop_" \
                    and not toks[i].lower().startswith("data_") and toks[i] != "#END":
                vals.append(toks[i]); i += 1
            n = len(names)
            rows = [vals[k:k + n] for k in range(0, len(vals) - n + 1, n)] if n else []
            loops.append((names, rows))
            continue
        if t.startswith("_") and i + 1 < len(toks):
            items[t.lower()] = toks[i + 1]; i += 2; continue
        i += 1
    return items, loops


def get_loop(loops, key):
    for names, rows in loops:
        if key in names:
            return names, rows
    return None, []


def parse_symop(op):
    op = op.replace(" ", "").lower()
    rot = np.zeros((3, 3)); tr = np.zeros(3)
    for r, comp in enumerate(op.split(",")):
        for m in re.finditer(r"([+-]?)(\d+/\d+|\d*\.?\d+)?\*?([xyz])?", comp):
            if not m.group(0):
                continue
            sign = -1.0 if m.group(1) == "-" else 1.0
            val, var = m.group(2), m.group(3)
            if var:
                coef = 1.0
                if val:
                    coef = eval(val) if "/" in val else float(val)
                rot[r, "xyz".index(var)] += sign * coef
            elif val:
                tr[r] += sign * (eval(val) if "/" in val else float(val))
    return rot, tr


def cell_matrix(a, b, c, al, be, ga):
    al, be, ga = map(math.radians, (al, be, ga))
    v = math.sqrt(1 - math.cos(al)**2 - math.cos(be)**2 - math.cos(ga)**2
                  + 2 * math.cos(al) * math.cos(be) * math.cos(ga))
    return np.array([[a, 0, 0],
                     [b * math.cos(ga), b * math.sin(ga), 0],
                     [c * math.cos(be), c * (math.cos(al) - math.cos(be) * math.cos(ga)) / math.sin(ga),
                      c * v / math.sin(ga)]])  # rows = lattice vectors


def elem_of(sym, label):
    s = (sym or label).strip()
    m = re.match(r"([A-Z][a-z]?)", s)
    e = m.group(1) if m else s[:1]
    if e == "D":
        e = "H"
    return e


def wl_hash(elems, adj, iters=4):
    lab = list(elems)
    for _ in range(iters):
        lab = [hashlib.md5((lab[i] + "|" + ",".join(sorted(lab[j] for j in adj[i]))).encode()).hexdigest()[:12]
               for i in range(len(lab))]
    return hashlib.md5(",".join(sorted(lab)).encode()).hexdigest()[:16]


def formula(elems):
    c = Counter(elems)
    order = (["C", "H"] if "C" in c else []) + sorted(k for k in c if k not in ("C", "H"))
    if "C" not in c and "H" in c:
        order = sorted(c)
    return " ".join(f"{k}{c[k]}" for k in order if k in c)


def analyse(path):
    fname = os.path.basename(path)
    refcode, klass = fname.split(".")[0], fname.split(".")[1]
    rec = dict(file=fname, refcode=refcode, family=re.sub(r"\d+$", "", refcode), klass=klass)
    items, loops = parse_cif(path)
    rec["name"] = (items.get("_chemical_name_systematic") or items.get("_chemical_name_common") or "").replace("\n", " ")
    rec["moiety"] = (items.get("_chemical_formula_moiety") or "").replace("\n", " ")
    rec["R"] = num(items.get("_refine_ls_r_factor_gt", "?") or "?")
    rec["T_K"] = num(items.get("_diffrn_ambient_temperature", "?") or "?")
    rec["year"] = items.get("_journal_year", "")
    try:
        cell = [num(items[k]) for k in ("_cell_length_a", "_cell_length_b", "_cell_length_c",
                                         "_cell_angle_alpha", "_cell_angle_beta", "_cell_angle_gamma")]
    except KeyError:
        cell = [None]
    names, rows = get_loop(loops, "_atom_site_fract_x")
    if None in cell or not rows:
        rec["status"] = "no_coordinates"
        return rec, None
    ix = {n: k for k, n in enumerate(names)}
    radii = dict(RAD)
    tn, trows = get_loop(loops, "_atom_type_radius_bond")
    if trows:
        ti = {n: k for k, n in enumerate(tn)}
        for r in trows:
            v = num(r[ti["_atom_type_radius_bond"]])
            if v:
                radii[elem_of(r[ti["_atom_type_symbol"]], "")] = v
    ops = []
    on, orows = get_loop(loops, "_symmetry_equiv_pos_as_xyz")
    if not orows:
        on, orows = get_loop(loops, "_space_group_symop_operation_xyz")
    if orows:
        k = on.index([n for n in on if n.endswith("xyz")][0])
        ops = [parse_symop(r[k]) for r in orows]
    else:
        ops = [(np.eye(3), np.zeros(3))]
    asym = []
    for r in rows:
        x, y, z = (num(r[ix["_atom_site_fract_x"]]), num(r[ix["_atom_site_fract_y"]]), num(r[ix["_atom_site_fract_z"]]))
        if None in (x, y, z):
            continue
        lab = r[ix["_atom_site_label"]]
        sym = r[ix["_atom_site_type_symbol"]] if "_atom_site_type_symbol" in ix else ""
        occ = num(r[ix["_atom_site_occupancy"]]) if "_atom_site_occupancy" in ix else 1.0
        if DROP_MINOR and lab.endswith("?"):
            continue
        asym.append((lab, elem_of(sym, lab), np.array([x, y, z]), occ if occ is not None else 1.0))
    rec["has_occupancy"] = int("_atom_site_occupancy" in ix)
    rec["partial_occ"] = int(any(a[3] < 0.99 for a in asym))
    rec["disorder_labels"] = int(any(re.search(r"[?']$|[A-Z]\d+[B-Z]$", a[0]) for a in asym))
    M = cell_matrix(*cell)
    # expand to full unit cell
    fr, el = [], []
    Rs = np.array([o[0] for o in ops]); Ts = np.array([o[1] for o in ops])
    for lab, e, f, occ in asym:
        imgs = (np.einsum("kij,j->ki", Rs, f) + Ts) % 1.0
        keep = []
        for g in imgs:
            ok = True
            for h in keep:
                d = g - h; d -= np.round(d)
                if np.linalg.norm(d @ M) < 0.25:
                    ok = False; break
            if ok:
                keep.append(g)
        fr.extend(keep); el.extend([e] * len(keep))
    fr = np.array(fr)
    # cross-site duplicates (atoms on special positions listed twice) - vectorized check
    if len(fr) > 1:
        from scipy.spatial import cKDTree
        sh = np.array([(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)])
        c0 = fr @ M; m0 = len(fr)
        sp = (c0[None] + (sh @ M)[:, None]).reshape(-1, 3)
        drop = set()
        for i, lst in enumerate(cKDTree(sp).query_ball_point(c0, 0.25)):
            for q in lst:
                j = q % m0
                if i < j and el[i] == el[j] and i not in drop:
                    drop.add(j)
        if drop:
            keepi = [k for k in range(len(fr)) if k not in drop]
            fr = fr[keepi]; el = [el[k] for k in keepi]
    n = len(fr)
    rec["n_cell_atoms"] = n
    if n > 12000:
        rec["status"] = "too_big"
        return rec, None
    cart = fr @ M
    rmax = max(radii.get(e, 1.5) for e in set(el))
    shifts = np.array([(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)])
    adj = defaultdict(list)  # i -> list of (j, shift)
    from scipy.spatial import cKDTree
    sup = (cart[None, :, :] + (shifts @ M)[:, None, :]).reshape(-1, 3)
    tree = cKDTree(sup)
    rr = np.array([radii.get(x, 1.5) for x in el])
    hits = tree.query_ball_point(cart, 2 * rmax + TOL)
    for i, lst in enumerate(hits):
        ei = el[i]
        if ei in IONIC:
            continue
        for q in lst:
            si, j = divmod(q, n)
            s = shifts[si]
            if i == j and not s.any():
                continue
            if el[j] in IONIC:
                continue
            d = np.linalg.norm(sup[q] - cart[i])
            if 0.5 < d < rr[i] + rr[j] + TOL:
                adj[i].append((j, tuple(s)))
    # periodic BFS: detect infinite components
    comp = [-1] * n; off = [None] * n; infinite = []
    for st in range(n):
        if comp[st] >= 0:
            continue
        cid = len(infinite); infinite.append(False)
        comp[st] = cid; off[st] = np.zeros(3, int); q = [st]
        while q:
            i = q.pop()
            for j, s in adj[i]:
                o = off[i] + np.array(s)
                if comp[j] < 0:
                    comp[j] = cid; off[j] = o; q.append(j)
                elif not np.array_equal(off[j], o):
                    infinite[cid] = True
    comps = defaultdict(list)
    for i in range(n):
        comps[comp[i]].append(i)
    zn_comps = [c for c, mem in comps.items() if any(el[i] == "Zn" for i in mem)]
    rec["n_zn_cell"] = sum(el[i] == "Zn" for i in range(n))
    rec["n_species_cell"] = len(comps)
    kinds = []
    for c in zn_comps:
        mem = comps[c]
        nzn = sum(el[i] == "Zn" for i in mem)
        other_m = sorted({el[i] for i in mem if el[i] in TM})
        if infinite[c]:
            kinds.append("polymeric")
        elif nzn > 1:
            kinds.append("multinuclear")
        elif other_m:
            kinds.append("heterometallic:" + "".join(other_m))
        else:
            kinds.append("mononuclear")
    kc = Counter(kinds)
    rec["zn_species"] = ";".join(f"{k}x{v}" for k, v in kc.items())
    if "polymeric" in kc:
        rec["status"] = "polymeric"
    elif any(k == "multinuclear" for k in kc):
        rec["status"] = "multinuclear"
    elif any(k.startswith("heterometallic") for k in kc):
        rec["status"] = "heterometallic"
    else:
        rec["status"] = "mononuclear"
    if rec["status"] != "mononuclear":
        return rec, None
    # pick representative Zn molecule; record distinct ones by hash
    mols = {}
    for c in zn_comps:
        mem = comps[c]
        pos = {i: cart[i] + off[i] @ M for i in mem}
        idx = {i: k for k, i in enumerate(mem)}
        e = [el[i] for i in mem]
        a = [[idx[j] for j, s in adj[i] if j in idx] for i in mem]
        h = wl_hash(e, a)
        if h not in mols:
            mols[h] = (mem, pos, e, a)
    rec["n_distinct_zn_mol"] = len(mols)
    want = {"S4": {"S": 4}, "S3N": {"S": 3, "N": 1}, "S2N2": {"S": 2, "N": 2},
            "SN3": {"S": 1, "N": 3}, "His4": {"N": 4}, "NC24": {"N": 4}}.get(klass, {})

    def pick_key(item):
        hh, (mm, pp, ee, aa) = item
        zi_ = ee.index("Zn")
        dc = Counter(ee[j] for j in aa[zi_])
        match = all(dc.get(k, 0) >= v for k, v in want.items())
        return (not match, -sum(x == "C" for x in ee), hh)
    h, (mem, pos, e, a) = sorted(mols.items(), key=pick_key)[0]
    rec["other_zn_species"] = "; ".join(formula(v[2]) for k, v in mols.items() if k != h)
    X = np.array([pos[i] for i in mem])
    zi = e.index("Zn")
    X -= X[zi]
    rec["mol_hash"] = h
    hv = [k for k in range(len(e)) if e[k] != "H"]
    hvi = {k: q for q, k in enumerate(hv)}
    rec["heavy_hash"] = wl_hash([e[k] for k in hv], [[hvi[j] for j in a[k] if j in hvi] for k in hv])
    rec["mol_formula"] = formula(e)
    rec["n_atoms"] = len(e)
    rec["n_H"] = e.count("H")
    rec["n_C"] = e.count("C")
    shell = sorted((float(np.linalg.norm(X[j])), e[j]) for j in a[zi])
    rec["CN"] = len(shell)
    rec["donors"] = "".join(f"{k}{v}" for k, v in sorted(Counter(s[1] for s in shell).items()))
    rec["zn_L"] = " ".join(f"{s[1]}{s[0]:.3f}" for s in shell)
    # close non-H contacts inside molecule => unresolved disorder
    heavy = [k for k in range(len(e)) if e[k] != "H"]
    D = np.linalg.norm(X[heavy][:, None] - X[heavy][None], axis=2)
    np.fill_diagonal(D, 9)
    rec["min_heavy_dist"] = round(float(D.min()), 3) if len(heavy) > 1 else None
    rec["disorder_flag"] = int((D < 0.9).any() or rec["partial_occ"])
    # heuristic missing-H flag: C with < 4 neighbours lacking H and sp3-like geometry is hard;
    # use simple counts: carbon present and H/C < 0.3, or zero H.
    rec["missing_H_flag"] = int(rec["n_C"] > 0 and rec["n_H"] / max(rec["n_C"], 1) < 0.3)
    # what else is in the cell (counterions / solvent), by formula
    others = Counter()
    for c, memb in comps.items():
        if c in zn_comps:
            continue
        others[formula([el[i] for i in memb])] += 1
    rec["other_species"] = "; ".join(f"{k}" for k in sorted(others))[:300]
    with open(os.path.join(OUT, "molecules", f"{refcode}.xyz"), "w") as fh:
        fh.write(f"{len(e)}\n{refcode} {rec['mol_formula']} from {fname}\n")
        for k in range(len(e)):
            fh.write(f"{e[k]:2s} {X[k,0]:12.6f} {X[k,1]:12.6f} {X[k,2]:12.6f}\n")
    return rec, h


def work(p):
    md5 = hashlib.md5(open(p, "rb").read()).hexdigest()
    try:
        rec, h = analyse(p)
    except Exception as ex:
        rec = dict(file=os.path.basename(p), refcode=os.path.basename(p).split(".")[0],
                   klass=os.path.basename(p).split(".")[1], status=f"parse_error:{ex}")
    rec["file_md5"] = md5
    return rec

if __name__ == "__main__":
  from multiprocessing import Pool
  paths = sorted(glob.glob(os.path.join(SRC, "*.cif")))
  with Pool(int(os.environ.get("NP", "8"))) as pool:
    recs = pool.map(work, paths, chunksize=4)
  seen_md5 = {}
  for rec in recs:
    rec["identical_file_of"] = seen_md5.get(rec["file_md5"], "")
    seen_md5.setdefault(rec["file_md5"], rec["file"])

  keys = []
  for r in recs:
      for k in r:
          if k not in keys:
              keys.append(k)
  with open(os.path.join(OUT, "zn_inventory_raw.csv"), "w", newline="") as fh:
      w = csv.DictWriter(fh, fieldnames=keys)
      w.writeheader()
      w.writerows(recs)
  json.dump(recs, open(os.path.join(OUT, "zn_inventory_raw.json"), "w"), indent=1, default=str)
  print(Counter(r["status"] for r in recs))
