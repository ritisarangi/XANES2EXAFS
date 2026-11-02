# Zn relaxed-scan campaign: report for Riti Sarangi (SSRL)

Generated 2026-11-02 12:03 UTC by `aurora/campaign_report.py` from the run folder `/lus/flare/projects/ModCon/dsokaras/zn_scans` and the results checkout `/home/dsokaras/dev/xanes2exafs/XANES2EXAFS-results` (branch `aurora-results`). Rebuild with `python3 aurora/campaign_report.py /lus/flare/projects/ModCon/dsokaras/zn_scans > aurora/CAMPAIGN_REPORT.md`. Hand-written sections come from `aurora/campaign_report_notes.md`. Numbers in tables are computed; statements marked *(inference)* are interpretation.

## Summary

Relaxed one-coordinate scans (B3LYP-D3(BJ), def2-TZVP on Zn and donors, def2-SVP elsewhere, RIJCOSX, CPCM(water), ORCA 6.0.1) around the stage-2 minima of **338 Zn complexes**: 10,175 scan branches, 102,426 planned points (constrained optimisations, two branch starts per coordinate included). 10,175 of 10,175 branches have terminated normally (100.0%). **330 complexes are published** on `aurora-results` (100,032 points validated, **89,807 pass**, **89.8%**); **8 finished complexes are not exported** (every branch start fails validation: the stage-2 minimum has a different Zn first shell than the donor list); **0 complexes are still running** (0 of their 0 branches done; Aurora `main` queue: 0 pending, 0 running). 39 published complexes fall below their stage-2 energy by more than 2 kJ/mol in some branch, and 46 pass fewer than 75% of their points; both lists are below.

|  | Complexes | Branches | Points | Passing |
|---|---|---|---|---|
| Published | 330 | 9,937 | 100,032 | 89,807 |
| Not exported | 8 | 238 | 2,394 | 0 |
| In progress | 0 | 0 (0 done) | 0 | - |
| Total | 338 | 10,175 | 102,426 | 89,807 |

**Reading guide.** The results are the `scan_results/` folder on branch `aurora-results`. Its layout and its
README are the deliverable; this report does not change them. Each published point is one constrained
optimisation that passed `scans/validate.py`. The *Complexes that need Riti's attention* section lists what
needs a chemist's decision. The *Decisions for Riti* section turns that into numbered choices, each with a
recommendation and a cost. Atom labels such as `N5` or `O62` are 0-based indices into the stage-2 xyz, so
`N5` is atom 5 counted from 0. This is the same convention as the coordinate names in `coords/<REF>.json`.
Facts come from files and code. *Inference* marks interpretation.

## How the scans were run

### Starting structures (Riti's pipeline, not redone)

The campaign started from `scan_bundle.tar.gz` (made by `scans/make_bundle.py`). For 338 complexes the bundle
holds three things:
- the stage-2 B3LYP minimum (`stage2_b3lyp/<REF>/<REF>.xyz`);
- the `.meta` file, with charge, multiplicity, Zn index and donor list;
- a stub `.out` file with only the final stage-2 energy.

Riti's pipeline produced these on S3DF:
- crystal (`structures/dft_ready_xyz/`);
- stage 1: r2SCAN-3c CPCM(water) Opt;
- stage 2: B3LYP-D3BJ, def2-TZVP on Zn and donors, def2-SVP elsewhere, CPCM(water), TightOpt Freq.

The donor list comes from the **crystal** (`curation/build_dft.py`). A neighbour is a donor if
d < r(Zn) + r(L) + 0.4 A (CSD radii) and d <= 2.8 A. The cut-off is therefore 2.53 A for N/O and 2.80 A for S.
The campaign never re-optimised stage 2. Full stage-1 and stage-2 outputs and the frequencies exist only on
S3DF.

### Coordinates (`scans/make_scans.py`)

Each coordinate is scanned with everything else relaxed. It runs as two branches, `neg` and `pos`, and both
start at the stage-2 minimum.

| Coordinate | Definition | Range, step | Points per branch |
|---|---|---|---|
| bond | Zn-L, every donor | -0.06 .. +0.20 A, 0.02 A | neg 4, pos 11 |
| angle | L-Zn-L, every donor pair | -15 .. +15 deg, 1.5 deg | 11 + 11 |
| twist | dihedral L1-L2-L3-L4 (CN 4 only) | -10 .. +10 deg, 1 deg | 11 + 11 |
| tilt | Zn-L-C-X, one per donor | -10 .. +10 deg, 1 deg | 11 + 11 |

A four-coordinate complex has 30 branches and 302 points; step 0 of every branch is the minimum. Angle
branches that would pass 178 deg are skipped, which is why some complexes have 29 branches. Dihedrals with an
angle above 165 deg are also skipped. Complexes with more donors have more branches.

### Level of theory (as written in every `scan.inp`)

```
! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) TightOpt DefGrid3 TightSCF
%scf MaxIter 500 end
%geom MaxIter 100  Scan <B|A|D> <atoms> = <start>, <end>, <n> end end
* xyz <charge> <mult>     (from the .meta; Zn and donor atoms carry newgto "def2-TZVP")
```

This is the stage-2 method, applied as a relaxed surface scan. Only `%pal nprocs` and `%maxcore` were changed
per site, at run time:

| Where | Cores per branch | maxcore (MB) | Notes |
|---|---|---|---|
| Aurora `main` pool (< 100 atoms) | 4 (24 per node) | 3000 | 10-17 to the end |
| Aurora `big` pool (>= 100 atoms) | 8 (12 per node) | 3000 | 10-18 to 10-25, then moved to NERSC |
| Aurora 256-node farms with `AUTO_CORES` | 12-16 | 3000 | from 10-29, when fewer branches than slots were left |
| Perlmutter shared QOS (m5268, m2464) | 8 | 3000, then 2000 from 10-25 09:15 | one Slurm job per branch, 48 h |
| Perlmutter regular QOS, 10 whole-node jobs | 8 (16 branches per node) | 3000 | 160 branches, 10-25 to 10-27 |

`maxcore` sets ORCA's batching, not the method. Different core counts give the same results within numerical
noise: the cross-site checks below compare Aurora at 4 cores with Perlmutter at 8 cores. *Inference* for the
12-16-core runs: they were not compared separately.

Both sites used ORCA 6.0.1 from the same archive, `orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz`. Its
SHA-256 was compared before NERSC was used (`nersc/iri/README.md`). OpenMPI 4.1.6 was built with the same
configure options at both sites.

### Stop and continue (restarts)

Every farm and every Perlmutter job stops ORCA before its walltime. `scans/restart.py` then does three things:
- It keeps the converged steps in `scan_acc.txt` and saves the original input once as `scan_orig.inp`.
- It writes a new `scan.inp` for the remaining targets.
- With `RESUME_PARTIAL=1`, the default on both sites, the interrupted step restarts from its **latest
  optimisation geometry at the same target** instead of from the last converged step.

When the continuation ends normally, `--stitch` rebuilds `scan.out` as the kept steps followed by the new
steps, numbered as one scan, and `validate.py` reads it as one run. Earlier raw outputs are kept as
`scan_try<N>.out`. A stitched `scan.out` therefore contains only the converged step blocks of earlier runs:
- ORCA headers and timings of earlier runs are only in `scan_try*.out`;
- the run time logged at the end covers the last run only.

Runs killed by MPI failures were continued from the last converged geometry. These were start-up races on
Aurora on 10-18 and an OpenMPI XPMEM segfault in Perlmutter shared jobs, fixed on 10-25 19:37 UTC by
`btl_vader_single_copy_mechanism=cma`. Both are transport problems; *inference*: they do not change results.
Riti was asked in `aurora/README.md` (How it differs from Perlmutter) to confirm that she accepts
`RESUME_PARTIAL`; that question is still open (Decision 9).

### Cross-site agreement (Run log)

- Aurora pilot, 10-17: the first SCF at each stage-2 geometry reproduced the S3DF stage-2 energy to 1e-6 Eh
  (0.001 kJ/mol), and 52 of 52 completed points passed.
- Perlmutter tests, 10-24: 103 scan steps of 24 CADKUO branches and 28 optimisation cycles of 4 OJEKOD branches
  reproduced Aurora to 0.003 and 0.009 kJ/mol and 0.007 A. These were the same inputs, ORCA build and restart
  code.

### Audit before publication (`aurora/audit.py`)

A complex is published only after the audit finds no problem for it. The audit checks three things:
- **identity**: every ORCA output in a branch folder (`scan.out`, `scan_cont.out`, `scan_try*.out`) echoes that
  folder's own scanned or constrained coordinate, charge and multiplicity;
- **overlap**: no branch folder was run by two ORCA processes at once (from the run logs);
- **queue**: no branch is pending twice, and none is in both pools.

Two incidents were reviewed:
- **UDODOG**, 10-23. Sixteen branches were each run twice at once for about 30 min because of a re-queue race,
  fixed since by a per-folder lock. Each run had its own input copy, scratch and output. Only one step from an
  overlapping run is in the results (angle_S1-Zn-N6 neg, 113.325 deg, E_rel 4.96 kJ/mol). It lies on the smooth
  curve and passes. The branches are listed in `autopilot/audit_reviewed.txt`, and UDODOG was published on 10-27.
- **isaac storage cut**, 10-23/24. After the isaac allocation ended, ALCF set its quota to 1 MB and writes
  failed silently. All 202 files written by farm 8957252 during that period were moved to
  `quarantine_8957252/` in their branch folders and are not used. `aurora/rebuild_acc.py` rebuilt 373 branches'
  `scan_acc.txt` by replaying their tries; it reproduced 4,160 intact branches byte for byte. The run folder was
  copied to ModCon storage.

Nothing ran twice in a way that reached the results. Every published `scan.out` matches its folder's input.

### What "published" means

A complex is published once, by `aurora/publish.py`, when:
- every branch has `ORCA TERMINATED NORMALLY`;
- the audit has passed;
- `validate.py` has run over all its points.

Its passing geometries go to `scan_results/<REF>.xyz` in the format of `scans/export_points.py`, with the
comment line `REF coordinate branch step= offset= value= E_rel_kJ= E_h=`. Every point, passing or not, goes to
`scan_results/validation_scan_full.csv`, and `coords.json` is copied to `scan_results/coords/<REF>.json`. A
complex whose branch starts all fail is recorded as `not_exported`, with no files. Raw outputs stay in the run
folder on Aurora.

### Where the work ran

Aurora CPU farms ran on ALCF project isaac until 10-21, then on ModCon. ModCon also holds the storage since
10-24. On 10-25 the unfinished `big` complexes moved to NERSC Perlmutter on project m5268. On 10-29, 10-30 and
10-31 some `main` complexes with long tails moved to m2464; the user capped that project and it is shared by a
group. On 11-01 the last 22 `main` branches (DIVKAW, UCOLON, FAZJAT, GIXSUE, LOHZAM, FEKQUH, QISJUA; 65-97
atoms, up to 24 attempts each) also moved to m2464, the user's decision: each needed one to five more points,
and on Aurora every 6 h farm run waited 4-6 h to start, with a maintenance on Nov 2-5. A complex listed in `remote_refs.txt` is never queued or prepared on Aurora, so no branch ran at both
sites at once. Finished branches are copied back to Aurora by Globus (`scan.out` and `scan_acc.txt`) and
published there like all others. The HPC side of the campaign is distilled in `HPC_LESSONS.md` and not
repeated here.

### Complexes run (fully or partly) on NERSC Perlmutter

From `remote_refs.txt`; branch counts from the NERSC driver state. Every complex listed started on Aurora; branches that had already finished there before the move are not counted, and the moved branches continued from their Aurora files.

| Complex | Atoms | Account | Branches with a Perlmutter job | Status |
|---|---|---|---|---|
| CAPWIB | 65 | m2464 | 30 / 30 | published 2026-10-31 |
| CAWKIW | 65 | m2464 | 26 / 30 | published 2026-10-31 |
| DIVKAW | 96 | m2464 | 6 / 30 | published 2026-11-02 |
| FAXYIP | 77 | m2464 | 25 / 30 | published 2026-11-01 |
| FAZJAT | 97 | m2464 | 3 / 30 | published 2026-11-02 |
| FEKQUH | 90 | m2464 | 2 / 30 | published 2026-11-02 |
| FUXMAM | 73 | m2464 | 26 / 30 | published 2026-10-31 |
| GIXSUE | 65 | m2464 | 3 / 30 | published 2026-11-02 |
| JOCZEG | 81 | m2464 | 30 / 30 | published 2026-10-31 |
| JUQXUO | 77 | m2464 | 27 / 30 | published 2026-11-01 |
| LAJGIM | 89 | m2464 | 30 / 30 | published 2026-11-01 |
| LOHZAM | 85 | m2464 | 3 / 30 | published 2026-11-02 |
| QISJUA | 91 | m2464 | 1 / 30 | published 2026-11-02 |
| SEJZOW | 85 | m2464 | 26 / 30 | published 2026-11-01 |
| TELRUZ | 77 | m2464 | 26 / 30 | published 2026-11-01 |
| TEYSOG | 73 | m2464 | 25 / 30 | published 2026-11-01 |
| TIFNUU | 65 | m2464 | 27 / 30 | published 2026-11-01 |
| UCOLON | 82 | m2464 | 4 / 30 | published 2026-11-02 |
| UWAVOF | 71 | m2464 | 26 / 30 | published 2026-11-01 |
| UYORAE | 93 | m2464 | 30 / 30 | published 2026-11-02 |
| WEQZAT01 | 48 | m2464 | 26 / 30 | published 2026-11-01 |
| BUNNII | 137 | m5268 | 30 / 30 | published 2026-10-31 |
| CATZUS10 | 137 | m5268 | 30 / 30 | published 2026-11-01 |
| DOZVOF | 111 | m5268 | 30 / 30 | published 2026-10-29 |
| GUCSED | 105 | m5268 | 30 / 30 | published 2026-10-28 |
| GUFHEU | 105 | m5268 | 30 / 30 | published 2026-10-30 |
| HOMQAC | 115 | m5268 | 30 / 30 | published 2026-10-27 |
| ICAVAK | 101 | m5268 | 30 / 30 | published 2026-10-27 |
| NAMSOJ | 104 | m5268 | 30 / 30 | published 2026-10-27 |
| NECTOG | 102 | m5268 | 30 / 30 | published 2026-10-27 |
| NONLEI | 117 | m5268 | 30 / 30 | published 2026-10-28 |
| OJEKUJ | 137 | m5268 | 14 / 30 | published 2026-10-26 |
| OJELOE | 109 | m5268 | 30 / 30 | published 2026-10-28 |
| RAYBIC | 124 | m5268 | 28 / 30 | published 2026-10-28 |
| REJBUD | 102 | m5268 | 30 / 30 | published 2026-10-27 |
| SONROE | 125 | m5268 | 29 / 30 | published 2026-10-28 |
| WIGBIX | 121 | m5268 | 30 / 30 | published 2026-10-29 |
| WORMAR | 113 | m5268 | 30 / 30 | published 2026-10-27 |
| WUJZOS | 127 | m5268 | 4 / 30 | published 2026-10-26 |

## Validation (`scans/validate.py`)

### What is checked

Points are checked in order along each branch. A point gets the **first** rule it breaks, and every later
point of that branch is `after_fail`. Those points were computed, but they were not validated or exported.
`E_rel` is relative to the branch's own step 0, not to the stage-2 energy. The rules, in the order the code
applies them:

| Status | Rule (thresholds exactly as in the code) | What a failing point means |
|---|---|---|
| `not_converged` | The step's output block has no `THE OPTIMIZATION HAS CONVERGED`, no final energy or no geometry. | No usable optimised structure at this target. |
| `constraint` | Measured coordinate differs from its target by more than 0.002 A (bond), 0.1 deg (angle) or 0.2 deg (twist, tilt; with wrap-around). | The constraint was not honoured, so the label (offset) would be wrong. |
| `bonds` | The covalent bond graph (CSD radii + 0.40 A; bonds to Zn excluded) differs from the stage-2 graph. | A ligand bond broke or formed, or an H moved: a different molecule. |
| `shell` | A donor is more than 2.8 A from Zn, **or** a donor other than the one being stretched moved more than 0.15 A from its stage-2 Zn-L distance. In angle, twist and tilt scans all donors are held to 0.15 A. | The first shell rearranged (a donor left, or the shell distorted beyond a small perturbation). The point no longer belongs to the species being scanned. |
| `new_contact` | A heavy atom that is not a donor comes within 2.6 A of Zn. | A new donor approaches: the coordination number is changing. |
| `energy_cap` | More than 40 kJ/mol above step 0. | Too high in energy to be thermally relevant. |
| `energy_drop` | Energy falls more than 2 kJ/mol below the **previous** point. | The branch found a lower-energy structure: the starting point was not the lowest minimum along this path. |
| `jump` | Any heavy-atom pair distance (Zn included, H excluded) changes by more than 0.3 A from the previous point. | A discontinuity (conformational switch) between neighbouring points. The change can be anywhere in the molecule, including far from Zn. |
| `ref_mismatch` | Step 0 only: a heavy-atom distance differs by more than 0.05 A from the stage-2 geometry, or the energy by more than 0.5 kJ/mol. | The branch did not start from the stage-2 minimum. |

