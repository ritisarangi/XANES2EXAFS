#!/usr/bin/env python3
"""Pack what the scans need into one small file for another cluster (run on S3DF).

Usage (inside the project folder):
    python3 <repo>/scans/make_bundle.py . [lists/all.txt]
Writes scan_bundle.tar.gz with, per complex, the stage-2 geometry (.xyz), donor metadata (.meta)
and a one-line .out stub holding the final stage-2 energy (validate.py compares against it),
plus lists/scan_full.txt: every complex except the pilot set and the ones awaiting a new
minimum (OKARID, MECFAC, PUFWOD). Standard library only.
"""
import sys, os, re, tarfile, io

dft = os.path.abspath(sys.argv[1])
lst = sys.argv[2] if len(sys.argv) > 2 else "lists/all.txt"
refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip()]
pilot = {l.strip() for l in open(os.path.join(dft, "lists", "pilot.txt")) if l.strip()}
hold = {"OKARID", "MECFAC", "PUFWOD"}
keep, miss = [], []
out = os.path.join(dft, "scan_bundle.tar.gz")
with tarfile.open(out, "w:gz") as tar:
    def add_bytes(name, data):
        ti = tarfile.TarInfo(name)
        ti.size = len(data)
        tar.addfile(ti, io.BytesIO(data))
    for ref in refs:
        d = os.path.join(dft, "stage2_b3lyp", ref)
        xyz, meta, o = (os.path.join(d, ref + e) for e in (".xyz", ".meta", ".out"))
        if not all(os.path.exists(p) for p in (xyz, meta, o)):
            miss.append(ref)
            continue
        E = re.findall(r"FINAL SINGLE POINT ENERGY\s+-?\d+\.\d+", open(o, errors="ignore").read())
        if not E:
            miss.append(ref)
            continue
        tar.add(xyz, "stage2_b3lyp/%s/%s.xyz" % (ref, ref))
        tar.add(meta, "stage2_b3lyp/%s/%s.meta" % (ref, ref))
        add_bytes("stage2_b3lyp/%s/%s.out" % (ref, ref), (E[-1] + "\nstub: stage-2 final energy only\n").encode())
        if ref not in pilot and ref not in hold:
            keep.append(ref)
    add_bytes("lists/scan_full.txt", ("\n".join(keep) + "\n").encode())
    add_bytes("lists/pilot.txt", ("\n".join(sorted(pilot)) + "\n").encode())
print("complexes packed: %d, in lists/scan_full.txt: %d, missing: %s" % (len(refs) - len(miss), len(keep), " ".join(miss) or "none"))
print("wrote %s (%.1f MB)" % (os.path.relpath(out, dft), os.path.getsize(out) / 1e6))
