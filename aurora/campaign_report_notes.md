# Hand-written sections of aurora/CAMPAIGN_REPORT.md

`aurora/campaign_report.py` includes each section below verbatim, at the place named by its `<!-- name -->`
marker. Lines above the first marker (this header) are not included. Keep numbers that will change as the
campaign ends in the script, not here; numbers below are fixed facts (thresholds, measured checks, dated events).

<!-- summary -->
**Reading guide.** The results are the `scan_results/` folder on branch `aurora-results`. Its layout and its
README are the deliverable; this report does not change them. Each published point is one constrained
optimisation that passed `scans/validate.py`. The *Complexes that need Riti's attention* section lists what
needs a chemist's decision. The *Decisions for Riti* section turns that into numbered choices, each with a
recommendation and a cost. Atom labels such as `N5` or `O62` are 0-based indices into the stage-2 xyz, so
`N5` is atom 5 counted from 0. This is the same convention as the coordinate names in `coords/<REF>.json`.
Facts come from files and code. *Inference* marks interpretation.

<!-- method -->
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

<!-- validation -->
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

<!-- attention -->
Sections (a) to (g) are ordered by consequence. Each one gives evidence first, then a recommended action. The
recommended actions are collected as numbered choices under *Decisions for Riti*.

<!-- not_exported -->
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

<!-- lower_minima -->
**Not yet examined.** Complexes published after 2026-10-31 appear in the list above but are not covered by the
geometry check below. The deepest among them are WEDVIK (-29.3 kJ/mol, a `shell` failure), TEYSOG (-27.5),
GEQCUE (-14.8) and LAPYAD (-12.2). They will get the same check when the campaign ends.

**What the structures show.** This is a read-only geometry check of the lowest first-failing point of each
complex on 2026-10-31: the Zn-donor distances at step 0 and at the failing step, the nearest non-donors, and
the heavy-atom pair that changed most. Three kinds stand out.

1. **The first shell changes: a different species lies lower** (*inference* for the chemical labels).
   - **TIFNOO**: the deepest at -32 to -44 kJ/mol. At Zn-S3 or Zn-S4 +0.08 A, the other S leaves (3.51 A) and the
     ring N9/N10, at 2.76 A at stage 2, bind at 2.03/2.23 A. This is an S -> N linkage switch like KERJOI and
     FECYIZ, here reached during the scan. The published points describe the S-bound local minimum.
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
   -12.7 kJ/mol, where carbonyl O7 reaches 2.60 A. In HOZGAF and NAMSOJ most branches drop
   by about 16 kJ/mol already at step 1-3, so the stage-2 geometry is not the lowest conformer and possibly not
   a true minimum. The stage-2 frequencies on S3DF would settle this. For the Zn K-edge the first shell is what
   matters, so these published points are probably still representative (*inference*). Their energies are
   relative to a conformer that is not the lowest.
3. **Small drops of 2-3 kJ/mol** (UFUROC, ZNDITZ11, FEKRAO, TARNIJ, ICAVAK, OJELOE, WIGBIX, FEKQOB): flat surfaces.
   *Inference*: no action needed beyond noting them.

**Recommended action.** For kind 1, decide per complex: either keep the published points as a labelled local
minimum (0 compute), or re-optimise stage 2 from the lowest scan geometry and re-scan (about 3-9 node-hours per
complex). TIFNOO and GUYHEN deserve this most; the six S-chelate cases are only 4-6 kJ/mol apart. For kind 2,
check the stage-2 frequencies on S3DF for HOZGAF, NAMSOJ, XAJQAB, ICUCIT and KAKYAW (0 compute). Re-scan only
if an imaginary mode or a strongly different conformer matters for the spectra.

<!-- low_pass -->
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

<!-- nonconverged -->
No published point failed as `not_converged`, so none of the published points is a non-converged step. Steps
that did not converge in an earlier run are not visible in the stitched `scan.out`, because only converged
step blocks are kept. They appear only in `scan_try*.out` and the logs. One case is recorded in the Run log:
on 2026-10-28, OJELOE angle_S3-Zn-N100 neg, step 10, reached ORCA's 100 optimisation cycles (`%geom MaxIter
100`) on Perlmutter after about 23 h. It was continued from its last geometry, converged, and OJELOE was
published (`Run log` 10-28 08:20 and 09:36). Other steps of this kind on Aurora (MaxIter reached, then
continued) were not counted; that would need a pass over all logs and `scan_try*.out` (not done; Lustre
load). *Inference*: such a step converges to the same constrained minimum, but after more than 100 cycles on a
flat surface.

<!-- ref_mismatch -->
**Measured on 2026-10-31 (read-only).** At step 0 of these branches, the largest heavy-atom distance
difference to the stage-2 geometry is **0.057 A**, against a limit of 0.05 A. The energy differs by only
-0.062 kJ/mol (RIBMEV) and -0.004 kJ/mol (RAYBIC) from stage 2. Step 0 re-optimises the stage-2 geometry with
the coordinate held at its own value. In these soft complexes the TightOpt settled 0.007 A past the tolerance.
*Inference*: these are the same minimum. Raising the step-0 geometry tolerance to 0.06 A, or accepting these
five branches by hand, recovers the points in the table at zero compute. Recommended.

<!-- shell_check -->
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

<!-- decisions -->
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
4. **Lower minima with a first-shell change** (TIFNOO -44, GUYHEN -18.6; DIFBOK, HULBIZ, MUJJUW, RIBMEV, RIBMIZ,
   WUCGIN -4 to -6 kJ/mol): keep the published points as labelled local minima, or re-optimise stage 2 from the
   lowest scan geometry and re-scan. *Recommended:* re-scan TIFNOO and GUYHEN. Keep the six S-chelate cases,
   noting the near-degenerate six-coordinate form. *Cost:* 0, or about 3-9 node-hours per re-scanned complex.
5. **Conformer drops** (HOZGAF, NAMSOJ, XAJQAB, ICUCIT, KAKYAW; first shell almost unchanged): check the stage-2
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

<!-- where -->
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