How the checks interact:
- The checks are ordered. A lower minimum reached by a structural change is recorded as `shell`,
  `new_contact` or `jump`, not as `energy_drop`. Such drops are therefore missing from the results README's
  *Lower minimum than stage 2* list. Section (b) below lists both kinds.
- `ref_mismatch` is tested last, so it appears only when everything else passes.
- The README list holds only `energy_drop` first failures with E_rel < -2 kJ/mol relative to the branch start.
  An `energy_drop` above -2 kJ/mol relative to the start (a drop relative to the previous point only) is not in
  that list.

### Inconsistency between curation and validation (fact)

The donor cut-off for N/O at curation is 2.53 A (crystal, `curation/build_dft.py`). The `new_contact` limit in
validation is a flat 2.6 A. A crystal contact between 2.53 and 2.6 A is not a donor, yet it is a violation
from the start: LIVNAG O43 at 2.589 A, and KERJOI N5 at 2.530 A, which missed the cut-off by 0.0002 A. The
cut-offs also measure different things: curation uses the crystal, validation uses the stage-2 minimum. That
mismatch is the root cause of the not-exported complexes. Section (f) checks all 338 complexes against both.

### First failures over all published points

Each branch has at most one first failure; every later point of that branch is `after_fail`.

| Status | Points | Share of published points |
|---|---|---|
| pass | 89,807 | 89.8% |
| jump | 1304 | 1.30% |
| shell | 403 | 0.40% |
| energy_drop | 183 | 0.18% |
| new_contact | 130 | 0.13% |
| energy_cap | 39 | 0.04% |
| ref_mismatch | 5 | 0.00% |
| not_converged | 1 | 0.00% |
| after_fail | 8,160 | 8.2% |
| constraint | 0 | - |
| bonds | 0 | - |

### Pass rate by coordinate type and branch (published complexes)

| Coordinate | Branch | Points | Pass | Pass % | First failures |
|---|---|---|---|---|---|
| angle | neg | 21,945 | 17,551 | 80.0 | jump 475, shell 335, energy_drop 53, new_contact 29 |
| angle | pos | 21,934 | 19,230 | 87.7 | jump 359, new_contact 68, energy_drop 52, energy_cap 33 |
| bond | neg | 5,300 | 5,213 | 98.4 | jump 37, energy_drop 8, ref_mismatch 1 |
| bond | pos | 14,575 | 13,531 | 92.8 | jump 117, shell 31, new_contact 27, energy_drop 22 |
| tilt | neg | 14,542 | 13,998 | 96.3 | jump 89, energy_drop 15, shell 1, ref_mismatch 1 |
| tilt | pos | 14,542 | 14,004 | 96.3 | jump 87, energy_drop 17, new_contact 1, ref_mismatch 1 |
| twist | neg | 3,597 | 3,142 | 87.4 | jump 72, energy_drop 8, new_contact 2, shell 2 |
| twist | pos | 3,597 | 3,138 | 87.2 | jump 68, energy_drop 8, shell 5, new_contact 3 |

Points lost per first-failure type (the failing point plus the `after_fail` points behind it): jump 6,990, shell 1,551, energy_drop 1,084, new_contact 508, ref_mismatch 48, energy_cap 43, not_converged 1.

## Per-complex table

All 338 complexes, by name. *Points*: validated points (published) or planned points (otherwise). *First failures*: counts of the first failing point per branch (`after_fail` points not counted). *Below start*: branches whose first failure lies more than 2 kJ/mol below the branch start (any reason; `energy_drop` ones are the README list), with the lowest E_rel in kJ/mol. *Site*: NERSC account and number of branches that had a Perlmutter job. *Date*: publication date (`published.json`).

