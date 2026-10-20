# Zn relaxed-scan results from ALCF Aurora

`scan_results/` is the export of `scans/export_points.py` (the `scan_results.tar.gz` of `nersc/README.md`), added complex by complex as each finishes on Aurora. Code and run log: branch `aurora`, `aurora/README.md`.

- `scan_results/<REF>.xyz`: one frame per point that passes `scans/validate.py`; comment line `REF coordinate branch step= offset= value= E_rel_kJ= E_h=`
- `scan_results/validation_scan_full.csv`: the `validate.py` row of every point of the published complexes
- `scan_results/coords/<REF>.json`: the scanned coordinates

A complex is added when all its branches have terminated normally and `aurora/audit.py` finds no problem (every ORCA output matches its own folder's input; no folder run twice at once).

## Published (7 complexes, 2011 points)

| Complex | Atoms | Branches | Points | Passing | Published |
|---|---|---|---|---|---|
| FATJUG | 49 | 30 | 302 | 280 | 2026-10-19 |
| GALGEG | 49 | 30 | 302 | 298 | 2026-10-19 |
| HUCCIU | 50 | 30 | 302 | 296 | 2026-10-19 |
| QOQYEA | 50 | 30 | 302 | 292 | 2026-10-19 |
| QORPUI | 52 | 30 | 302 | 302 | 2026-10-20 |
| WUCGIN | 51 | 30 | 302 | 249 | 2026-10-20 |
| ZEFGAS | 51 | 30 | 302 | 294 | 2026-10-19 |

## Lower minimum than stage 2

A branch fell more than 2 kJ/mol below its start (`energy_drop`), so the complex has a lower minimum than the stage-2 geometry; points past the drop are not exported.

None so far.

## Finished but not exported

No branch start passes validation, so no point is usable as defined (for example a non-donor atom within 2.6 A of Zn at the stage-2 minimum).

None so far.
