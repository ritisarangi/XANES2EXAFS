"""Curate mononuclear Zn set: moiety charge/H check, dedup, representative choice."""
import json, re, csv, collections, sys

R = json.load(open(sys.argv[1]))
out_csv = sys.argv[2]


def parse_moiety(m):
    """Return list of (mult, {el: n}, charge) for each moiety component."""
    res = []
    for part in re.split(r",(?![^()]*\))", m):
        part = part.strip()
        if not part:
            continue
        mult = 1.0
        mm = re.match(r"^([\d.]+)\((.*)\)n?$", part)
        if mm:
            mult = float(mm.group(1)); part = mm.group(2)
        part = re.sub(r"^\((.*)\)n$", r"\1", part)
        ch = 0
        cm = re.search(r"(\d*)([+-])$", part)
        if cm:
            ch = int(cm.group(1) or 1) * (1 if cm.group(2) == "+" else -1)
            part = part[:cm.start()].strip()
        comp = {}
        for e, n in re.findall(r"([A-Z][a-z]?)([\d.]+)", part):
            comp[e] = comp.get(e, 0) + float(n)
        res.append((mult, comp, ch))
    return res


def counts(formula):
    return {e: int(n) for e, n in re.findall(r"([A-Z][a-z]?)(\d+)", formula)}


mono = [r for r in R if r.get("status") == "mononuclear" and not r.get("identical_file_of")]
for r in mono:
    mc = counts(r["mol_formula"])
    r["charge_csd"] = ""
    r["H_expected"] = ""
    r["moiety_match"] = "none"
    for mult, comp, ch in parse_moiety(r.get("moiety", "")):
        if comp.get("Zn") == 1:
            heavy_ok = all(abs(comp.get(e, 0) - n) < 0.01 for e, n in mc.items() if e != "H") and \
                all(abs(mc.get(e, 0) - n) < 0.01 for e, n in comp.items() if e != "H")
            if heavy_ok:
                r["charge_csd"] = ch
                r["H_expected"] = int(comp.get("H", 0))
                r["moiety_match"] = "exact" if abs(comp.get("H", 0) - mc.get("H", 0)) < 0.01 else "H_mismatch"
                break
            elif r["moiety_match"] == "none":
                r["moiety_match"] = "heavy_mismatch"
                r["charge_csd"] = ch
                r["H_expected"] = int(comp.get("H", 0))
    r["missing_H"] = int(r["moiety_match"] == "H_mismatch" and (r["H_expected"] or 0) > r["n_H"])
    r["extra_H"] = int(r["moiety_match"] == "H_mismatch" and (r["H_expected"] or 0) < r["n_H"])
    # quality score for representative choice (lower is better)
    r["_score"] = (r["moiety_match"] != "exact", r["disorder_flag"], r["R"] if r["R"] is not None else 1.0,
                   r["T_K"] if r["T_K"] is not None else 400)

groups = collections.defaultdict(list)
for r in mono:
    groups[r["heavy_hash"]].append(r)
reps = []
for h, g in groups.items():
    g.sort(key=lambda x: x["_score"])
    rep = g[0]
    rep["group_size"] = len(g)
    rep["group_members"] = " ".join(x["refcode"] for x in g)
    for x in g[1:]:
        x["duplicate_of"] = rep["refcode"]
    reps.append(rep)

# suitability flags for the DFT set
for r in reps:
    issues = []
    if r["moiety_match"] != "exact":
        issues.append(f"moiety:{r['moiety_match']}")
    if r["disorder_flag"]:
        issues.append("disorder")
    if r["CN"] < 4 or r["CN"] > 6:
        issues.append(f"CN={r['CN']}")
    if "H" in r["donors"]:
        issues.append("Zn-H contact")
    if r["n_distinct_zn_mol"] > 1:
        issues.append(f"{r['n_distinct_zn_mol']} distinct Zn molecules in cell")
    r["issues"] = "; ".join(issues)
    r["clean"] = int(not issues)

reps.sort(key=lambda x: (x["donors"], x["refcode"]))
cols = ["refcode", "klass", "donors", "CN", "mol_formula", "n_atoms", "charge_csd", "n_H", "H_expected",
        "moiety_match", "disorder_flag", "issues", "clean", "zn_L", "R", "T_K", "year", "group_size",
        "group_members", "other_species", "name", "moiety"]
with open(out_csv, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
    w.writeheader(); w.writerows(reps)
json.dump(reps, open(out_csv.replace(".csv", ".json"), "w"), indent=1, default=str)

print("mononuclear files", len(mono), "unique complexes", len(reps), "clean", sum(r["clean"] for r in reps))
print("by file class", collections.Counter(r["klass"] for r in reps))
print("by donor set", collections.Counter(r["donors"] for r in reps).most_common())
print("moiety", collections.Counter(r["moiety_match"] for r in reps))
print("charge", collections.Counter(r["charge_csd"] for r in reps))
print("issues", collections.Counter(i.split(":")[0].split("=")[0] for r in reps for i in r["issues"].split("; ") if i))
na = sorted(r["n_atoms"] for r in reps if r["clean"])
print("atoms in clean set: min", na[0], "median", na[len(na)//2], "max", na[-1],
      ">100:", sum(x > 100 for x in na))