| Complex | Status | Atoms | Branches | Points | Pass | Pass % | First failures | after_fail | Below start | Site | Date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABIDEU | published | 69 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-24 |
| ADOLOU | published | 81 | 53 | 541 | 477 | 88.2 | shell 12, jump 6 | 46 | - | Aurora | 2026-10-27 |
| AHOQIY | published | 39 | 30 | 302 | 293 | 97.0 | jump 2, shell 1 | 6 | - | Aurora | 2026-10-24 |
| ALACUL | published | 39 | 30 | 302 | 294 | 97.4 | shell 3 | 5 | - | Aurora | 2026-10-23 |
| AMETZN | published | 33 | 30 | 302 | 294 | 97.4 | jump 2 | 6 | - | Aurora | 2026-10-23 |
| AYIFAP | published | 43 | 30 | 302 | 291 | 96.4 | shell 3 | 8 | - | Aurora | 2026-10-23 |
| AYUQOC | published | 51 | 30 | 302 | 290 | 96.0 | jump 1, shell 1 | 10 | - | Aurora | 2026-10-23 |
| AZIJIC | published | 78 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-30 |
| BAPZIC | published | 95 | 30 | 302 | 288 | 95.4 | jump 3, shell 1 | 10 | - | Aurora | 2026-10-31 |
| BELDUS | published | 59 | 30 | 302 | 238 | 78.8 | jump 13, shell 1, energy_cap 1 | 49 | - | Aurora | 2026-10-26 |
| BELFAA | published | 57 | 30 | 302 | 262 | 86.8 | jump 6, shell 1, energy_cap 1 | 32 | - | Aurora | 2026-11-01 |
| BELFEE | published | 47 | 30 | 302 | 297 | 98.3 | shell 1, energy_cap 1 | 3 | - | Aurora | 2026-10-24 |
| BELFII | published | 44 | 30 | 302 | 297 | 98.3 | shell 1, energy_cap 1 | 3 | - | Aurora | 2026-10-24 |
| BIJQOC | published | 95 | 30 | 302 | 281 | 93.0 | jump 6, new_contact 5 | 10 | - | Aurora | 2026-11-01 |
| BMBTZN | published | 61 | 30 | 302 | 297 | 98.3 | jump 1 | 4 | - | Aurora | 2026-10-23 |
| BOJMIX | published | 95 | 30 | 302 | 198 | 65.6 | jump 18, shell 1 | 85 | - | Aurora | 2026-11-01 |
| BTSQZN10 | published | 61 | 30 | 302 | 293 | 97.0 | shell 2, jump 1 | 6 | - | Aurora | 2026-11-01 |
| BUNNII | published | 137 | 30 | 302 | 182 | 60.3 | jump 20 | 100 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-31 |
| BUNTOW | published | 25 | 30 | 302 | 300 | 99.3 | shell 2 | 0 | - | Aurora | 2026-10-23 |
| CADKUO | published | 45 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| CAPWIB | published | 65 | 30 | 302 | 292 | 96.7 | shell 2 | 8 | - | Aurora + NERSC m2464 (30/30 br.) | 2026-10-31 |
| CATZUS10 | published | 137 | 30 | 302 | 268 | 88.7 | jump 9 | 25 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-11-01 |
| CAWKIW | published | 65 | 30 | 302 | 293 | 97.0 | shell 2 | 7 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-10-31 |
| CAXBEM | published | 69 | 30 | 302 | 286 | 94.7 | shell 4 | 12 | - | Aurora | 2026-10-27 |
| CAXBIQ | published | 59 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| CAXBUC | published | 64 | 30 | 302 | 227 | 75.2 | jump 10, shell 3, energy_drop 1 | 61 | - | Aurora | 2026-10-25 |
| CUCJAL | published | 53 | 30 | 302 | 292 | 96.7 | shell 2 | 8 | - | Aurora | 2026-10-23 |
| CURLOQ | published | 25 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-24 |
| CURLUW | published | 39 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| CUSGEE | published | 82 | 30 | 302 | 275 | 91.1 | shell 7 | 20 | - | Aurora | 2026-10-30 |
| DASFUY | published | 21 | 30 | 302 | 298 | 98.7 | shell 2 | 2 | - | Aurora | 2026-10-24 |
| DASMOZ | published | 41 | 30 | 302 | 296 | 98.0 | shell 2 | 4 | - | Aurora | 2026-10-24 |
| DASPOC | published | 43 | 30 | 302 | 295 | 97.7 | shell 2 | 5 | - | Aurora | 2026-10-24 |
| DETCEL | published | 61 | 30 | 302 | 290 | 96.0 | shell 2, jump 1 | 9 | - | Aurora | 2026-11-01 |
| DIFBIE | published | 45 | 30 | 302 | 293 | 97.0 | shell 2, jump 1 | 6 | - | Aurora | 2026-10-25 |
| DIFBOK | published | 55 | 30 | 302 | 264 | 87.4 | shell 8, jump 1, energy_cap 1 | 28 | 7 (-6.339) | Aurora | 2026-10-24 |
| DILGUA | published | 53 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-20 |
| DIVKAW | published | 96 | 30 | 302 | 262 | 86.8 | jump 9 | 31 | - | Aurora + NERSC m2464 (6/30 br.) | 2026-11-02 |
| DOMMOH | published | 37 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| DOMMUN | published | 45 | 30 | 302 | 291 | 96.4 | jump 1, shell 1 | 9 | - | Aurora | 2026-10-24 |
| DOZVOF | published | 111 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-29 |
| DUFYUY | published | 17 | 30 | 302 | 299 | 99.0 | shell 2 | 1 | - | Aurora | 2026-10-23 |
| EBEXIS | published | 66 | 28 | 280 | 180 | 64.3 | jump 16 | 84 | - | Aurora | 2026-10-27 |
| EDUPEZ | published | 47 | 30 | 302 | 225 | 74.5 | jump 15, shell 2 | 60 | - | Aurora | 2026-10-23 |
| EFEWUI | published | 38 | 30 | 302 | 298 | 98.7 | shell 2 | 2 | - | Aurora | 2026-10-23 |
| EGORAT | published | 65 | 30 | 302 | 286 | 94.7 | shell 2, jump 2 | 12 | - | Aurora | 2026-10-23 |
| ELISUO | published | 73 | 30 | 302 | 260 | 86.1 | jump 9, shell 2 | 31 | - | Aurora | 2026-11-01 |
| EPOFUL | **not exported** | 69 | 30 | 302 | 0 | 0.0 | branch starts: new_contact 30 | - | - | Aurora | 2026-11-01 |
| EQOFEW | published | 63 | 30 | 302 | 278 | 92.1 | jump 3, energy_drop 1 | 20 | - | Aurora | 2026-10-27 |
| ETEROK | published | 81 | 30 | 302 | 301 | 99.7 | jump 1 | 0 | - | Aurora | 2026-11-01 |
| EVOJOO | published | 49 | 30 | 302 | 287 | 95.0 | jump 3 | 12 | - | Aurora | 2026-10-23 |
| FADYOY | published | 41 | 30 | 302 | 280 | 92.7 | shell 2, jump 2 | 18 | - | Aurora | 2026-10-25 |
| FAJZAS | published | 78 | 30 | 302 | 300 | 99.3 | jump 1 | 1 | - | Aurora | 2026-10-27 |
| FATJUG | published | 49 | 30 | 302 | 280 | 92.7 | jump 5 | 17 | - | Aurora | 2026-10-19 |
| FAXYIP | published | 77 | 30 | 302 | 293 | 97.0 | shell 2, energy_cap 1 | 6 | - | Aurora + NERSC m2464 (25/30 br.) | 2026-11-01 |
| FAZJAT | published | 97 | 30 | 302 | 50 | 16.6 | jump 24, energy_drop 5 | 223 | 5 (-24.658) | Aurora + NERSC m2464 (3/30 br.) | 2026-11-02 |
| FECYIZ | **not exported** | 85 | 30 | 302 | 0 | 0.0 | branch starts: shell 30 | - | - | Aurora | 2026-11-01 |
| FEKQIV | published | 78 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-11-01 |
| FEKQOB | published | 84 | 30 | 302 | 296 | 98.0 | energy_drop 1, jump 1 | 4 | 1 (-2.832) | Aurora | 2026-10-31 |
| FEKQUH | published | 90 | 30 | 302 | 283 | 93.7 | energy_drop 3, jump 2 | 14 | 2 (-9.851) | Aurora + NERSC m2464 (2/30 br.) | 2026-11-02 |
| FEKRAO | published | 65 | 30 | 302 | 228 | 75.5 | energy_drop 9, jump 3, energy_cap 1 | 61 | 5 (-3.29) | Aurora | 2026-10-27 |
| FEKRES | published | 67 | 30 | 302 | 296 | 98.0 | jump 1, energy_drop 1 | 4 | - | Aurora | 2026-11-01 |
| FEKTAQ | published | 29 | 30 | 302 | 291 | 96.4 | shell 2, jump 2 | 7 | - | Aurora | 2026-10-24 |
| FEYNUT | published | 93 | 30 | 302 | 286 | 94.7 | new_contact 2, jump 2 | 12 | - | Aurora | 2026-10-23 |
| FILGEN | published | 43 | 30 | 302 | 298 | 98.7 | shell 1, energy_cap 1 | 2 | - | Aurora | 2026-10-24 |
| FIQTII | published | 53 | 30 | 302 | 301 | 99.7 | jump 1 | 0 | - | Aurora | 2026-11-01 |
| FIYQIP | published | 69 | 26 | 258 | 248 | 96.1 | energy_cap 2, new_contact 2 | 6 | - | Aurora | 2026-10-24 |
| FOQGOH | published | 71 | 30 | 302 | 255 | 84.4 | jump 6 | 41 | - | Aurora | 2026-11-01 |
| FUXMAM | published | 73 | 30 | 302 | 288 | 95.4 | jump 4 | 10 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-10-31 |
| FUXMEQ | published | 99 | 30 | 302 | 293 | 97.0 | jump 2, shell 1, energy_cap 1 | 5 | - | Aurora | 2026-10-31 |
| GADFUO | published | 51 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-23 |
| GAKKUY | published | 49 | 30 | 302 | 234 | 77.5 | jump 10, energy_drop 4 | 54 | 1 (-4.906) | Aurora | 2026-10-21 |
| GALGAC | published | 47 | 30 | 302 | 296 | 98.0 | shell 1, jump 1 | 4 | - | Aurora | 2026-10-24 |
| GALGEG | published | 49 | 30 | 302 | 298 | 98.7 | shell 1 | 3 | - | Aurora | 2026-10-19 |
| GALGIK | published | 47 | 30 | 302 | 274 | 90.7 | jump 6, shell 1 | 21 | - | Aurora | 2026-10-24 |
| GECLUZ | **not exported** | 73 | 29 | 291 | 0 | 0.0 | branch starts: new_contact 29 | - | - | Aurora | 2026-10-24 |
| GEQCUE | published | 47 | 30 | 302 | 239 | 79.1 | jump 7, energy_drop 2, shell 1 | 53 | 2 (-14.839) | Aurora | 2026-11-01 |
| GEXZOY | published | 81 | 30 | 302 | 276 | 91.4 | jump 7 | 19 | - | Aurora | 2026-10-25 |
| GILZEG | published | 49 | 30 | 302 | 299 | 99.0 | shell 1, new_contact 1 | 1 | - | Aurora | 2026-10-23 |
| GIXSUE | published | 65 | 30 | 302 | 214 | 70.9 | jump 13, shell 2, new_contact 2 | 71 | - | Aurora + NERSC m2464 (3/30 br.) | 2026-11-02 |
| GIXTAL | published | 57 | 30 | 302 | 153 | 50.7 | jump 19, energy_drop 3 | 127 | 1 (-4.886) | Aurora | 2026-10-28 |
| GOLCIU01 | published | 43 | 30 | 302 | 295 | 97.7 | shell 2, jump 2 | 3 | - | Aurora | 2026-10-25 |
| GOWRAL | published | 53 | 30 | 302 | 240 | 79.5 | jump 10 | 52 | - | Aurora | 2026-10-25 |
| GOYNIT | published | 79 | 30 | 302 | 175 | 57.9 | jump 14, shell 2 | 111 | - | Aurora | 2026-10-31 |
| GUCSAZ | published | 93 | 30 | 302 | 288 | 95.4 | shell 2, new_contact 2 | 10 | - | Aurora | 2026-10-31 |
| GUCSED | published | 105 | 30 | 302 | 288 | 95.4 | shell 2, new_contact 2, jump 2 | 8 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-28 |
| GUFGUJ | published | 77 | 30 | 302 | 300 | 99.3 | jump 1 | 1 | - | Aurora | 2026-10-31 |
| GUFHEU | published | 105 | 30 | 302 | 284 | 94.0 | jump 4 | 14 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-30 |
| GUWXUR | published | 75 | 30 | 302 | 298 | 98.7 | jump 2 | 2 | - | Aurora | 2026-10-31 |
| GUYHEN | published | 49 | 30 | 302 | 204 | 67.5 | shell 9, new_contact 4, jump 2 | 82 | 9 (-18.665) | Aurora | 2026-10-21 |
| HEFHOR | published | 87 | 30 | 302 | 271 | 89.7 | jump 4, shell 3, new_contact 2 | 22 | - | Aurora | 2026-11-01 |
| HEFHUX | published | 53 | 30 | 302 | 286 | 94.7 | shell 2, new_contact 2 | 12 | - | Aurora | 2026-10-23 |
| HIJGEM | published | 13 | 30 | 302 | 298 | 98.7 | jump 1, shell 1 | 2 | - | Aurora | 2026-10-24 |
| HOMQAC | published | 115 | 30 | 302 | 297 | 98.3 | shell 1, energy_cap 1 | 3 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| HOSXAR | published | 61 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-23 |
| HOZGAF | published | 96 | 30 | 302 | 137 | 45.4 | energy_drop 15, jump 6 | 144 | 15 (-16.099) | Aurora | 2026-10-31 |
| HOZGEJ | published | 99 | 30 | 302 | 282 | 93.4 | jump 4 | 16 | - | Aurora | 2026-10-25 |
| HOZGIN | published | 95 | 30 | 302 | 298 | 98.7 | jump 2 | 2 | - | Aurora | 2026-10-24 |
| HUBBIQ | published | 80 | 30 | 302 | 300 | 99.3 | shell 2 | 0 | - | Aurora | 2026-10-30 |
| HUCCIU | published | 50 | 30 | 302 | 296 | 98.0 | shell 3 | 3 | - | Aurora | 2026-10-19 |
| HULBIZ | published | 57 | 30 | 302 | 243 | 80.5 | shell 10, jump 1, energy_cap 1 | 47 | 10 (-6.333) | Aurora | 2026-10-24 |
| IBEQUB | published | 79 | 30 | 302 | 296 | 98.0 | shell 2, jump 1 | 3 | - | Aurora | 2026-10-31 |
| ICATOW | published | 77 | 30 | 302 | 272 | 90.1 | new_contact 7 | 23 | - | Aurora | 2026-10-25 |
| ICATUC | published | 85 | 30 | 302 | 196 | 64.9 | new_contact 11, jump 3 | 92 | - | Aurora | 2026-11-01 |
| ICAVAK | published | 101 | 30 | 302 | 291 | 96.4 | shell 2, jump 2, energy_drop 1 | 6 | 1 (-2.533) | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| ICAVEO | published | 81 | 30 | 302 | 300 | 99.3 | shell 2 | 0 | - | Aurora | 2026-10-31 |
| ICEHOP | published | 73 | 30 | 302 | 293 | 97.0 | jump 1, shell 1, energy_cap 1 | 6 | - | Aurora | 2026-10-24 |
| ICONOE | published | 85 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-30 |
| ICUCAL | published | 46 | 30 | 302 | 218 | 72.2 | jump 13, new_contact 1 | 70 | - | Aurora | 2026-10-24 |
| ICUCEP | published | 46 | 30 | 302 | 296 | 98.0 | energy_drop 1, shell 1, new_contact 1 | 3 | - | Aurora | 2026-10-24 |
| ICUCIT | published | 49 | 30 | 302 | 272 | 90.1 | jump 5, energy_drop 1, shell 1 | 22 | 1 (-10.556) | Aurora | 2026-10-23 |
| ICUCOZ | published | 49 | 30 | 302 | 295 | 97.7 | jump 1, shell 1, new_contact 1 | 4 | - | Aurora | 2026-10-23 |
| ICUDAM | published | 49 | 30 | 302 | 242 | 80.1 | jump 11, energy_drop 1 | 48 | - | Aurora | 2026-10-24 |
| IGURAD | published | 81 | 30 | 302 | 296 | 98.0 | jump 1, shell 1 | 4 | - | Aurora | 2026-10-30 |
| IGURIL | published | 78 | 30 | 302 | 288 | 95.4 | jump 4, energy_drop 1 | 9 | - | Aurora | 2026-10-31 |
| IQETOP | published | 39 | 30 | 302 | 268 | 88.7 | jump 5, energy_drop 2, shell 1 | 26 | - | Aurora | 2026-10-24 |
| IRETIJ | published | 67 | 30 | 302 | 283 | 93.7 | jump 4, shell 1 | 14 | - | Aurora | 2026-11-01 |
| JADMAG | published | 65 | 30 | 302 | 257 | 85.1 | jump 5, shell 3, new_contact 2 | 35 | - | Aurora | 2026-10-24 |
| JADMEK | published | 71 | 30 | 302 | 290 | 96.0 | shell 2, new_contact 2 | 8 | - | Aurora | 2026-10-23 |
| JAMJAJ | published | 47 | 30 | 302 | 298 | 98.7 | shell 2 | 2 | - | Aurora | 2026-10-24 |
| JAXFEW | published | 81 | 30 | 302 | 289 | 95.7 | shell 1, energy_drop 1, jump 1 | 10 | - | Aurora | 2026-10-31 |
| JEYTAI | published | 33 | 30 | 302 | 296 | 98.0 | shell 2 | 4 | - | Aurora | 2026-10-23 |
| JOCZEG | published | 81 | 30 | 302 | 296 | 98.0 | jump 1, shell 1, energy_cap 1 | 3 | - | Aurora + NERSC m2464 (30/30 br.) | 2026-10-31 |
| JUQXUO | published | 77 | 30 | 302 | 279 | 92.4 | jump 4, energy_drop 2 | 17 | - | Aurora + NERSC m2464 (27/30 br.) | 2026-11-01 |
| KAFFON | published | 49 | 30 | 302 | 295 | 97.7 | jump 2 | 5 | - | Aurora | 2026-11-01 |
| KAKVAT | published | 45 | 30 | 302 | 221 | 73.2 | jump 15, shell 1 | 65 | - | Aurora | 2026-10-25 |
| KAKVEX | published | 53 | 30 | 302 | 286 | 94.7 | jump 4 | 12 | - | Aurora | 2026-10-24 |
| KAKVIB01 | published | 49 | 30 | 302 | 204 | 67.5 | jump 13, shell 1, energy_cap 1 | 83 | - | Aurora | 2026-10-25 |
| KAKYAW | published | 51 | 30 | 302 | 231 | 76.5 | jump 13, shell 1, energy_drop 1 | 56 | 1 (-10.288) | Aurora | 2026-10-25 |
| KAKYEA | published | 51 | 30 | 302 | 299 | 99.0 | shell 1 | 2 | - | Aurora | 2026-10-24 |
| KAKYUQ | published | 47 | 30 | 302 | 244 | 80.8 | jump 15 | 43 | - | Aurora | 2026-10-25 |
| KALDIK | published | 49 | 30 | 302 | 271 | 89.7 | jump 8, shell 1 | 22 | - | Aurora | 2026-10-25 |
| KECGEI | **not exported** | 65 | 30 | 302 | 0 | 0.0 | branch starts: new_contact 30 | - | - | Aurora | 2026-10-25 |
| KERJOI | **not exported** | 41 | 29 | 291 | 0 | 0.0 | branch starts: shell 29 | - | - | Aurora | 2026-10-25 |
| KEXPAF | published | 80 | 30 | 302 | 249 | 82.5 | jump 8 | 45 | - | Aurora | 2026-10-31 |
| KEXPEJ | published | 80 | 30 | 302 | 285 | 94.4 | jump 2 | 15 | - | Aurora | 2026-10-31 |
| KEXPIN | published | 75 | 30 | 302 | 296 | 98.0 | jump 1, shell 1 | 4 | - | Aurora | 2026-10-31 |
| KEXQAG | published | 79 | 30 | 302 | 288 | 95.4 | jump 5, shell 1 | 8 | - | Aurora | 2026-10-31 |
| KEXQEK | published | 82 | 30 | 302 | 264 | 87.4 | jump 9 | 29 | - | Aurora | 2026-10-30 |
| KOMLIH01 | published | 53 | 30 | 302 | 295 | 97.7 | jump 1, shell 1, energy_cap 1 | 4 | - | Aurora | 2026-10-24 |
| KOPYOD | published | 47 | 30 | 302 | 291 | 96.4 | shell 3 | 8 | - | Aurora | 2026-10-23 |
| KOXDIN | published | 55 | 30 | 302 | 297 | 98.3 | jump 1, shell 1, new_contact 1 | 2 | - | Aurora | 2026-10-24 |
| KUBVEJ | **not exported** | 53 | 30 | 302 | 0 | 0.0 | branch starts: new_contact 30 | - | - | Aurora | 2026-10-27 |
| KUBVIN | published | 49 | 30 | 302 | 264 | 87.4 | new_contact 8, shell 1, energy_cap 1 | 28 | - | Aurora | 2026-10-25 |
| KUNDIH | published | 67 | 30 | 302 | 297 | 98.3 | shell 2 | 3 | - | Aurora | 2026-10-25 |
| LAJGIM | published | 89 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora + NERSC m2464 (30/30 br.) | 2026-11-01 |
| LAPYAD | published | 71 | 30 | 302 | 214 | 70.9 | energy_drop 9, jump 6 | 73 | 7 (-12.177) | Aurora | 2026-11-01 |
| LAPYOR | published | 75 | 30 | 302 | 286 | 94.7 | jump 5 | 11 | - | Aurora | 2026-10-24 |
| LAQBIP | published | 51 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-21 |
| LEMVAB | published | 37 | 30 | 302 | 294 | 97.4 | jump 2 | 6 | - | Aurora | 2026-10-24 |
| LEMVEF | published | 49 | 30 | 302 | 292 | 96.7 | jump 2 | 8 | - | Aurora | 2026-10-24 |
| LEQHAU | published | 17 | 30 | 302 | 300 | 99.3 | shell 2 | 0 | - | Aurora | 2026-10-23 |
| LIVNAG | **not exported** | 49 | 30 | 302 | 0 | 0.0 | branch starts: new_contact 30 | - | - | Aurora | 2026-10-25 |
| LIYDEE | published | 79 | 30 | 302 | 209 | 69.2 | jump 13, energy_drop 3 | 77 | - | Aurora | 2026-11-01 |
| LIYFEG01 | published | 59 | 30 | 302 | 281 | 93.0 | jump 4, shell 2 | 15 | - | Aurora | 2026-10-24 |
| LOHZAM | published | 85 | 30 | 302 | 258 | 85.4 | jump 10, new_contact 2 | 32 | - | Aurora + NERSC m2464 (3/30 br.) | 2026-11-02 |
| LUKREP | published | 53 | 30 | 302 | 291 | 96.4 | shell 2, jump 1 | 8 | - | Aurora | 2026-10-23 |
| LUVFUD | published | 60 | 30 | 302 | 301 | 99.7 | shell 1 | 0 | - | Aurora | 2026-10-25 |
| LUZTEF | published | 81 | 30 | 302 | 298 | 98.7 | shell 1, jump 1 | 2 | - | Aurora | 2026-10-26 |
| LUZTUV | published | 81 | 30 | 302 | 254 | 84.1 | jump 7 | 41 | - | Aurora | 2026-10-31 |
| LUZVAD | published | 80 | 30 | 302 | 299 | 99.0 | jump 2 | 1 | - | Aurora | 2026-11-01 |
| MAZBZN10 | published | 49 | 30 | 302 | 288 | 95.4 | shell 4 | 10 | - | Aurora | 2026-10-27 |
| MEPWOT | published | 38 | 28 | 280 | 248 | 88.6 | jump 5, shell 1 | 26 | - | Aurora | 2026-10-24 |
| MIYPAM | published | 89 | 30 | 302 | 245 | 81.1 | jump 13 | 44 | - | Aurora | 2026-10-23 |
| MIYVEW | published | 69 | 30 | 302 | 276 | 91.4 | jump 4 | 22 | - | Aurora | 2026-11-01 |
| MIYVIA | published | 63 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| MIYVOG | published | 59 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| MIYVUM | published | 67 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| MOYBAD | published | 57 | 30 | 302 | 270 | 89.4 | jump 4, shell 1 | 27 | - | Aurora | 2026-10-25 |
| MOZSIE | published | 53 | 30 | 302 | 282 | 93.4 | jump 3, shell 2 | 15 | - | Aurora | 2026-10-21 |
| MUJJOQ | published | 49 | 30 | 302 | 295 | 97.7 | shell 2, new_contact 1 | 4 | - | Aurora | 2026-10-25 |
| MUJJUW | published | 55 | 30 | 302 | 249 | 82.5 | shell 8, jump 2, energy_cap 1 | 42 | 7 (-6.28) | Aurora | 2026-10-24 |
| NAMSOJ | published | 104 | 30 | 302 | 212 | 70.2 | energy_drop 11, new_contact 2, jump 1 | 76 | 13 (-16.76) | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| NAYXAM | published | 71 | 30 | 302 | 282 | 93.4 | jump 5, shell 1 | 14 | - | Aurora | 2026-10-25 |
| NECTOG | published | 102 | 30 | 302 | 278 | 92.1 | shell 3, new_contact 3, jump 2 | 16 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| NEHKIU | published | 53 | 30 | 302 | 300 | 99.3 | shell 1 | 1 | - | Aurora | 2026-10-20 |
| NEQXUC | published | 80 | 30 | 302 | 301 | 99.7 | shell 1 | 0 | - | Aurora | 2026-10-31 |
| NEQYAJ01 | published | 78 | 30 | 302 | 299 | 99.0 | jump 1 | 2 | - | Aurora | 2026-10-31 |
| NESBUK | published | 61 | 30 | 302 | 176 | 58.3 | jump 21, energy_cap 2 | 103 | - | Aurora | 2026-10-31 |
| NESCAR | published | 63 | 30 | 302 | 168 | 55.6 | jump 20, energy_cap 2 | 112 | - | Aurora | 2026-10-25 |
| NIGTEC | published | 96 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-21 |
| NIHTEG | published | 45 | 30 | 302 | 280 | 92.7 | jump 5, shell 2 | 15 | - | Aurora | 2026-10-25 |
| NIHTIK | published | 51 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-25 |
| NIJVUY | published | 75 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-11-01 |
| NITZEW | published | 35 | 30 | 302 | 292 | 96.7 | shell 2, jump 1 | 7 | - | Aurora | 2026-10-24 |
| NOCNEY | published | 65 | 30 | 302 | 270 | 89.4 | new_contact 7 | 25 | - | Aurora | 2026-10-24 |
| NONKUX | published | 93 | 30 | 302 | 285 | 94.4 | shell 2, new_contact 2, jump 1 | 12 | - | Aurora | 2026-10-31 |
| NONLEI | published | 117 | 30 | 302 | 288 | 95.4 | shell 2, new_contact 2 | 10 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-28 |
| NUYWOV | published | 55 | 30 | 302 | 282 | 93.4 | jump 4 | 16 | - | Aurora | 2026-10-24 |
| OCOZAJ | published | 43 | 30 | 302 | 286 | 94.7 | jump 4, shell 1, energy_drop 1 | 10 | - | Aurora | 2026-10-24 |
| OCOZOX | published | 37 | 30 | 302 | 296 | 98.0 | jump 2 | 4 | - | Aurora | 2026-10-24 |
| OGUGON | **not exported** | 53 | 30 | 302 | 0 | 0.0 | branch starts: new_contact 30 | - | - | Aurora | 2026-10-23 |
| OGUWUJ | published | 86 | 30 | 302 | 291 | 96.4 | jump 3 | 8 | - | Aurora | 2026-10-31 |
| OJEKIX | published | 95 | 30 | 302 | 174 | 57.6 | jump 16 | 112 | - | Aurora | 2026-10-24 |
| OJEKOD | published | 135 | 30 | 302 | 291 | 96.4 | jump 3 | 8 | - | Aurora | 2026-10-25 |
| OJEKUJ | published | 137 | 30 | 302 | 266 | 88.1 | jump 9 | 27 | - | Aurora + NERSC m5268 (14/30 br.) | 2026-10-26 |
| OJELEU | published | 135 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-22 |
| OJELIY | published | 91 | 30 | 302 | 254 | 84.1 | jump 10 | 38 | - | Aurora | 2026-10-31 |
| OJELOE | published | 109 | 30 | 302 | 229 | 75.8 | jump 10, energy_drop 3 | 60 | 2 (-2.511) | Aurora + NERSC m5268 (30/30 br.) | 2026-10-28 |
| OKAROJ | published | 47 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-23 |
| OKIWIQ | published | 59 | 30 | 302 | 292 | 96.7 | shell 2, jump 1 | 7 | - | Aurora | 2026-11-01 |
| OLIPEG | published | 57 | 30 | 302 | 189 | 62.6 | jump 21 | 92 | - | Aurora | 2026-10-25 |
| OVAPIL | published | 75 | 30 | 302 | 286 | 94.7 | jump 6 | 10 | - | Aurora | 2026-11-01 |
| OVAQIM | published | 81 | 30 | 302 | 267 | 88.4 | jump 5 | 30 | - | Aurora | 2026-10-30 |
| OYASOZ | published | 89 | 30 | 302 | 287 | 95.0 | jump 2, shell 1 | 12 | - | Aurora | 2026-10-30 |
| OYASUF | published | 87 | 30 | 302 | 295 | 97.7 | shell 2 | 5 | - | Aurora | 2026-10-31 |
| OYATEQ | published | 92 | 30 | 302 | 291 | 96.4 | jump 2, shell 2 | 7 | - | Aurora | 2026-10-28 |
| PAGFEM | published | 33 | 30 | 302 | 295 | 97.7 | jump 1, shell 1 | 5 | - | Aurora | 2026-10-24 |
| PAGJOA | published | 77 | 30 | 302 | 253 | 83.8 | shell 9, jump 4 | 36 | - | Aurora | 2026-10-31 |
| PEQSEK | published | 70 | 30 | 302 | 287 | 95.0 | shell 3, new_contact 3 | 9 | - | Aurora | 2026-10-24 |
| PMTCZN10 | published | 73 | 30 | 302 | 297 | 98.3 | jump 3 | 2 | - | Aurora | 2026-11-01 |
| POHTOV | published | 43 | 30 | 302 | 290 | 96.0 | jump 2, shell 1 | 9 | - | Aurora | 2026-10-24 |
| POZDIR | published | 64 | 30 | 302 | 295 | 97.7 | shell 2, new_contact 1 | 4 | - | Aurora | 2026-11-01 |
| PTOLZN01 | published | 53 | 30 | 302 | 171 | 56.6 | jump 17 | 114 | - | Aurora | 2026-10-26 |
| PUMRAQ | published | 57 | 30 | 302 | 285 | 94.4 | new_contact 5, shell 1 | 11 | - | Aurora | 2026-10-24 |
| PUNTEZ | published | 69 | 30 | 302 | 299 | 99.0 | jump 1, shell 1 | 1 | - | Aurora | 2026-11-01 |
| PUZKUQ | published | 33 | 30 | 302 | 289 | 95.7 | shell 2, jump 1 | 10 | - | Aurora | 2026-10-24 |
| QADDEF | published | 85 | 30 | 302 | 281 | 93.0 | jump 5, shell 2, new_contact 1 | 12 | 1 (-6.959) | Aurora | 2026-10-31 |
| QAGWII | published | 73 | 30 | 302 | 284 | 94.0 | shell 2, jump 2 | 14 | - | Aurora | 2026-10-25 |
| QASRIL | published | 53 | 30 | 302 | 263 | 87.1 | jump 7 | 32 | - | Aurora | 2026-10-24 |
| QASROR | published | 81 | 30 | 302 | 281 | 93.0 | jump 4 | 17 | - | Aurora | 2026-10-31 |
| QAWBAS | published | 79 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-30 |
| QEJKEV | published | 75 | 30 | 302 | 295 | 97.7 | shell 2, jump 1 | 4 | - | Aurora | 2026-11-01 |
| QELPED | published | 49 | 30 | 302 | 282 | 93.4 | jump 4, shell 2 | 14 | - | Aurora | 2026-10-24 |
| QEMXUE | published | 89 | 30 | 302 | 236 | 78.1 | jump 14 | 52 | - | Aurora | 2026-10-31 |
| QIBVAZ | published | 45 | 30 | 302 | 300 | 99.3 | shell 1 | 1 | - | Aurora | 2026-10-25 |
| QISJUA | published | 91 | 30 | 302 | 274 | 90.7 | jump 4, shell 2 | 22 | - | Aurora + NERSC m2464 (1/30 br.) | 2026-11-02 |
| QISKEL | published | 89 | 30 | 302 | 227 | 75.2 | jump 14, shell 1 | 60 | - | Aurora | 2026-11-01 |
| QOBKAW | published | 37 | 30 | 302 | 291 | 96.4 | jump 2, shell 1 | 8 | - | Aurora | 2026-10-24 |
| QOQYAW | published | 71 | 30 | 302 | 289 | 95.7 | jump 2, shell 1, new_contact 1 | 9 | - | Aurora | 2026-10-25 |
| QOQYEA | published | 50 | 30 | 302 | 292 | 96.7 | jump 2, shell 1, new_contact 1 | 6 | - | Aurora | 2026-10-19 |
| QORPUI | published | 52 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-20 |
| QUFSAL | published | 17 | 30 | 302 | 298 | 98.7 | shell 2 | 2 | - | Aurora | 2026-10-23 |
| QUQGEO | published | 31 | 30 | 302 | 295 | 97.7 | jump 3 | 4 | - | Aurora | 2026-10-24 |
| RADPOB | published | 81 | 26 | 258 | 254 | 98.4 | energy_cap 4 | 0 | - | Aurora | 2026-10-24 |
| RAGDUY | published | 49 | 30 | 302 | 267 | 88.4 | jump 6 | 29 | - | Aurora | 2026-10-25 |
| RAGFAG | published | 67 | 30 | 302 | 275 | 91.1 | jump 7 | 20 | - | Aurora | 2026-11-01 |
| RAJHOA | published | 57 | 40 | 405 | 317 | 78.3 | shell 17 | 71 | - | Aurora | 2026-10-24 |
| RATHOL | published | 55 | 30 | 302 | 294 | 97.4 | jump 2 | 6 | - | Aurora | 2026-10-21 |
| RAXDAV | published | 37 | 30 | 302 | 292 | 96.7 | jump 3 | 7 | - | Aurora | 2026-10-24 |
| RAYBIC | published | 124 | 30 | 302 | 156 | 51.7 | jump 20, ref_mismatch 1 | 125 | - | Aurora + NERSC m5268 (28/30 br.) | 2026-10-28 |
| REJBUD | published | 102 | 30 | 302 | 284 | 94.0 | jump 5 | 13 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| RIBMEV | published | 59 | 30 | 302 | 205 | 67.9 | shell 9, ref_mismatch 4, jump 1 | 83 | 8 (-6.282) | Aurora | 2026-10-25 |
| RIBMIZ | published | 53 | 30 | 302 | 235 | 77.8 | shell 11 | 56 | 10 (-6.116) | Aurora | 2026-10-24 |
| RUKJAL | published | 37 | 30 | 302 | 294 | 97.4 | jump 2 | 6 | - | Aurora | 2026-10-24 |
| SEJZOW | published | 85 | 30 | 302 | 292 | 96.7 | jump 3 | 7 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-11-01 |
| SENFOG | published | 59 | 30 | 302 | 296 | 98.0 | shell 3, new_contact 3 | 0 | - | Aurora | 2026-10-23 |
| SEWZUS | published | 57 | 30 | 302 | 261 | 86.4 | jump 7 | 34 | - | Aurora | 2026-10-23 |
| SEYCIL | published | 61 | 30 | 302 | 281 | 93.0 | jump 3, shell 2 | 16 | - | Aurora | 2026-10-23 |
| SIHXIR | published | 75 | 30 | 302 | 151 | 50.0 | energy_drop 11, jump 7, energy_cap 1 | 132 | 10 (-2.643) | Aurora | 2026-11-01 |
| SIJKUR | published | 47 | 30 | 302 | 293 | 97.0 | shell 2 | 7 | - | Aurora | 2026-10-24 |
| SOCSAE | published | 51 | 30 | 302 | 299 | 99.0 | energy_drop 2 | 1 | - | Aurora | 2026-10-20 |
| SONROE | published | 125 | 30 | 302 | 289 | 95.7 | shell 3, new_contact 3, jump 1 | 6 | - | Aurora + NERSC m5268 (29/30 br.) | 2026-10-28 |
| SUYTIR | published | 53 | 30 | 302 | 291 | 96.4 | shell 2, jump 1 | 8 | - | Aurora | 2026-10-21 |
| SUYTOX | published | 67 | 30 | 302 | 281 | 93.0 | jump 5, shell 2 | 14 | - | Aurora | 2026-10-24 |
| TACIZN | published | 41 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| TAKZIQ | published | 69 | 30 | 302 | 292 | 96.7 | jump 2 | 8 | - | Aurora | 2026-10-25 |
| TAKZUB | published | 17 | 30 | 302 | 294 | 97.4 | jump 2 | 6 | - | Aurora | 2026-10-24 |
| TANRAE | published | 63 | 30 | 302 | 200 | 66.2 | jump 21 | 81 | - | Aurora | 2026-10-25 |
| TARNIJ | published | 53 | 30 | 302 | 281 | 93.0 | jump 4, energy_drop 1 | 16 | 1 (-2.476) | Aurora | 2026-10-24 |
| TAVZEW | published | 75 | 48 | 486 | 484 | 99.6 | shell 2 | 0 | - | Aurora | 2026-10-24 |
| TBZZNP01 | published | 51 | 30 | 302 | 226 | 74.8 | jump 14 | 62 | - | Aurora | 2026-10-21 |
| TELRIN | published | 69 | 30 | 302 | 200 | 66.2 | energy_drop 10, jump 5, energy_cap 1 | 86 | 10 (-8.018) | Aurora | 2026-11-01 |
| TELROT | published | 71 | 30 | 302 | 206 | 68.2 | jump 11, energy_drop 5, energy_cap 1 | 79 | 2 (-2.534) | Aurora | 2026-11-01 |
| TELRUZ | published | 77 | 30 | 302 | 161 | 53.3 | jump 18, shell 1 | 122 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-11-01 |
| TELSAG | published | 73 | 30 | 302 | 201 | 66.6 | jump 20 | 81 | - | Aurora | 2026-11-01 |
| TEYSIA | published | 67 | 30 | 302 | 217 | 71.9 | jump 15, shell 1 | 69 | - | Aurora | 2026-11-01 |
| TEYSOG | published | 73 | 30 | 302 | 287 | 95.0 | jump 4, energy_drop 1, shell 1 | 8 | 1 (-27.45) | Aurora + NERSC m2464 (25/30 br.) | 2026-11-01 |
| TIFNOO | published | 55 | 30 | 302 | 241 | 79.8 | shell 8, new_contact 5, energy_cap 1 | 47 | 8 (-44.024) | Aurora | 2026-10-27 |
| TIFNUU | published | 65 | 30 | 302 | 260 | 86.1 | jump 6, energy_drop 4 | 32 | 3 (-2.298) | Aurora + NERSC m2464 (27/30 br.) | 2026-11-01 |
| TIQLEK | published | 83 | 30 | 302 | 285 | 94.4 | jump 4 | 13 | - | Aurora | 2026-10-30 |
| TIQLOU | published | 69 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| TIXQOH | published | 92 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-22 |
| TIXREY | published | 48 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| UCOLIH | published | 69 | 30 | 302 | 204 | 67.5 | jump 13 | 85 | - | Aurora | 2026-11-01 |
| UCOLON | published | 82 | 30 | 302 | 287 | 95.0 | energy_drop 4, jump 3 | 8 | 1 (-8.969) | Aurora + NERSC m2464 (4/30 br.) | 2026-11-02 |
| UDOCUL | published | 70 | 30 | 302 | 300 | 99.3 | shell 1 | 1 | - | Aurora | 2026-10-26 |
| UDODOG | published | 90 | 30 | 302 | 234 | 77.5 | new_contact 9, jump 1 | 58 | - | Aurora | 2026-10-27 |
| UDODUM | published | 75 | 30 | 302 | 283 | 93.7 | new_contact 8 | 11 | - | Aurora | 2026-11-01 |
| UDOFAU | published | 74 | 30 | 302 | 299 | 99.0 | jump 1 | 2 | - | Aurora | 2026-11-01 |
| UFUROC | published | 29 | 30 | 302 | 181 | 59.9 | energy_drop 16 | 105 | 14 (-3.621) | Aurora | 2026-10-24 |
| UMEVOY | published | 39 | 30 | 302 | 291 | 96.4 | shell 3 | 8 | - | Aurora | 2026-10-24 |
| UQOWIH | published | 65 | 30 | 302 | 287 | 95.0 | jump 3, shell 2 | 10 | - | Aurora | 2026-10-24 |
| UTAXAQ | published | 81 | 30 | 302 | 242 | 80.1 | jump 12 | 48 | - | Aurora | 2026-10-30 |
| UWAVOF | published | 71 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-11-01 |
| UYORAE | published | 93 | 30 | 302 | 274 | 90.7 | jump 4, shell 2 | 22 | - | Aurora + NERSC m2464 (30/30 br.) | 2026-11-02 |
| VAGJES | published | 35 | 30 | 302 | 296 | 98.0 | shell 2 | 4 | - | Aurora | 2026-10-24 |
| VAGJIW | published | 55 | 30 | 302 | 292 | 96.7 | shell 2 | 8 | - | Aurora | 2026-10-25 |
| VATSAM | published | 67 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-11-01 |
| VATSEQ | published | 81 | 30 | 302 | 286 | 94.7 | jump 3, shell 2 | 11 | - | Aurora | 2026-11-01 |
| VEKDUL | published | 65 | 30 | 302 | 212 | 70.2 | jump 10, energy_drop 1 | 79 | - | Aurora | 2026-10-25 |
| VEKFAT | published | 74 | 30 | 302 | 298 | 98.7 | jump 2, shell 1 | 1 | - | Aurora | 2026-10-27 |
| VEPXOD | published | 49 | 30 | 302 | 293 | 97.0 | shell 2 | 7 | - | Aurora | 2026-10-24 |
| VIBLAT | published | 72 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-25 |
| VIKDUP | published | 37 | 30 | 302 | 289 | 95.7 | shell 1, energy_cap 1, jump 1 | 10 | - | Aurora | 2026-10-25 |
| VOJHIO | published | 53 | 30 | 302 | 97 | 32.1 | jump 24 | 181 | - | Aurora | 2026-10-21 |
| VOYFUN | published | 81 | 30 | 302 | 289 | 95.7 | jump 3, shell 1 | 9 | - | Aurora | 2026-10-31 |
| VUHDIL | published | 89 | 30 | 302 | 294 | 97.4 | jump 3 | 5 | - | Aurora | 2026-10-25 |
| VUVVAM | published | 55 | 30 | 302 | 254 | 84.1 | jump 8, shell 2 | 38 | - | Aurora | 2026-10-21 |
| WACPAS | published | 61 | 30 | 302 | 278 | 92.1 | jump 3, shell 1, energy_cap 1 | 19 | - | Aurora | 2026-10-25 |
| WAJJIB | published | 93 | 30 | 302 | 182 | 60.3 | jump 16 | 104 | - | Aurora | 2026-11-01 |
| WAJNAW | published | 64 | 30 | 302 | 301 | 99.7 | shell 1 | 0 | - | Aurora | 2026-10-31 |
| WAJNEA | published | 65 | 30 | 302 | 297 | 98.3 | shell 1, jump 1 | 3 | - | Aurora | 2026-10-24 |
| WEDVEG | published | 51 | 30 | 302 | 293 | 97.0 | energy_drop 1, jump 1 | 7 | - | Aurora | 2026-10-23 |
| WEDVIK | published | 49 | 30 | 302 | 275 | 91.1 | new_contact 2, shell 2, jump 1 | 20 | 2 (-29.293) | Aurora | 2026-11-01 |
| WEQZAT01 | published | 48 | 30 | 302 | 290 | 96.0 | jump 3, shell 1 | 8 | - | Aurora + NERSC m2464 (26/30 br.) | 2026-11-01 |
| WIGBIX | published | 121 | 30 | 302 | 216 | 71.5 | jump 13, energy_drop 1 | 72 | 1 (-2.309) | Aurora + NERSC m5268 (30/30 br.) | 2026-10-29 |
| WITLAM | published | 43 | 30 | 302 | 291 | 96.4 | jump 2, shell 1, energy_cap 1 | 7 | - | Aurora | 2026-10-25 |
| WONYUW | published | 33 | 28 | 280 | 254 | 90.7 | jump 4, shell 1, energy_cap 1 | 20 | - | Aurora | 2026-10-25 |
| WORLUK | published | 69 | 30 | 302 | 293 | 97.0 | shell 2, jump 1 | 6 | - | Aurora | 2026-10-27 |
| WORMAR | published | 113 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora + NERSC m5268 (30/30 br.) | 2026-10-27 |
| WUCGIN | published | 51 | 30 | 302 | 249 | 82.5 | shell 9, jump 1, energy_cap 1 | 42 | 9 (-5.726) | Aurora | 2026-10-20 |
| WUJZOS | published | 127 | 30 | 302 | 154 | 51.0 | energy_drop 14, jump 9 | 125 | 9 (-5.665) | Aurora + NERSC m5268 (4/30 br.) | 2026-10-26 |
| XAJQAB | published | 95 | 30 | 302 | 277 | 91.7 | jump 4, energy_drop 1 | 20 | 1 (-21.073) | Aurora | 2026-10-23 |
| XAYGEL | published | 77 | 30 | 302 | 222 | 73.5 | jump 14 | 66 | - | Aurora | 2026-10-25 |
| XENWET | published | 25 | 30 | 302 | 298 | 98.7 | shell 2 | 2 | - | Aurora | 2026-10-24 |
| XIGZUI | published | 69 | 30 | 302 | 223 | 73.8 | jump 12, shell 2 | 65 | - | Aurora | 2026-10-25 |
| XILGIJ | published | 49 | 30 | 302 | 290 | 96.0 | jump 3, energy_drop 1 | 8 | - | Aurora | 2026-10-24 |
| XIXTEG | published | 59 | 30 | 302 | 195 | 64.6 | energy_drop 11, jump 8 | 88 | 11 (-6.57) | Aurora | 2026-10-25 |
| XIYHET | published | 73 | 30 | 302 | 179 | 59.3 | jump 18 | 105 | - | Aurora | 2026-11-01 |
| XIZPOL | published | 82 | 30 | 302 | 275 | 91.1 | jump 4, shell 1, new_contact 1 | 21 | - | Aurora | 2026-11-01 |
| XOGYUQ | published | 49 | 30 | 302 | 204 | 67.5 | jump 16, energy_drop 1 | 81 | - | Aurora | 2026-10-25 |
| XOGZAX | published | 61 | 30 | 302 | 272 | 90.1 | jump 5 | 25 | - | Aurora | 2026-10-24 |
| XUBBAX | published | 71 | 30 | 302 | 279 | 92.4 | jump 4, shell 1 | 18 | - | Aurora | 2026-11-01 |
| XUSTAG | published | 21 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-23 |
| XUVWES | published | 65 | 30 | 302 | 284 | 94.0 | jump 5 | 13 | - | Aurora | 2026-11-01 |
| YACTOP | published | 81 | 30 | 302 | 296 | 98.0 | jump 3 | 3 | - | Aurora | 2026-11-01 |
| YACTUV | published | 78 | 30 | 302 | 243 | 80.5 | new_contact 8, jump 1, energy_drop 1 | 49 | - | Aurora | 2026-10-31 |
| YOLCOR | published | 45 | 30 | 302 | 234 | 77.5 | jump 11, shell 1 | 56 | - | Aurora | 2026-10-24 |
| YOTFEU | published | 17 | 30 | 302 | 299 | 99.0 | shell 2 | 1 | - | Aurora | 2026-10-24 |
| ZACWOP | published | 45 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-24 |
| ZAHCAM | published | 71 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-10-24 |
| ZAZQUM | published | 49 | 30 | 302 | 222 | 73.5 | jump 11, energy_drop 2 | 67 | 2 (-7.364) | Aurora | 2026-11-01 |
| ZAZRIB | published | 49 | 30 | 302 | 302 | 100.0 | - | 0 | - | Aurora | 2026-11-01 |
| ZEFGAS | published | 51 | 30 | 302 | 294 | 97.4 | shell 2 | 6 | - | Aurora | 2026-10-19 |
| ZIBCAR | published | 57 | 30 | 302 | 282 | 93.4 | jump 5, shell 1, new_contact 1 | 13 | - | Aurora | 2026-10-24 |
| ZNDITZ11 | published | 59 | 30 | 302 | 178 | 58.9 | jump 10, energy_drop 10 | 104 | 8 (-2.658) | Aurora | 2026-10-24 |
| ZUKRII | published | 75 | 30 | 302 | 291 | 96.4 | shell 2, energy_drop 1 | 8 | 1 (-2.724) | Aurora | 2026-11-01 |

