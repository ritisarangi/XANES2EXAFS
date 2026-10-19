# Zn relaxed-scan results from ALCF Aurora

Validated geometries and energies from the relaxed one-coordinate scans of the XANES2EXAFS Zn model complexes, computed on ALCF Aurora. This branch holds data only; the code that made it is on the `aurora` branch (`aurora/README.md`), and the scan definitions are in `scans/make_scans.py`.

## What is here

The geometry files use exactly the frame format of `scans/export_points.py` (the `scan_results/<REF>.xyz` of the NERSC instructions); the validation rows are `scans/validate.py` output, split per complex. At the end of the campaign the same points are also packed as `scan_results.tar.gz` with `go.sh export`.

A complex appears here once every one of its scan branches has finished. Only points that pass `scans/validate.py` are included as geometries; the validation row of every point (passing or not, with the reason) is kept beside them.

| Path | Content |
|---|---|
| `scan_points/<REF>.xyz` | One frame per passing point. Comment line: `REF coordinate branch step=<n> offset=<from minimum> value=<scanned value> E_rel_kJ=<vs branch start> E_h=<absolute energy>` |
| `validation/<REF>.csv` | `scans/validate.py` result for every point of the complex: `status` is `pass`, the first failure reason (`new_contact`, `jump`, `energy_drop`, `shell`, `bonds`, `constraint`, `not_converged`, `energy_cap`, `ref_mismatch`), or `after_fail` for points beyond a branch's first failure |
| `coords/<REF>.json` | The scanned coordinates of the complex: type, atom indices (0-based, stage-2 atom order), start value, branch ends and folder names |
| `summary.csv` | One line per published complex: atoms, branches, points, passing points, failure reasons, date published |
| `FLAGGED.md` | Finished complexes not published because no branch start passes validation |
| `LOWER_MINIMA.md` | Complexes where a branch fell more than 2 kJ/mol below its start (`energy_drop`): the complex has a lower minimum than the stage-2 geometry (the list `nersc/README.md` asks for) |

Units: angstrom, degrees, hartree (`E_h`), kJ/mol (`E_rel_kJ`). Bond offsets are in angstrom, angle and dihedral offsets in degrees.

## Method

B3LYP-D3(BJ), def2-TZVP on Zn and the first-shell donors, def2-SVP elsewhere, def2/J, RIJCOSX, CPCM(water), DefGrid3, TightSCF, TightOpt; relaxed surface scans with one coordinate constrained and everything else relaxed, each coordinate as two branches starting at the stage-2 minimum (bonds -0.06 to +0.20 A in 0.02 A; angles +-15 deg in 1.5 deg; donor twist and Zn-L-C-X tilts +-10 deg in 1 deg). ORCA 6.0.1 with OpenMPI 4.1.6 on Aurora CPU nodes (Xeon Max 9470C), 4 MPI ranks per ORCA job (8 for complexes of 100 atoms or more). The first SCF at the stage-2 geometry reproduces the S3DF stage-2 energies to 1e-6 hartree.

Branches stopped by a job's walltime were continued from their last optimisation geometry at the same target and stitched into one scan (`scans/restart.py`); the stitched branch is validated as one piece.

## Checks before a complex is published

1. `aurora/audit.py` finds no problem: every ORCA output in a branch folder echoes that folder's own input (coordinate, atoms, charge, multiplicity), no folder was ever run by two ORCA processes at once, and no branch was queued twice.
2. Every branch of the complex terminated normally.
3. `scans/validate.py` passes the point (converged, constraint met, bond graph and first shell intact, no new Zn contact, energy continuity, branch start reproduces the stage-2 minimum).
