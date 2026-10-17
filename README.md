# XANES2EXAFS: Zn model-complex DFT and spectra dataset

This repository holds the code, inputs and small metadata for a Zn K-edge XANES/EXAFS dataset built from mononuclear Zn complexes in the CSD. Calculation output stays on S3DF at `/sdf/data/ssrl/smb/xas/users/ritis/`. Git tracks only what is needed to regenerate it.

## Pipeline

| Step | What it does | Where |
|---|---|---|
| Curation | 778 CSD CIFs reduced to 347 unique mononuclear Zn complexes; counterions and solvent removed, H added and checked, disorder cleaned | `curation/`, output in `structures/` |
| Stage 1 | r2SCAN-3c, CPCM(water), Opt from the crystal geometry | `dft/stage1_r2scan/<REF>/<REF>.inp` |
| Stage 2 | B3LYP-D3(BJ), def2-TZVP on Zn and first-shell donors, def2-SVP elsewhere, def2/J RIJCOSX, CPCM(water), TightOpt, analytic Freq, DefGrid3 | input written on the node by `dft/scripts/make_stage2_inp.py`; donor indices in `dft/stage2_b3lyp/<REF>/<REF>.meta` |
| Perturbation scans | Relaxed 1D scans at the stage-2 level (B3LYP-D3BJ, mixed basis, CPCM, TightOpt), one coordinate constrained, everything else relaxed: Zn–L bonds −0.06 to +0.20 Å in 0.02 Å steps; L–Zn–L angles ±15° in 1.5°; donor twist dihedral ±10° in 1°; Zn–L–C–X tilt dihedrals ±10° in 1°. Each coordinate runs as two branches starting at the minimum | `scans/` |
| Spectra (planned) | FEFF XANES and EXAFS per geometry; Debye-Waller factors from the stage-2 Hessians and the frequency–distance relation | to be added under `feff/` |

## Layout

```
structures/dft_ready_xyz/      347 starting geometries; comment line holds REF, charge, mult, formula
structures/dft_ready_manifest.csv
structures/excluded_duplicates/
curation/                      CIF parsing, dedup, protonation, cleanup and audit scripts
dft/lists/                     all.txt, pilot.txt, rest_00..03 (Slurm arrays are capped at 100 tasks)
dft/scripts/                   Slurm arrays, submit.sh, status.py, make_stage2_inp.py
dft/analysis/                  stage-1 summary, Zn–L statistics, imaginary-mode analysis
results/                       small summary tables
```

## Running on S3DF

The account is `ssrl:smbxas`, partition `milano`, with a group limit of 1,440 CPUs. Slurm's `MaxArraySize` is 100, so lists longer than 99 entries are split.

```
s3df sh                                   # from the Mac, in a folder whose s3df.env names the project
python3 scripts/status.py lists/all.txt   # typed at the S3DF prompt
exit
```

Submit a list (stage 2 waits on stage 1 task by task):

```
S1MAX=20 S2MAX=10 bash scripts/submit.sh lists/rest_00
```

## Scans

Run inside the project folder on S3DF:

```
python3 ../XANES2EXAFS/scans/make_scans.py . lists/pilot.txt        # writes scans/<REF>/... and scans/jobs_pilot.txt
bash ../XANES2EXAFS/scans/submit_scans.sh scans/jobs_pilot.txt      # ACCOUNT=..., MAX=... optional
python3 ../XANES2EXAFS/scans/validate.py . lists/pilot.txt          # pass/fail per point, pass rates, cost
```

A CN-4 complex gives 30 branch jobs and 273 geometries. `validate.py` keeps a point only if its optimisation converged, the constraint was met, the bond graph matches the reference, every donor stays bound with unscanned Zn–L within 0.15 Å, no new atom comes within 2.6 Å of Zn, the energy stays within 40 kJ/mol of the minimum without dropping more than 2 kJ/mol between steps, and no heavy-atom distance jumps more than 0.3 Å between steps. After the first failure the rest of that branch is dropped.

Branches stopped by the 72-hour limit or a cancellation are continued from their last converged step:

```
bash ../XANES2EXAFS/scans/submit_restart.sh      # finds stopped branches, writes continuation inputs, submits (ACCOUNT=ssrl:default by default)
```

The kept steps go to `scan_acc.txt`, the original input to `scan_orig.inp`, and the continuation to `scan_cont.out`; when it finishes, `scan.out` is rewritten as one continuous scan for `validate.py`.

## Dielectric series

Re-optimises each complex with analytic frequencies at other CPCM dielectric constants, starting from the stage-2 geometry at the stage-2 level. Only epsilon changes; the water cavity is kept (Rsolv 1.30). Each Zn–L bond then has r, k and σ² at several dielectrics, which give a per-bond slope of ln k against r to compare with the relaxed scans.

```
python3 ../XANES2EXAFS/dielectric/make_eps.py . lists/pilot.txt 4 2       # writes dielectric/eps4, eps2 and dielectric/jobs_pilot.txt
bash ../XANES2EXAFS/dielectric/submit_eps.sh dielectric/jobs_pilot.txt     # ACCOUNT=..., MAX=... optional
python3 ../XANES2EXAFS/dielectric/analyze_eps.py . lists/pilot.txt 4 2    # per-bond r, k, sigma2 and slopes; dielectric/eps_compare_pilot.csv
```

## One-electron change (redox pair)

Re-optimises each complex with analytic frequencies at its charge moved one unit toward neutral: q > 0 to q − 1, q < 0 to q + 1, q = 0 to +1 with −1 as the fallback when the +1 run does not finish. Odd electron counts run as UKS doublets. Each Zn–L bond then has (r, k, σ²) in two states; a bond counts when 0.01 ≤ |Δr| ≤ 0.15 Å with the donor still bound.

```
python3 ../XANES2EXAFS/redox/make_redox.py . lists/pilot.txt        # redox/primary, redox/fallback, redox/jobs_pilot.txt
bash ../XANES2EXAFS/redox/submit_redox.sh redox/jobs_pilot.txt      # ACCOUNT=ssrl:default, MAX=20 by default
python3 ../XANES2EXAFS/redox/analyze_redox.py . lists/pilot.txt     # per-bond dr, dk/k, slope, spin; redox/redox_compare_pilot.csv
```

## Other clusters

Cluster settings live in `sites/<site>.sh` (`s3df`, `nersc`); the scan submit scripts read `SITE`. `scans/make_bundle.py` packs the stage-2 geometries for another cluster, `nersc/go.sh` runs the full scan set on Perlmutter, and `scans/export_points.py` packs the passing geometries for the trip back. See `nersc/README.md`.

## Data policy

Each job runs in node-local scratch and keeps only final geometries, energies, frequencies, Hessians for the reference structures, and spectra (`xmu.dat`, `chi.dat`, `feff.inp`). Per-job results go to small HDF5 files that are merged into one dataset. ORCA `.gbw`, trajectories and FEFF potential and phase files are deleted after extraction. Only the merged dataset leaves S3DF.

## Status (2026-10-15)

Stage 1: 346 of 347 converged; VIKDUP crashed in the SCF and needs a rerun. Stage 2: in progress. Imaginary modes so far: OKARID (two NH2 wags near −130 cm⁻¹, to be displaced and re-optimized); ICUCOZ and ICUDAM (methyl rotations, kept); RIBMEV (−20 cm⁻¹, mode type to be confirmed); RAXDAV and XUVWES (below 5 cm⁻¹, grid noise, kept).