## Complexes that need Riti's attention

Sections (a) to (g) are ordered by consequence. Each one gives evidence first, then a recommended action. The
recommended actions are collected as numbered choices under *Decisions for Riti*.

### (a) Finished but not exported

| Complex | Atoms | Branches | Planned points | Reason recorded by publish.py | Finished | Site |
|---|---|---|---|---|---|---|
| EPOFUL | 69 | 30 | 302 | all 30 branches finished; branch starts fail validation (new_contact 30) | 2026-11-01 | Aurora |
| FECYIZ | 85 | 30 | 302 | all 30 branches finished; branch starts fail validation (shell 30) | 2026-11-01 | Aurora |
| GECLUZ | 73 | 29 | 291 | all 29 branches finished; branch starts fail validation (new_contact 29) | 2026-10-24 | Aurora |
| KECGEI | 65 | 30 | 302 | all 30 branches finished; branch starts fail validation (new_contact 30) | 2026-10-25 | Aurora |
| KERJOI | 41 | 29 | 291 | all 29 branches finished; branch starts fail validation (shell 29) | 2026-10-25 | Aurora |
| KUBVEJ | 53 | 30 | 302 | all 30 branches finished; branch starts fail validation (new_contact 30) | 2026-10-27 | Aurora |
| LIVNAG | 49 | 30 | 302 | all 30 branches finished; branch starts fail validation (new_contact 30) | 2026-10-25 | Aurora |
| OGUGON | 53 | 30 | 302 | all 30 branches finished; branch starts fail validation (new_contact 30) | 2026-10-23 | Aurora |

