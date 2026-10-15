# XANES2EXAFS: Zn model-complex DFT and spectra dataset

This repository holds the code, inputs and small metadata for a Zn K-edge XANES/EXAFS dataset built from mononuclear Zn complexes in the CSD. Calculation output stays on S3DF at `/sdf/data/ssrl/smb/xas/users/ritis/`. Git tracks only what is needed to regenerate it.

## Pipeline

| Step | What it does | Where |
|---|---|---|
| Curation | 778 CSD CIFs reduced to 347 unique mononuclear Zn complexes; counterions and solvent removed, H added and checked, disorder cleaned | `curation/`, output in `structures/` |
| Stage 1 | r2SCAN-3c, CPCM(water), Opt from the crystal geometry | `dft/stage1_r2scan/<REF>/<REF>.inp` |
| Stage 2 | B3LYP-D3(BJ), def2-TZVP on Zn and first-shell donors, def2-SVP elsewhere, def2/J RIJCOSX, CPCM(water), TightOpt, analytic Freq, DefGrid3 | input written on the node by `dft/scripts/make_stage2_inp.py`; donor indices in `dft/stage2_b3lyp/<REF>/<REF>.meta` |
| Perturbation scans (planned) | Relaxed 1D scans on the Zn core: 4 Zn–L bonds, 6 L–Zn–L angles, 1 donor-plane twist dihedral, 4 Zn–L–C–C ligand-tilt dihedrals, about 21 points each | to be added under `scans/` |
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

## Data policy

Each job runs in node-local scratch and keeps only final geometries, energies, frequencies, Hessians for the reference structures, and spectra (`xmu.dat`, `chi.dat`, `feff.inp`). Per-job results go to small HDF5 files that are merged into one dataset. ORCA `.gbw`, trajectories and FEFF potential and phase files are deleted after extraction. Only the merged dataset leaves S3DF.

## Status (2026-10-15)

Stage 1: 346 of 347 converged; VIKDUP crashed in the SCF and needs a rerun. Stage 2: in progress. Imaginary modes so far: OKARID (two NH2 wags near −130 cm⁻¹, to be displaced and re-optimized); ICUCOZ and ICUDAM (methyl rotations, kept); RIBMEV (−20 cm⁻¹, mode type to be confirmed); RAXDAV and XUVWES (below 5 cm⁻¹, grid noise, kept).