**Why these complexes export nothing.** This is a read-only investigation from 2026-10-31. It covers the six
complexes that had finished by then: GECLUZ, KECGEI, KERJOI, KUBVEJ, LIVNAG and OGUGON. Facts and *inference*
are marked.

The validation code works as written. Re-running the `validate.py` logic over all 1,790 points of the six
reproduces exactly the published reasons. The donor indices match the geometry, and the `coords.json` donors
equal the `.meta` donors. Charge and multiplicity are consistent: 0/1 for five complexes and +2/1 for OGUGON.
All six have even electron counts. The cause is upstream: the stage-2 B3LYP minimum has a different Zn first
shell from the crystal-derived donor list (fact).

Riti's stage-1 summary (`results/stage1_summary_2026-10-14.csv`, column `new_ZnX`) had already flagged three of
them at stage 1 (r2SCAN-3c): GECLUZ, KECGEI and LIVNAG. KERJOI, KUBVEJ and OGUGON changed only in the B3LYP
stage-2 optimisation (fact).

| REF | Atoms that moved in, crystal -> stage 2 (A) | Original donors, crystal -> stage 2 (A) | CN | Step-0 failure | Nature (*inference*) |
|---|---|---|---|---|---|
| GECLUZ | S1 3.012->2.526, S2 3.012->2.526 (2nd S of each dithiocarbamate) | S3/S4 2.332->2.548, N51/N52 2.166->2.206; S3-Zn-S4 169.0 deg | 4->6 | `new_contact` S1/S2 2.526 (29/29) | genuine: anisobidentate dtc becomes symmetric bidentate, octahedral S4N2; r2SCAN-3c agrees |
| KECGEI | O11 2.830->2.393, O12 2.719->2.340 (acenaphthenone C=O/C-O-) | S 2.33->2.45, N 2.05/2.07->2.12 | 4->6 | `new_contact` O12 2.340, O11 2.393 (30/30) | genuine: ONS tridentate, mer octahedral N2S2O2 |
| LIVNAG | O42 2.731->2.412, O43 2.589->2.405 (oxindole C=O) | S 2.31/2.38->2.45, N 2.03/2.08->2.11 | 4->6 | `new_contact` O43 2.405, O42 2.412 (30/30) | genuine: ONS tridentate; O43 already below 2.6 A in the crystal |
| KUBVEJ | N9 2.777->2.454 (pyrimidine ring N next to C-S; 4-membered N,S chelate) | S 2.28/2.30->2.35/2.39, N 2.08/2.12->2.12/2.16 | 4->5 | `new_contact` N9 2.454 (30/30) | soft, depends on the method: r2SCAN-3c keeps N9 out; in the scans N9 spans 2.09-3.00 A and the other ring N11 spans 2.16-3.18 A (hemilabile, flat surface) |
| KERJOI | N5 2.530->1.996 (thiadiazole ring N next to C-S), N6 3.89->2.90 | **S2 2.355->3.520 (left the shell)**, N 1.99-2.08; S2-Zn-N7 163 deg | N3S -> N4 | `shell` S2 3.520 > 2.8 (29/29); N5 masked because `shell` is checked first | linkage isomer S->N; the stage-2 species is not the CSD compound |
| OGUGON | O43 2.975->2.402, O40 3.125->2.468 (two of four ligand OH) | N 2.06-2.07->2.09-2.19; O-Zn-O 81.2 deg | 4->6 (cis N4O2) | `new_contact` O43 2.402, O40 2.468 (30/30) | probably an artefact of the model: the CSD entry is [Zn(L)2]Cl2, the Cl- were removed and the dication computed at +2 in CPCM; the OH groups, at 2.85-3.13 A in the crystal, most likely H-bond to Cl- (chloride positions are not in our files) |

29 rather than 30 branches for GECLUZ and KERJOI is expected: one angle branch each would pass 178 deg
(S3-Zn-S4 at 169.0 deg, S2-Zn-N7 at 163.0 deg).

**What the scans hold, if the donors are redefined to the stage-2 shell.** These numbers come from
re-validating the existing points, with zero compute and unchanged thresholds. The added donors are:
GECLUZ S1,S2; KECGEI O11,O12; LIVNAG O42,O43; KUBVEJ N9; OGUGON O40,O43; KERJOI N5 added and S2 removed.

| REF | Pass / points | Branch starts pass | First failures | Assessment |
|---|---|---|---|---|
| GECLUZ | 266 / 291 | 29/29 | 4 shell, 4 jump (late angle and tilt steps) | usable |
| KECGEI | 270 / 302 | 30/30 | 7 shell (angle steps 3-10) | usable |
| LIVNAG | 261 / 302 | 30/30 | 8 shell (angle steps 3-9) | usable |
| OGUGON | 238 / 302 | 30/30 | 15 shell (mostly angles, steps 4-10) | usable as a labelled "N4O2 solution model" |
| KERJOI | 285 / 291 | 29/29 | 1 jump, 1 energy_cap | 11 of 29 branches scan coordinates of S2, now a non-bonded atom at 3.5 A: valid geometries, wrong labels |
| KUBVEJ | 153 / 302 | 30/30 | 19 shell, 4 jump, many at steps 2-5 | a biased half of a floppy system |

All branches terminated normally. No `energy_drop` occurs under the new donor set. The existing branches do
not scan the new bonds: there is no Zn-O, Zn-S1/S2, Zn-N9 or Zn-N5 stretch, no angle or tilt involving a new
donor, and the twist uses the four original donors.

**Options and cost.** Cost basis: each of the six took 291-302 points and 2,600-4,100 optimisation cycles. The
final `scan.out` files log 68-94 job-hours on 4 cores. That is about 3-4 node-hours at 24 jobs per node, a lower
bound because restarted branches log only their last run. The campaign median of 41 min per point gives about
8.5 node-hours per complex. A complete redo is therefore **about 3-9 node-hours per complex**, plus under 0.5
node-hours for a stage-2 re-optimisation. That is under 60 node-hours for all six, negligible on ModCon, which
is not a constraint. The real costs are wall time and a code change.

- **(b) Redefine the donors and re-validate (0 compute).** This needs a per-complex donor override read by
  `validate.py` and `publish.py`, for example a `donors` field in a small override file. It gains about 1,470
  points for the six. Optionally, add branches for the new donors (their bonds, angles and tilts): about
  200-260 extra points per complex, at about 3-9 node-hours each.
- **(a) Redo stage 2 differently.**
  - OGUGON: neutral [Zn(L)2]Cl2 with the two crystal chlorides (positions from the CIF), then rerun the 30
    branches. About 4-9 node-hours, plus recovering the Cl positions.
  - KERJOI: an S-bound B3LYP minimum may not exist. Stage 2 started S-bound and switched. Keeping it S-bound
    would need a Zn-S constraint in every branch, which breaks the "relaxed minimum" premise. Not recommended.
  - KUBVEJ: neither a constrained contact nor the r2SCAN-3c geometry would cure the floppiness. Not
    recommended.
  - GECLUZ, KECGEI, LIVNAG: re-optimising would give the same six-coordinate minimum (*inference*: r2SCAN-3c and
    B3LYP agree). Not useful.
- **(c) Drop the complex (0 compute).** The scans stay on disk.

| REF | Recommendation |
|---|---|
| GECLUZ | (b) redefine donors -> 266 points; optionally add new-donor branches |
| KECGEI | (b) -> 270 points |
| LIVNAG | (b) -> 261 points |
| OGUGON | (a) redo with chlorides (~4-9 node-hours), or (b) as a labelled N4O2 solution model -> 238 points |
| KERJOI | (c) drop, or (b) only if an explicit N-bound linkage isomer is wanted (285 points, 11 branches mislabelled) |
| KUBVEJ | (c) drop, or (b) with a caveat (153 points) |
| EPOFUL | (b), as for KECGEI and LIVNAG (O chelate closes, 4 -> 6) |
| FECYIZ | (c) drop, or (b) only if an explicit N-bound linkage isomer is wanted, as for KERJOI |

**Two more complexes joined this list on 2026-11-01, as predicted on 10-31.** EPOFUL and FECYIZ finished that
day, and every branch start failed in the same way: `new_contact` for EPOFUL (30 of 30), `shell` for FECYIZ
(30 of 30). Their stage-2 shells had been checked on 2026-10-31 at step 0 of finished branches. **EPOFUL** has
non-donors O62/O63 at 2.404/2.399 A at stage 2, against 2.703 A in the crystal. This is the KECGEI/LIVNAG
pattern: an O closes a chelate, 4 -> 6. **FECYIZ** has non-donor N10 at 1.98 A, while its donor S1 sits at
3.702 A. This is the KERJOI pattern, an S -> N linkage switch at stage 2; its `bond_Zn-S1` branches stretch a
non-bond. Both are recorded `not_exported`. The same options apply. See section (f).

### (b) Lower minimum than the stage-2 geometry

Every published complex with at least one branch whose first failing point lies more than 2 kJ/mol below the branch start. *energy_drop* = flagged as such (the results README list); *structural* = the drop came with a `shell`, `new_contact` or `jump` failure, so it is not in the README list. E_rel is relative to the branch start, which reproduces the stage-2 minimum (within 0.5 kJ/mol and 0.05 A, else `ref_mismatch`).

| Complex | Branches below start | Lowest E_rel (kJ/mol) | Where | Kind | Pass |
|---|---|---|---|---|---|
| TIFNOO | 8 | -44.024 | angle_S3-Zn-N33 neg step 7 (shell) | structural 8 | 241/302 |
| WEDVIK | 2 | -29.293 | bond_Zn-N6 pos step 7 (shell) | structural 2 | 275/302 |
| TEYSOG | 1 | -27.45 | angle_S1-Zn-S2 pos step 9 (energy_drop) | energy_drop 1 | 287/302 |
| FAZJAT | 5 | -24.658 | angle_S93-Zn-S94 neg step 3 (energy_drop) | energy_drop 5 | 50/302 |
| XAJQAB | 1 | -21.073 | angle_N22-Zn-N69 neg step 9 (energy_drop) | energy_drop 1 | 277/302 |
| GUYHEN | 9 | -18.665 | angle_S1-Zn-N11 neg step 4 (shell) | structural 9 | 204/302 |
| NAMSOJ | 13 | -16.76 | angle_N3-Zn-S4 pos step 1 (energy_drop) | energy_drop 11, structural 2 | 212/302 |
| HOZGAF | 15 | -16.099 | angle_N3-Zn-N5 neg step 1 (energy_drop) | energy_drop 15 | 137/302 |
| GEQCUE | 2 | -14.839 | bond_Zn-S44 pos step 3 (energy_drop) | energy_drop 2 | 239/302 |
| LAPYAD | 7 | -12.177 | bond_Zn-N39 pos step 4 (energy_drop) | energy_drop 7 | 214/302 |
| ICUCIT | 1 | -10.556 | angle_N2-Zn-N3 pos step 8 (energy_drop) | energy_drop 1 | 272/302 |
| KAKYAW | 1 | -10.288 | angle_N29-Zn-N50 pos step 3 (energy_drop) | energy_drop 1 | 231/302 |
| FEKQUH | 2 | -9.851 | angle_N2-Zn-S3 neg step 5 (energy_drop) | energy_drop 2 | 283/302 |
| UCOLON | 1 | -8.969 | angle_S3-Zn-S4 pos step 10 (energy_drop) | energy_drop 1 | 287/302 |
| TELRIN | 10 | -8.018 | angle_S2-Zn-N6 pos step 1 (energy_drop) | energy_drop 10 | 200/302 |
| ZAZQUM | 2 | -7.364 | angle_S1-Zn-S3 neg step 7 (energy_drop) | energy_drop 2 | 222/302 |
| QADDEF | 1 | -6.959 | angle_N5-Zn-N7 pos step 9 (energy_drop) | energy_drop 1 | 281/302 |
| XIXTEG | 11 | -6.57 | tilt_Zn-S4-C54-N10 pos step 10 (energy_drop) | energy_drop 11 | 195/302 |
| DIFBOK | 7 | -6.339 | angle_S3-Zn-N5 neg step 7 (shell) | structural 7 | 264/302 |
| HULBIZ | 10 | -6.333 | angle_S1-Zn-N7 neg step 6 (shell) | structural 10 | 243/302 |
| RIBMEV | 8 | -6.282 | twist_S1-S2-N5-N6 neg step 4 (shell) | structural 8 | 205/302 |
| MUJJUW | 7 | -6.28 | angle_S1-Zn-N9 neg step 8 (shell) | structural 7 | 249/302 |
| RIBMIZ | 10 | -6.116 | angle_S1-Zn-N5 neg step 5 (shell) | structural 10 | 235/302 |
| WUCGIN | 9 | -5.726 | angle_S2-Zn-N10 neg step 7 (shell) | structural 9 | 249/302 |
| WUJZOS | 9 | -5.665 | angle_N1-Zn-N9 pos step 2 (energy_drop) | energy_drop 9 | 154/302 |
| GAKKUY | 1 | -4.906 | angle_S2-Zn-S3 neg step 9 (energy_drop) | energy_drop 1 | 234/302 |
| GIXTAL | 1 | -4.886 | angle_N6-Zn-N7 pos step 6 (energy_drop) | energy_drop 1 | 153/302 |
| UFUROC | 14 | -3.621 | angle_S1-Zn-S2 neg step 1 (energy_drop) | energy_drop 14 | 181/302 |
| FEKRAO | 5 | -3.29 | tilt_Zn-S2-C32-C38 neg step 9 (energy_drop) | energy_drop 5 | 228/302 |
| FEKQOB | 1 | -2.832 | angle_N1-Zn-S3 neg step 9 (energy_drop) | energy_drop 1 | 296/302 |
| ZUKRII | 1 | -2.724 | angle_N21-Zn-N58 neg step 8 (energy_drop) | energy_drop 1 | 291/302 |
| ZNDITZ11 | 8 | -2.658 | tilt_Zn-S2-C34-N8 neg step 6 (energy_drop) | energy_drop 8 | 178/302 |
| SIHXIR | 10 | -2.643 | bond_Zn-N5 pos step 1 (energy_drop) | energy_drop 10 | 151/302 |
| TELROT | 2 | -2.534 | tilt_Zn-S2-C29-C37 pos step 4 (energy_drop) | energy_drop 2 | 206/302 |
| ICAVAK | 1 | -2.533 | angle_S1-Zn-N2 pos step 8 (energy_drop) | energy_drop 1 | 291/302 |
| OJELOE | 2 | -2.511 | twist_S3-S4-N100-S5 neg step 7 (energy_drop) | energy_drop 2 | 229/302 |
| TARNIJ | 1 | -2.476 | angle_S1-Zn-S2 neg step 8 (energy_drop) | energy_drop 1 | 281/302 |
| WIGBIX | 1 | -2.309 | angle_S20-Zn-N39 pos step 7 (energy_drop) | energy_drop 1 | 216/302 |
| TIFNUU | 3 | -2.298 | angle_S6-Zn-S7 pos step 5 (energy_drop) | energy_drop 3 | 260/302 |

All branches below start (coordinate, branch, step of the first failure, E_rel kJ/mol, status):

- **DIFBOK**: angle_S1-Zn-N6 neg 8 -6.174 (shell); angle_S3-Zn-N5 neg 7 -6.339 (shell); angle_S3-Zn-N6 neg 9 -6.306 (shell); bond_Zn-N5 pos 6 -5.467 (shell); bond_Zn-N6 pos 7 -4.65 (shell); bond_Zn-S1 pos 5 -4.816 (shell); bond_Zn-S3 pos 7 -5.503 (shell)
- **FAZJAT**: angle_S92-Zn-S93 neg 3 -20.796 (energy_drop); angle_S92-Zn-S95 neg 1 -6.423 (energy_drop); angle_S93-Zn-S94 neg 3 -24.658 (energy_drop); bond_Zn-S93 pos 1 -7.64 (energy_drop); bond_Zn-S94 neg 1 -7.73 (energy_drop)
- **FEKQOB**: angle_N1-Zn-S3 neg 9 -2.832 (energy_drop)
- **FEKQUH**: angle_N1-Zn-S4 pos 7 -9.777 (energy_drop); angle_N2-Zn-S3 neg 5 -9.851 (energy_drop)
- **FEKRAO**: angle_S1-Zn-N3 neg 2 -2.508 (energy_drop); angle_S1-Zn-N4 neg 3 -2.483 (energy_drop); angle_S2-Zn-N3 neg 2 -2.345 (energy_drop); tilt_Zn-S2-C32-C38 neg 9 -3.29 (energy_drop); twist_S1-S2-N3-N4 neg 3 -2.489 (energy_drop)
- **GAKKUY**: angle_S2-Zn-S3 neg 9 -4.906 (energy_drop)
- **GEQCUE**: bond_Zn-S44 pos 3 -14.839 (energy_drop); bond_Zn-S45 pos 5 -11.695 (energy_drop)
- **GIXTAL**: angle_N6-Zn-N7 pos 6 -4.886 (energy_drop)
- **GUYHEN**: angle_N11-Zn-N12 neg 3 -16.45 (shell); angle_S1-Zn-N11 neg 4 -18.665 (shell); angle_S1-Zn-N12 neg 4 -17.688 (shell); angle_S1-Zn-S2 pos 8 -11.041 (shell); angle_S2-Zn-N11 neg 4 -17.692 (shell); angle_S2-Zn-N12 neg 4 -18.662 (shell); bond_Zn-N11 pos 2 -18.614 (shell); bond_Zn-N12 pos 2 -18.615 (shell); twist_S1-S2-N11-N12 pos 5 -17.374 (shell)
- **HOZGAF**: angle_N3-Zn-N5 neg 1 -16.099 (energy_drop); angle_N3-Zn-N6 neg 1 -16.094 (energy_drop); angle_N3-Zn-N6 pos 8 -2.22 (energy_drop); angle_N5-Zn-N6 pos 1 -15.968 (energy_drop); angle_S1-Zn-N3 neg 1 -16.095 (energy_drop); angle_S1-Zn-N3 pos 3 -15.406 (energy_drop); angle_S1-Zn-N5 neg 1 -16.028 (energy_drop); angle_S1-Zn-N6 pos 1 -16.09 (energy_drop); bond_Zn-N3 pos 1 -16.087 (energy_drop); bond_Zn-N5 pos 1 -15.996 (energy_drop); bond_Zn-N6 neg 1 -15.931 (energy_drop); bond_Zn-S1 pos 2 -15.858 (energy_drop); tilt_Zn-N3-C10-C21 neg 6 -16.006 (energy_drop); tilt_Zn-N6-C14-C15 pos 7 -15.659 (energy_drop); twist_S1-N3-N5-N6 neg 1 -16.089 (energy_drop)
- **HULBIZ**: angle_N7-Zn-N8 neg 3 -5.207 (shell); angle_S1-Zn-N7 neg 6 -6.333 (shell); angle_S1-Zn-N8 neg 6 -6.005 (shell); angle_S2-Zn-N7 neg 6 -6.007 (shell); angle_S2-Zn-N8 neg 6 -6.33 (shell); bond_Zn-N7 pos 6 -5.394 (shell); bond_Zn-N8 pos 6 -5.395 (shell); bond_Zn-S1 pos 4 -4.197 (shell); bond_Zn-S2 pos 4 -4.2 (shell); twist_S1-S2-N7-N8 pos 7 -6.009 (shell)
- **ICAVAK**: angle_S1-Zn-N2 pos 8 -2.533 (energy_drop)
- **ICUCIT**: angle_N2-Zn-N3 pos 8 -10.556 (energy_drop)
- **KAKYAW**: angle_N29-Zn-N50 pos 3 -10.288 (energy_drop)
- **LAPYAD**: angle_N39-Zn-S66 pos 3 -11.029 (energy_drop); angle_N40-Zn-S65 pos 3 -11.048 (energy_drop); bond_Zn-N39 pos 4 -12.177 (energy_drop); bond_Zn-N40 pos 4 -12.174 (energy_drop); tilt_Zn-N39-C35-C33 pos 5 -9.657 (energy_drop); tilt_Zn-N40-C36-C34 pos 5 -9.668 (energy_drop); twist_N39-S65-N40-S66 pos 3 -11.849 (energy_drop)
- **MUJJUW**: angle_S1-Zn-N10 neg 6 -6.222 (shell); angle_S1-Zn-N9 neg 8 -6.28 (shell); angle_S3-Zn-N10 neg 7 -6.155 (shell); angle_S3-Zn-N9 neg 6 -6.272 (shell); bond_Zn-N9 pos 5 -5.771 (shell); bond_Zn-S1 pos 5 -4.745 (shell); bond_Zn-S3 pos 5 -4.789 (shell)
- **NAMSOJ**: angle_N1-Zn-N2 pos 3 -15.459 (energy_drop); angle_N1-Zn-N3 neg 2 -16.738 (energy_drop); angle_N1-Zn-S4 neg 1 -16.718 (energy_drop); angle_N2-Zn-N3 neg 7 -3.647 (new_contact); angle_N2-Zn-S4 neg 3 -15.969 (energy_drop); angle_N2-Zn-S4 pos 4 -16.305 (energy_drop); angle_N3-Zn-S4 pos 1 -16.76 (energy_drop); bond_Zn-N1 neg 2 -16.558 (energy_drop); bond_Zn-N2 pos 6 -12.737 (new_contact); bond_Zn-S4 neg 3 -15.584 (energy_drop); tilt_Zn-N1-C19-C24 pos 3 -4.152 (energy_drop); tilt_Zn-S4-C5-O7 neg 8 -15.792 (energy_drop); twist_N1-N2-N3-S4 neg 1 -16.653 (energy_drop)
- **OJELOE**: angle_S4-Zn-N100 pos 4 -2.003 (energy_drop); twist_S3-S4-N100-S5 neg 7 -2.511 (energy_drop)
- **QADDEF**: angle_N5-Zn-N7 pos 9 -6.959 (energy_drop)
- **RIBMEV**: angle_N5-Zn-N6 neg 4 -4.823 (shell); angle_S1-Zn-N5 neg 5 -6.271 (shell); angle_S2-Zn-N5 neg 4 -6.172 (shell); angle_S2-Zn-N6 neg 5 -6.271 (shell); bond_Zn-N6 pos 5 -6.218 (shell); bond_Zn-S1 pos 5 -4.485 (shell); bond_Zn-S2 pos 5 -4.486 (shell); twist_S1-S2-N5-N6 neg 4 -6.282 (shell)
- **RIBMIZ**: angle_N5-Zn-N6 neg 4 -4.288 (shell); angle_S1-Zn-N5 neg 5 -6.116 (shell); angle_S1-Zn-N6 neg 4 -6.025 (shell); angle_S2-Zn-N5 neg 4 -6.025 (shell); angle_S2-Zn-N6 neg 5 -6.115 (shell); bond_Zn-N5 pos 6 -5.548 (shell); bond_Zn-N6 pos 6 -5.556 (shell); bond_Zn-S1 pos 4 -3.525 (shell); bond_Zn-S2 pos 4 -3.525 (shell); twist_S1-S2-N5-N6 neg 4 -6.081 (shell)
- **SIHXIR**: angle_N5-Zn-S11 neg 1 -2.433 (energy_drop); angle_N5-Zn-S12 pos 3 -2.212 (energy_drop); angle_N8-Zn-S11 pos 1 -2.439 (energy_drop); angle_N8-Zn-S12 neg 1 -2.467 (energy_drop); bond_Zn-N5 pos 1 -2.643 (energy_drop); bond_Zn-N8 pos 1 -2.642 (energy_drop); bond_Zn-S11 neg 1 -2.566 (energy_drop); tilt_Zn-N5-C13-H14 neg 2 -2.431 (energy_drop); tilt_Zn-S11-C25-N6 pos 2 -2.633 (energy_drop); tilt_Zn-S12-C56-N9 neg 2 -2.438 (energy_drop)
- **TARNIJ**: angle_S1-Zn-S2 neg 8 -2.476 (energy_drop)
- **TELRIN**: angle_N5-Zn-N6 neg 2 -6.456 (energy_drop); angle_S1-Zn-N5 neg 1 -6.128 (energy_drop); angle_S1-Zn-N6 neg 4 -7.006 (energy_drop); angle_S2-Zn-N5 pos 7 -7.607 (energy_drop); angle_S2-Zn-N6 neg 8 -6.445 (energy_drop); angle_S2-Zn-N6 pos 1 -8.018 (energy_drop); tilt_Zn-N5-C51-H52 neg 3 -7.861 (energy_drop); tilt_Zn-N6-C60-C59 pos 9 -6.646 (energy_drop); tilt_Zn-S1-C7-C8 pos 10 -5.637 (energy_drop); twist_S1-S2-N5-N6 pos 4 -8.01 (energy_drop)
- **TELROT**: tilt_Zn-S2-C29-C37 pos 4 -2.534 (energy_drop); twist_S1-S2-N5-N6 pos 3 -2.01 (energy_drop)
- **TEYSOG**: angle_S1-Zn-S2 pos 9 -27.45 (energy_drop)
- **TIFNOO**: angle_N33-Zn-N34 neg 4 -31.876 (shell); angle_S3-Zn-N33 neg 7 -44.024 (shell); angle_S3-Zn-N34 neg 7 -37.596 (shell); angle_S3-Zn-S4 pos 9 -15.896 (shell); angle_S4-Zn-N33 neg 7 -34.454 (shell); bond_Zn-S3 pos 4 -32.173 (shell); bond_Zn-S4 pos 4 -32.174 (shell); twist_S3-S4-N33-N34 pos 8 -32.322 (shell)
- **TIFNUU**: angle_S5-Zn-S8 pos 5 -2.29 (energy_drop); angle_S6-Zn-S7 pos 5 -2.298 (energy_drop); twist_S5-S6-S7-S8 pos 7 -2.136 (energy_drop)
- **UCOLON**: angle_S3-Zn-S4 pos 10 -8.969 (energy_drop)
- **UFUROC**: angle_S1-Zn-S2 neg 1 -3.621 (energy_drop); angle_S1-Zn-S3 pos 1 -3.152 (energy_drop); angle_S1-Zn-S4 neg 1 -2.971 (energy_drop); angle_S2-Zn-S3 pos 3 -3.3 (energy_drop); angle_S2-Zn-S4 neg 1 -3.606 (energy_drop); angle_S3-Zn-S4 pos 2 -3.615 (energy_drop); bond_Zn-S1 neg 3 -2.655 (energy_drop); bond_Zn-S2 pos 2 -3.299 (energy_drop); bond_Zn-S3 neg 1 -3.613 (energy_drop); bond_Zn-S4 pos 3 -3.064 (energy_drop); tilt_Zn-S2-C12-O11 neg 3 -3.564 (energy_drop); tilt_Zn-S3-C18-C19 neg 2 -3.22 (energy_drop); tilt_Zn-S4-C24-O23 neg 2 -3.615 (energy_drop); twist_S1-S2-S3-S4 neg 1 -3.334 (energy_drop)
- **WEDVIK**: angle_N5-Zn-N6 neg 4 -20.701 (shell); bond_Zn-N6 pos 7 -29.293 (shell)
- **WIGBIX**: angle_S20-Zn-N39 pos 7 -2.309 (energy_drop)
- **WUCGIN**: angle_N9-Zn-N10 neg 4 -2.705 (shell); angle_S1-Zn-N10 neg 7 -5.717 (shell); angle_S2-Zn-N10 neg 7 -5.726 (shell); angle_S2-Zn-N9 neg 7 -5.716 (shell); bond_Zn-N10 pos 6 -4.69 (shell); bond_Zn-N9 pos 6 -4.693 (shell); bond_Zn-S1 pos 4 -3.547 (shell); bond_Zn-S2 pos 4 -3.546 (shell); twist_S1-S2-N9-N10 pos 7 -5.669 (shell)
- **WUJZOS**: angle_N1-Zn-N6 neg 5 -2.591 (energy_drop); angle_N1-Zn-N9 pos 2 -5.665 (energy_drop); angle_N4-Zn-N6 neg 2 -5.635 (energy_drop); bond_Zn-N4 pos 5 -4.526 (energy_drop); tilt_Zn-N1-C11-C43 neg 4 -5.43 (energy_drop); tilt_Zn-N4-C43-C11 neg 5 -4.602 (energy_drop); tilt_Zn-N6-C69-C101 pos 9 -4.898 (energy_drop); tilt_Zn-N9-C75-C74 neg 3 -5.495 (energy_drop); twist_N1-N4-N6-N9 neg 3 -5.18 (energy_drop)
- **XAJQAB**: angle_N22-Zn-N69 neg 9 -21.073 (energy_drop)
- **XIXTEG**: angle_N5-Zn-N9 neg 2 -6.213 (energy_drop); angle_S2-Zn-N5 neg 3 -4.432 (energy_drop); angle_S2-Zn-S4 pos 3 -6.376 (energy_drop); angle_S4-Zn-N5 pos 6 -3.541 (energy_drop); angle_S4-Zn-N9 neg 3 -4.737 (energy_drop); bond_Zn-N5 pos 4 -6.315 (energy_drop); bond_Zn-N9 pos 4 -6.38 (energy_drop); tilt_Zn-N5-C26-C27 pos 4 -4.229 (energy_drop); tilt_Zn-N9-C49-C50 pos 4 -4.473 (energy_drop); tilt_Zn-S4-C54-N10 pos 10 -6.57 (energy_drop); twist_S2-N5-S4-N9 neg 8 -3.992 (energy_drop)
- **ZAZQUM**: angle_S1-Zn-S3 neg 7 -7.364 (energy_drop); angle_S3-Zn-N4 pos 4 -6.257 (energy_drop)
- **ZNDITZ11**: angle_S1-Zn-N3 neg 2 -2.201 (energy_drop); angle_S1-Zn-N7 pos 2 -2.522 (energy_drop); angle_S1-Zn-S2 pos 4 -2.225 (energy_drop); angle_S2-Zn-N3 pos 1 -2.373 (energy_drop); bond_Zn-N3 pos 4 -2.047 (energy_drop); tilt_Zn-S1-C11-N4 pos 7 -2.373 (energy_drop); tilt_Zn-S2-C34-N8 neg 6 -2.658 (energy_drop); tilt_Zn-S2-C34-N8 pos 5 -2.413 (energy_drop)
- **ZUKRII**: angle_N21-Zn-N58 neg 8 -2.724 (energy_drop)

**What the structures show.** This is a read-only geometry check of the lowest first-failing point of each
complex on 2026-10-31: the Zn-donor distances at step 0 and at the failing step, the nearest non-donors, and
the heavy-atom pair that changed most. The same check was repeated on 2026-11-02 for the complexes published
after 10-31: WEDVIK, TEYSOG, GEQCUE, LAPYAD, TELRIN, ZAZQUM, ZUKRII, SIHXIR, TELROT and TIFNUU. Their step-0
geometries match stage 2 within 0.001 A. Three kinds stand out.

1. **The first shell changes: a different species lies lower** (*inference* for the chemical labels).
   - **TIFNOO**: the deepest at -32 to -44 kJ/mol. At Zn-S3 or Zn-S4 +0.08 A, the other S leaves (3.51 A) and the
     ring N9/N10, at 2.76 A at stage 2, bind at 2.03/2.23 A. This is an S -> N linkage switch like KERJOI and
     FECYIZ, here reached during the scan. The published points describe the S-bound local minimum.
   - **WEDVIK**: -29.3 kJ/mol. At Zn-N6 +0.14 A, both S leave (3.40/3.44 A), and N7/N8, at 2.97/2.99 A at
     stage 2, bind at 2.02/2.03 A. Its second low branch (angle_N5-Zn-N6 neg, -20.7) shows the same switch. This
     is an S -> N linkage switch like TIFNOO and KERJOI. The published points describe the S-bound local minimum.
   - **GUYHEN**: -18.6 kJ/mol (Run log 10-21). N9/N10, at 2.85 A at stage 2, come in to 2.13 A, while S1/S2
     lengthen to 2.64 A: 4 -> 6.
   - **DIFBOK, HULBIZ, MUJJUW, RIBMEV, RIBMIZ, WUCGIN**: -4 to -6 kJ/mol. The second S atom of each of two
     bidentate S-ligands comes in to 2.54-2.64 A (the S...S distance between them shortens from about 5.1 to 3.7
     A), and the original Zn-S bonds lengthen to about 2.56-2.62 A. This is the GECLUZ pattern (4 -> 6 by closing
     anisobidentate S chelates), here only slightly lower in energy, so the four-coordinate stage-2 minimum is
     nearly degenerate with a six-coordinate one.
2. **Peripheral conformers: the first shell is almost unchanged.** In HOZGAF (-16 kJ/mol), NAMSOJ (-16.8),
   XAJQAB (-21.1), ICUCIT (-10.6), KAKYAW (-10.3), QADDEF (-7.0), XIXTEG (-6.6), WUJZOS (-5.7), GAKKUY and GIXTAL
   (-4.9), the Zn-donor
   distances change by at most about 0.05 A at the lowest point. The heavy-atom pairs that change most (by
   2-8 A) lie in the ligand periphery: aryl or alkyl groups rotating. NAMSOJ also has two `new_contact` failures at
   -12.7 kJ/mol, where carbonyl O7 reaches 2.60 A. The same holds for TEYSOG (-27.5), GEQCUE (-14.8), LAPYAD
   (-12.2), TELRIN (-8.0) and ZAZQUM (-7.4): the unscanned Zn-donor distances change by at most 0.036 A, and the
   pairs that change most (by 3-11 A) lie 5-9 A from Zn, such as a methyl-bearing thioether arm in TEYSOG and a
   chloroaryl arm in GEQCUE. In HOZGAF, NAMSOJ and TELRIN most branches drop
   already at step 1-3 (by about 16 kJ/mol in HOZGAF and NAMSOJ, 6-8 in 10 TELRIN branches), so the stage-2 geometry is not the lowest conformer and possibly not
   a true minimum. The stage-2 frequencies on S3DF would settle this. For the Zn K-edge the first shell is what
   matters, so these published points are probably still representative (*inference*). Their energies are
   relative to a conformer that is not the lowest.
3. **Small drops of 2-3 kJ/mol** (UFUROC, ZNDITZ11, FEKRAO, TARNIJ, ICAVAK, OJELOE, WIGBIX, FEKQOB, ZUKRII,
   SIHXIR, TELROT, TIFNUU): flat surfaces. In TIFNUU, N18/N19 come in from 3.20/3.25 to 3.01 A, still outside
   the shell.
   *Inference*: no action needed beyond noting them.

**Recommended action.** For kind 1, decide per complex: either keep the published points as a labelled local
minimum (0 compute), or re-optimise stage 2 from the lowest scan geometry and re-scan (about 3-9 node-hours per
complex). TIFNOO, WEDVIK and GUYHEN deserve this most; for TIFNOO and WEDVIK the lower form is N-bound, not the
CSD compound, so they belong with the KERJOI question (Decision 3); the six S-chelate cases are only 4-6 kJ/mol apart. For kind 2,
check the stage-2 frequencies on S3DF for HOZGAF, NAMSOJ, TELRIN, XAJQAB, ICUCIT, KAKYAW, TEYSOG, GEQCUE, LAPYAD
and ZAZQUM (0 compute); TELRIN first, since its drops start at step 1. Re-scan only
if an imaginary mode or a strongly different conformer matters for the spectra.

### (c) Pass rate below 75%

*Median first-failure step* and *median E_rel at first failure* help tell soft modes (early, near 0 kJ/mol) from lower minima (negative) and from the ends of stiff scans (late, positive).

| Complex | Atoms | Pass | Pass % | First failures | Median first-failure step | Median E_rel at first failure | Site |
|---|---|---|---|---|---|---|---|
| FAZJAT | 97 | 50/302 | 16.6 | jump 24, energy_drop 5 | 1 | -0.5 | Aurora + NERSC m2464 (3/30 br.) |
| VOJHIO | 53 | 97/302 | 32.1 | jump 24 | 1 | 0.0 | Aurora |
| HOZGAF | 96 | 137/302 | 45.4 | energy_drop 15, jump 6 | 2 | -15.9 | Aurora |
| SIHXIR | 75 | 151/302 | 50.0 | energy_drop 11, jump 7, energy_cap 1 | 2 | -2.2 | Aurora |
| GIXTAL | 57 | 153/302 | 50.7 | jump 19, energy_drop 3 | 3 | 0.2 | Aurora |
| WUJZOS | 127 | 154/302 | 51.0 | energy_drop 14, jump 9 | 4 | 0.2 | Aurora + NERSC m5268 (4/30 br.) |
| RAYBIC | 124 | 156/302 | 51.7 | jump 20, ref_mismatch 1 | 3 | 0.3 | Aurora + NERSC m5268 (28/30 br.) |
| TELRUZ | 77 | 161/302 | 53.3 | jump 18, shell 1 | 2 | 0.2 | Aurora + NERSC m2464 (26/30 br.) |
| NESCAR | 63 | 168/302 | 55.6 | jump 20, energy_cap 2 | 4.5 | 0.7 | Aurora |
| PTOLZN01 | 53 | 171/302 | 56.6 | jump 17 | 3 | -0.1 | Aurora |
| OJEKIX | 95 | 174/302 | 57.6 | jump 16 | 2 | 0.1 | Aurora |
| GOYNIT | 79 | 175/302 | 57.9 | jump 14, shell 2 | 1 | 0.0 | Aurora |
| NESBUK | 61 | 176/302 | 58.3 | jump 21, energy_cap 2 | 5 | 0.8 | Aurora |
| ZNDITZ11 | 59 | 178/302 | 58.9 | jump 10, energy_drop 10 | 4 | -1.6 | Aurora |
| XIYHET | 73 | 179/302 | 59.3 | jump 18 | 3 | 0.1 | Aurora |
| UFUROC | 29 | 181/302 | 59.9 | energy_drop 16 | 2 | -3.3 | Aurora |
| BUNNII | 137 | 182/302 | 60.3 | jump 20 | 2.5 | 0.1 | Aurora + NERSC m5268 (30/30 br.) |
| WAJJIB | 93 | 182/302 | 60.3 | jump 16 | 2.5 | -0.4 | Aurora |
| OLIPEG | 57 | 189/302 | 62.6 | jump 21 | 4 | 0.7 | Aurora |
| EBEXIS | 66 | 180/280 | 64.3 | jump 16 | 3.5 | 0.2 | Aurora |
| XIXTEG | 59 | 195/302 | 64.6 | energy_drop 11, jump 8 | 4 | -4.0 | Aurora |
| ICATUC | 85 | 196/302 | 64.9 | new_contact 11, jump 3 | 1 | 0.2 | Aurora |
| BOJMIX | 95 | 198/302 | 65.6 | jump 18, shell 1 | 5 | 0.5 | Aurora |
| TANRAE | 63 | 200/302 | 66.2 | jump 21 | 6 | 1.4 | Aurora |
| TELRIN | 69 | 200/302 | 66.2 | energy_drop 10, jump 5, energy_cap 1 | 4 | -6.3 | Aurora |
| TELSAG | 73 | 201/302 | 66.6 | jump 20 | 6 | 0.8 | Aurora |
| GUYHEN | 49 | 204/302 | 67.5 | shell 9, new_contact 4, jump 2, energy_cap 1 | 4 | -13.7 | Aurora |
| KAKVIB01 | 49 | 204/302 | 67.5 | jump 13, shell 1, energy_cap 1 | 4 | 0.9 | Aurora |
| UCOLIH | 69 | 204/302 | 67.5 | jump 13 | 4 | 0.8 | Aurora |
| XOGYUQ | 49 | 204/302 | 67.5 | jump 16, energy_drop 1 | 5 | 0.4 | Aurora |
| RIBMEV | 59 | 205/302 | 67.9 | shell 9, ref_mismatch 4, jump 1 | 4 | -4.5 | Aurora |
| TELROT | 71 | 206/302 | 68.2 | jump 11, energy_drop 5, energy_cap 1 | 4 | 0.2 | Aurora |
| LIYDEE | 79 | 209/302 | 69.2 | jump 13, energy_drop 3 | 6 | -0.8 | Aurora |
| NAMSOJ | 104 | 212/302 | 70.2 | energy_drop 11, new_contact 2, jump 1 | 3 | -15.9 | Aurora + NERSC m5268 (30/30 br.) |
| VEKDUL | 65 | 212/302 | 70.2 | jump 10, energy_drop 1 | 2 | -1.5 | Aurora |
| GIXSUE | 65 | 214/302 | 70.9 | jump 13, shell 2, new_contact 2 | 6 | 0.3 | Aurora + NERSC m2464 (3/30 br.) |
| LAPYAD | 71 | 214/302 | 70.9 | energy_drop 9, jump 6 | 5 | -0.6 | Aurora |
| WIGBIX | 121 | 216/302 | 71.5 | jump 13, energy_drop 1 | 4 | 0.4 | Aurora + NERSC m5268 (30/30 br.) |
| TEYSIA | 67 | 217/302 | 71.9 | jump 15, shell 1 | 4 | 1.0 | Aurora |
| ICUCAL | 46 | 218/302 | 72.2 | jump 13, new_contact 1 | 4.5 | 1.1 | Aurora |
| KAKVAT | 45 | 221/302 | 73.2 | jump 15, shell 1 | 6.5 | 1.5 | Aurora |
| XAYGEL | 77 | 222/302 | 73.5 | jump 14 | 5 | 1.2 | Aurora |
| ZAZQUM | 49 | 222/302 | 73.5 | jump 11, energy_drop 2 | 4 | 0.7 | Aurora |
| XIGZUI | 69 | 223/302 | 73.8 | jump 12, shell 2 | 5.5 | 0.7 | Aurora |
| EDUPEZ | 47 | 225/302 | 74.5 | jump 15, shell 2 | 7 | 1.3 | Aurora |
| TBZZNP01 | 51 | 226/302 | 74.8 | jump 14 | 5 | 0.2 | Aurora |

**What the low pass rates mean.** Most low pass rates come from `jump`, and most jumps are in the ligand
periphery. A read-only check on 2026-10-31 looked at all 923 published `jump` first failures, comparing the
failing step with the step before:

- The atom pair whose distance changed most has its atom nearest to Zn at a median of **5.2 A** from Zn. That
  nearest atom is 4 A or more from Zn in 85% of cases.
- If `jump` counted only heavy atoms within 3.5 A of Zn (Zn included), **659 of the 923** jumps (71%) would
  not be a jump. Within 5 A, 331 of 923 would not be.
- The median E_rel at the jump is +1.3 kJ/mol, and 555 of 923 lie within +-2 kJ/mol of the branch start. None
  is below -2 kJ/mol.

These are soft, nearly free conformational changes (ring rotations, alkyl swings) far from Zn (*inference*).
Examples: VOJHIO (step 1 of most branches, |dE| < 0.4 kJ/mol, atoms 5.6-8.4 A from Zn, Run log 10-21), RAYBIC,
NESCAR, OJEKIX and BUNNII (moving atoms 5-7 A from Zn). Under the current rule each such event discards the
rest of the branch. The Zn first shell, which the XANES/EXAFS dataset is about, is often unchanged.

The other low-pass patterns:
- **`energy_drop`-dominated**: HOZGAF, WUJZOS, UFUROC, ZNDITZ11, XIXTEG, NAMSOJ. These are lower minima; see
  (b).
- **`shell`-dominated**: RIBMEV, RIBMIZ, WUCGIN, GUYHEN. These are soft first shells. Stretching one Zn-S bond
  moves another donor by more than 0.15 A, or the second S of a chelate comes in; see (b), kind 1.

**Recommended action (0 compute).** Re-validate the published points with `jump` limited to the Zn
neighbourhood: pairs where both atoms are within about 3.5-4 A of Zn, Zn-L distances included. The current
rule would be kept as an extra flag column, not a cut. Points after a peripheral jump would then pass if
every other rule holds. The upper bound on recovered points is the *jump* figure in "Points lost per
first-failure type" above; the true gain is smaller, because later points can fail other rules. This is
Riti's call. The 0.3 A jump rule was designed to keep each branch a single continuous path, and some users of
the data may want that.

### (d) Non-converged optimisation steps

`not_converged` first failures among the published points: **1** (WEDVIK angle_S3-Zn-N6 neg step 10).

No published point failed as `not_converged`, so none of the published points is a non-converged step. Steps
that did not converge in an earlier run are not visible in the stitched `scan.out`, because only converged
step blocks are kept. They appear only in `scan_try*.out` and the logs. One case is recorded in the Run log:
on 2026-10-28, OJELOE angle_S3-Zn-N100 neg, step 10, reached ORCA's 100 optimisation cycles (`%geom MaxIter
100`) on Perlmutter after about 23 h. It was continued from its last geometry, converged, and OJELOE was
published (`Run log` 10-28 08:20 and 09:36). Other steps of this kind on Aurora (MaxIter reached, then
continued) were not counted; that would need a pass over all logs and `scan_try*.out` (not done; Lustre
load). *Inference*: such a step converges to the same constrained minimum, but after more than 100 cycles on a
flat surface.

### (e) Branch starts that miss the stage-2 minimum (`ref_mismatch`)

| Complex | Coordinate | Branch | Points lost (incl. after_fail) |
|---|---|---|---|
| RAYBIC | twist_N1-N2-N3-S4 | pos | 11 |
| RIBMEV | bond_Zn-N5 | neg | 4 |
| RIBMEV | bond_Zn-N5 | pos | 11 |
| RIBMEV | tilt_Zn-N5-C37-C38 | neg | 11 |
| RIBMEV | tilt_Zn-N5-C37-C38 | pos | 11 |

**Measured on 2026-10-31 (read-only).** At step 0 of these branches, the largest heavy-atom distance
difference to the stage-2 geometry is **0.057 A**, against a limit of 0.05 A. The energy differs by only
-0.062 kJ/mol (RIBMEV) and -0.004 kJ/mol (RAYBIC) from stage 2. Step 0 re-optimises the stage-2 geometry with
the coordinate held at its own value. In these soft complexes the TightOpt settled 0.007 A past the tolerance.
*Inference*: these are the same minimum. Raising the step-0 geometry tolerance to 0.06 A, or accepting these
five branches by hand, recovers the points in the table at zero compute. Recommended.

### (f) Stage-2 Zn shell versus the donor list, all complexes

Computed from `stage2_b3lyp/<REF>/<REF>.xyz` and the donors in `scans/<REF>/coords.json` (= the `.meta` donors), with the `validate.py` limits; the crystal column uses `structures/dft_ready_xyz/` from this repository. Listed: any non-donor heavy atom within 2.8 A of Zn, any donor beyond 2.6 A, and any crystal non-donor contact between the curation cut-off for N/O (2.53 A) and the 2.6 A validation limit. Carbon contacts of 2.6-2.8 A are usually the ipso/ring carbons of the donor's own ring (*inference*); O, N, S, F, Cl and Br contacts are the ones to look at.

| Complex | Status | Findings (atom index 0-based, distance to Zn in A) |
|---|---|---|
| CUSGEE | published | donor S3 at 2.660 |
| EPOFUL | not_exported | non-donor O62 at 2.404 (< 2.6: fails every start); non-donor O63 at 2.399 (< 2.6: fails every start) |
| FECYIZ | not_exported | donor S1 at 3.702 (> 2.8: fails every start); non-donor N10 at 1.980 (< 2.6: fails every start) |
| FEYNUT | published | non-donor F2 at 2.689 |
| GECLUZ | not_exported | non-donor S1 at 2.526 (< 2.6: fails every start); non-donor S2 at 2.526 (< 2.6: fails every start) |
| GOYNIT | published | non-donor C7 at 2.790; non-donor C48 at 2.791 |
| GUCSAZ | published | non-donor C5 at 2.767; non-donor C7 at 2.765; non-donor C49 at 2.762; non-donor C51 at 2.762 |
| GUCSED | published | non-donor C5 at 2.791; non-donor C6 at 2.791 |
| HEFHUX | published | non-donor C19 at 2.787; non-donor C20 at 2.787 |
| ICATOW | published | non-donor O9 at 2.668 |
| ICATUC | published | non-donor O8 at 2.606; crystal: non-donor O8 at 2.552 |
| JADMEK | published | non-donor C5 at 2.789; non-donor C40 at 2.798 |
| KECGEI | not_exported | non-donor O11 at 2.393 (< 2.6: fails every start); non-donor O12 at 2.340 (< 2.6: fails every start) |
| KERJOI | not_exported | donor S2 at 3.520 (> 2.8: fails every start); non-donor N5 at 1.996 (< 2.6: fails every start); crystal: non-donor N5 at 2.530 |
| KUBVEJ | not_exported | non-donor N9 at 2.454 (< 2.6: fails every start) |
| LIVNAG | not_exported | non-donor O42 at 2.412 (< 2.6: fails every start); non-donor O43 at 2.405 (< 2.6: fails every start); crystal: non-donor O43 at 2.589 |
| NECTOG | published | non-donor C17 at 2.785; non-donor C67 at 2.794 |
| NOCNEY | published | non-donor N5 at 2.661; crystal: non-donor N5 at 2.590 |
| NONKUX | published | non-donor C9 at 2.791; non-donor C54 at 2.791 |
| NONLEI | published | non-donor C15 at 2.788; non-donor C16 at 2.788 |
| OGUGON | not_exported | non-donor O40 at 2.468 (< 2.6: fails every start); non-donor O43 at 2.402 (< 2.6: fails every start) |
| QASRIL | published | non-donor F51 at 2.789 |
| TIFNOO | published | non-donor N9 at 2.757; non-donor N10 at 2.758 |
| UDODOG | published | non-donor O2 at 2.637 |
| VEKDUL | published | non-donor O6 at 2.747 |
| WONYUW | published | non-donor N10 at 2.784 |
| WUJZOS | published | non-donor C11 at 2.784; non-donor C74 at 2.780 |
| YACTUV | published | non-donor F65 at 2.631 |

**Reading this list.** Exactly eight complexes have a non-donor below 2.6 A, or a donor beyond 2.8 A, at
stage 2. All eight are the not-exported complexes: GECLUZ, KECGEI, KERJOI, KUBVEJ, LIVNAG and OGUGON, plus
EPOFUL and FECYIZ, which finished on 11-01 and failed every branch start as predicted here (KERJOI and FECYIZ
show both). No other complex has this signature.

The complexes at risk have a non-donor O, N or F at 2.6-2.8 A at stage 2. Their branches fail early as
`new_contact` when a scan pulls that atom inside 2.6 A. Published examples: UDODOG O2 2.637 (9 `new_contact`),
NOCNEY N5 2.661 (7), ICATOW O9 2.668 (7), YACTUV F65 2.631 (8), FEYNUT F2 2.689 (2), and TIFNOO N9/N10 2.76,
whose N switch is the lower minimum in (b). **ICATUC** has O8 at 2.606 A at stage 2, 0.006 A above the limit;
it was published on 11-01 with 196 of 302 points passing and 11 `new_contact` failures. Crystal contacts between 2.53 and 2.6 A (non-donors only
because of the 2.53 A curation cut-off) are listed with the prefix `crystal:`.

**Recommended action.** Align the two cut-offs. The cleanest fix is to take the donor list from the stage-2
minimum with the validation limits, and to record "secondary" contacts of 2.6-2.8 A as their own class
(*suggestion*).

### (g) Every Run-log note addressed to Riti

Verbatim from `aurora/README.md` (Run log and setup notes), oldest first.

- setup note: With `RESUME_PARTIAL=1` (on by default in `go.sh`, off by default in `restart.py`), the interrupted step restarts from its last optimisation geometry at the same target instead of from the last converged step, so its finished optimisation cycles are not repeated. Riti: please check you are happy with this; `RESUME_PARTIAL=0 go.sh submit` restores the original behaviour.
- 2026-10-18 15:00: All 30 failing starts are OGUGON: a non-donor heavy atom is within 2.6 A of Zn at its stage-2 minimum (`new_contact`), so none of its points pass as defined. Riti: its donor list probably needs the extra contact.
- 2026-10-21 13:08: For Riti: VOJHIO passes only 97 of 302 points. In 24 of its 30 branches an early step (mostly the first) moves a heavy-atom distance by more than 0.3 A (`jump`) at almost no energy cost (|dE| < 0.4 kJ/mol), so the rest of each branch is `after_fail`. It happens in branches that never restarted too, so it is a soft conformational mode of the complex, not a restart artifact. GAKKUY has a lower minimum than stage 2 (angle_S2-Zn-S3 neg, -4.9 kJ/mol).
- 2026-10-21 19:11: For Riti: in 12 GUYHEN branches the point where the branch stops passing is a `shell`, `new_contact` or `jump` at about -17 to -19 kJ/mol. The complex finds a rearranged structure about 18 kJ/mol below the stage-2 geometry. `validate.py` flags these as structural changes, not `energy_drop`, so GUYHEN is not in the results README's lower-minimum list; its stage-2 minimum may need another look.
- 2026-10-23 16:44: For Riti: OGUGON finished and is not exported (all 30 branch starts fail validation, `new_contact`: a non-donor atom within 2.6 A of Zn at the stage-2 minimum, as flagged earlier); ICUCIT has a lower minimum than stage 2 (angle_N2-Zn-N3 pos step 8, -10.6 kJ/mol).
- 2026-10-23 20:44: For Riti: XAJQAB has a lower minimum than stage 2 (angle_N22-Zn-N69 neg step 9, -21.1 kJ/mol).
- 2026-10-24 08:37: For Riti: GECLUZ finished and is not exported (all 29 branch starts fail validation, `new_contact`, like OGUGON); lower minima than stage 2 in UFUROC (14 branches, up to -3.6 kJ/mol), ZNDITZ11 (8 branches, up to -2.7 kJ/mol) and TARNIJ (-2.5 kJ/mol); fewest passing points: OJEKIX 174, ZNDITZ11 178, UFUROC 181, ICUCAL 218 of 302.
- 2026-10-25 02:46: For Riti: KERJOI finished and is not exported (all 29 branch starts fail validation, `shell`); XIXTEG has a lower minimum than stage 2 (bond_Zn-N5/N9 pos step 4, -6.3/-6.4 kJ/mol); fewest passing points: OLIPEG 189, XIXTEG 195, TANRAE 200 of 302.
- 2026-10-25 22:05: For Riti: KECGEI and LIVNAG finished and are not exported (all 30 branch starts fail validation, `new_contact`, like GECLUZ and OGUGON); KAKYAW has a lower minimum than stage 2 (angle_N29-Zn-N50 pos step 3, -10.3 kJ/mol).
- 2026-10-26 22:19: For Riti: WUJZOS has a lower minimum than stage 2 in many branches (down to -5.7 kJ/mol, e.g. angle_N1-Zn-N9 pos step 2), so only 154 of its 302 points pass.
- 2026-10-27 06:15: For Riti: KUBVEJ finished and is not exported (all 30 branch starts fail validation, `new_contact`); FEKRAO has a lower minimum than stage 2 (several branches, about -2.5 kJ/mol).
- 2026-10-27 07:00: for Riti, why six finished complexes are not exported (every branch start fails validation): stage-2 B3LYP changed their Zn coordination relative to the crystal, so the donor list no longer matches the minimum the scans start from. KECGEI O11/O12 2.83/2.72 -> 2.39/2.34 A, LIVNAG O42/O43 2.73/2.59 -> 2.41/2.41, OGUGON O40/O43 3.13/2.98 -> 2.47/2.40 (4 -> 6 coordinate); GECLUZ dithiocarbamate S1/S2 3.01 -> 2.53 (4 -> 6; CSD lists it as unusual, CN 8); KUBVEJ pyrimidine N9 2.78 -> 2.45 (4 -> 5); KERJOI thiadiazole switches from S- to N-binding (S2 2.35 -> 3.52, N5 2.53 -> 2.00). The scans are valid calculations of these 5-/6-coordinate minima. Options: keep them out; redefine the donors to the B3LYP shell and re-validate (no compute; scans of the extra Zn-L bonds would need new branches); or constrain the weak contacts / redo stage 2 and the scans. KERJOI is a linkage isomer and needs a chemist's look.
- 2026-10-27 15:08: For Riti: NAMSOJ has a much lower minimum than stage 2 (many branches drop by 15-17 kJ/mol within the first 1-3 steps, e.g. angle_N1-Zn-N3 neg step 2 at -16.7 kJ/mol), so its stage-2 geometry is not its minimum; ICAVAK drops 2.5 kJ/mol in one branch.
- 2026-10-28 07:04: For Riti: GIXTAL has a lower minimum than stage 2 (angle_N6-Zn-N7 pos step 6, -4.9 kJ/mol).
- 2026-10-28 08:20: For Riti: a non-converged step fails validation and makes the rest of its branch after_fail, so such steps are worth reviewing before more compute goes into them.
- 2026-10-31 07:26: BUNNII, the slowest of the big complexes on NERSC (m5268), finished all 30 branches and is published, with 182 of 302 points passing validation (lower than most; for Riti to look at).
- 2026-11-01 13:17: EPOFUL finished and was not exported (`new_contact` on all 30 branch starts), as `CAMPAIGN_REPORT.md` predicted: it has the same stage-2 shell change as the six already listed (attention case a), so seven are now withheld for Riti's decision; FECYIZ is expected to follow. 8995873 handed its 118 unfinished branches back before its 6 h limit, and 9019151 picked them up at 11:05; 9024268 queued as the second 16-node farm.
- 2026-11-01 18:05: FECYIZ not exported (`shell` on all 30 branch starts), as `CAMPAIGN_REPORT.md` predicted, so eight are withheld for Riti's decision.
- 2026-11-02 11:30: All 10,175 branches of the 338 complexes terminated normally: **330 complexes published** on `aurora-results`, **8 not exported** for Riti's decision (GECLUZ, KECGEI, KERJOI, KUBVEJ, LIVNAG, OGUGON, EPOFUL, FECYIZ; see `CAMPAIGN_REPORT.md` (a)).

## Decisions for Riti

Each item gives our recommendation and its cost. ModCon node-hours are not a constraint for the user. The NERSC
projects are shared and are not to be used for more of this work unless DOE adds hours (the user made one
exception, for the last 22 slow branches on 11-01). "0 compute" means a
re-validation or inspection of results that already exist.

1. **Donor overrides for the eight shell-changed complexes**: GECLUZ, KECGEI, LIVNAG, OGUGON, KERJOI, KUBVEJ,
   EPOFUL and FECYIZ (both finished 11-01). *Recommended:* yes for GECLUZ, KECGEI and LIVNAG (about 800 points),
   and EPOFUL by the same argument. *Cost:* 0 compute; a small code change (a per-complex `donors` override read
   by `validate.py` and `publish.py`). The results layout stays as is.
2. **OGUGON**: redo stage 2 and the scans as neutral [Zn(L)2]Cl2 with the crystal chlorides, or publish the
   current N4O2 dication under option 1 with a label. *Recommended:* redo, for fidelity to the crystal.
   *Cost:* about 4-9 node-hours on Aurora, plus recovering the Cl positions from the CIF.
3. **KERJOI and KUBVEJ** (and FECYIZ, the same kind of S -> N switch as KERJOI): drop them, or keep them with
   option 1 as an explicit N-bound isomer or a floppy model. *Recommended:* drop, unless a linkage isomer is
   wanted. *Cost:* 0.
4. **Lower minima with a first-shell change** (TIFNOO -44, WEDVIK -29.3, GUYHEN -18.6; DIFBOK, HULBIZ, MUJJUW, RIBMEV, RIBMIZ,
   WUCGIN -4 to -6 kJ/mol): keep the published points as labelled local minima, or re-optimise stage 2 from the
   lowest scan geometry and re-scan. *Recommended:* re-scan GUYHEN; decide TIFNOO and WEDVIK (both S -> N, so the
   lower form is not the CSD compound) together with item 3. Keep the six S-chelate cases,
   noting the near-degenerate six-coordinate form. *Cost:* 0, or about 3-9 node-hours per re-scanned complex.
5. **Conformer drops** (HOZGAF, NAMSOJ, TELRIN, XAJQAB, ICUCIT, KAKYAW, TEYSOG, GEQCUE, LAPYAD, ZAZQUM; first shell
   almost unchanged): check the stage-2
   frequency outputs on S3DF for imaginary modes before deciding. *Recommended:* check first, and re-scan only
   if stage 2 was not a minimum. *Cost:* 0 for the check.
6. **`jump` rule limited to the Zn neighbourhood** (the median moving atom is 5.2 A from Zn; 71% of jumps vanish
   within 3.5 A): re-validate the published points. *Recommended:* yes, keeping the old flag as a column.
   *Cost:* 0 compute; a small change in `validate.py`.
7. **`ref_mismatch` tolerance** (5 branches of RIBMEV and RAYBIC at 0.057 A vs 0.05 A, |dE| <= 0.06 kJ/mol):
   accept them. *Recommended:* yes. *Cost:* 0.
8. **Curation/validation cut-off mismatch** (N/O donors 2.53 A on the crystal vs `new_contact` 2.6 A on stage 2):
   take donors from the stage-2 minimum in future, and treat 2.6-2.8 A O/N/F contacts as a flagged class. The
   check over all 338 complexes is already done, in section (f). *Recommended:* yes, for the next dataset.
   *Cost:* 0.
9. **`RESUME_PARTIAL`** (an interrupted step restarts from its latest optimisation geometry at the same target,
   instead of from the last converged step): this has been the default on both sites since 10-17, and Riti was
   asked to confirm it. *Recommended:* accept. *Inference:* a constrained optimisation that ends at the same
   target reaches the same local minimum; on flat surfaces the path could differ. *Cost:* 0 to accept. Undoing
   it would mean re-running every restarted branch.

## Where everything lives

| What | Where |
|---|---|
| Validated results (the deliverable) | branch `aurora-results`: `scan_results/<REF>.xyz`, `scan_results/validation_scan_full.csv`, `scan_results/coords/<REF>.json`, `README.md` (published, lower minima, not exported) |
| Code, Run log, this report | branch `aurora`: `scans/` (make_scans, validate, restart, export_points, zncore), `aurora/` (farm, queue, audit, publish, autopilot, `README.md` with the dated Run log, `STATUS.md`, `CAMPAIGN_REPORT.md`, `campaign_report.py`, `campaign_report_notes.md`), `nersc/iri/` (Perlmutter driver and job scripts), `HPC_LESSONS.md` (rules for the next campaign) |
| Riti's pipeline and crystals | branch `main` (`structures/dft_ready_xyz/`, `curation/build_dft.py`, `dft/scripts/make_stage2_inp.py`) |
| Run folder on Aurora (raw outputs) | `/lus/flare/projects/ModCon/dsokaras/zn_scans`: `scans/<REF>/<coord>_<branch>/` (`scan.inp`, `scan_orig.inp`, stitched `scan.out`, `scan_acc.txt`, `scan_try*.out`, `scan_cont.out`, `quarantine_8957252/` where present), `scans/<REF>/coords.json`, `scans/jobs_scan_full.txt` (all branches), `stage2_b3lyp/` (the bundle), `logs/` (one log per branch run), `autopilot/published.json` and `audit_reviewed.txt`, `remote_refs.txt`, `queue/` |
| Frozen copy from the isaac project | `/lus/flare/projects/isaac/dsokaras/zn_scans.isaac_frozen_20261024` (the old `zn_scans` path there is a symlink to the ModCon copy) |
| Perlmutter working copies | `/pscratch/sd/d/dsokaras/zn_nersc/run` (scratch: subject to NERSC purge). Finished branches' `scan.out` and `scan_acc.txt` are copied back to the Aurora run folder; the other Perlmutter outputs (`scan_try*.out`, job logs) stay on scratch. Driver state and log: `~/dev/iri/nersc_run/` on Aurora (`state.json`, `driver.log`) |
| Full stage-1/stage-2 outputs and frequencies | S3DF only (Riti) |

**Reproducing.**
- Validation of any set of complexes: `python3 scans/validate.py <run_dir> <list file> <tag>`, inside the run
  folder. It writes `scans/validation_<tag>.csv`, and `publish.py` uses the same code.
- Export in the delivery format: `scans/export_points.py`.
- Publication: `aurora/publish.py`, which is called by `aurora/go.sh publish` after `aurora/audit.py`.
- This report: `python3 aurora/campaign_report.py <run_dir> [<aurora-results checkout>] > aurora/CAMPAIGN_REPORT.md`.
  It only reads, and at the end of the campaign it picks up the remaining complexes by itself.

How the campaign was operated (farms, queues, charging, failures) is in `HPC_LESSONS.md` and the Run log.
