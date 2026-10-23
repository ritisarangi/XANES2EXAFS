# Zn relaxed-scan results from ALCF Aurora

`scan_results/` is the export of `scans/export_points.py` (the `scan_results.tar.gz` of `nersc/README.md`), added complex by complex as each finishes on Aurora. Code and run log: branch `aurora`, `aurora/README.md`.

- `scan_results/<REF>.xyz`: one frame per point that passes `scans/validate.py`; comment line `REF coordinate branch step= offset= value= E_rel_kJ= E_h=`
- `scan_results/validation_scan_full.csv`: the `validate.py` row of every point of the published complexes
- `scan_results/coords/<REF>.json`: the scanned coordinates

A complex is added when all its branches have terminated normally and `aurora/audit.py` finds no problem (every ORCA output matches its own folder's input; no folder run twice at once).

## Published (60 complexes, 17006 points)

| Complex | Atoms | Branches | Points | Passing | Published |
|---|---|---|---|---|---|
| ALACUL | 39 | 30 | 302 | 294 | 2026-10-23 |
| AMETZN | 33 | 30 | 302 | 294 | 2026-10-23 |
| AYIFAP | 43 | 30 | 302 | 291 | 2026-10-23 |
| AYUQOC | 51 | 30 | 302 | 290 | 2026-10-23 |
| BMBTZN | 61 | 30 | 302 | 297 | 2026-10-23 |
| BUNTOW | 25 | 30 | 302 | 300 | 2026-10-23 |
| CADKUO | 45 | 30 | 302 | 302 | 2026-10-23 |
| CUCJAL | 53 | 30 | 302 | 292 | 2026-10-23 |
| CURLUW | 39 | 30 | 302 | 302 | 2026-10-23 |
| DILGUA | 53 | 30 | 302 | 302 | 2026-10-20 |
| DUFYUY | 17 | 30 | 302 | 299 | 2026-10-23 |
| EDUPEZ | 47 | 30 | 302 | 225 | 2026-10-23 |
| EFEWUI | 38 | 30 | 302 | 298 | 2026-10-23 |
| EGORAT | 65 | 30 | 302 | 286 | 2026-10-23 |
| EVOJOO | 49 | 30 | 302 | 287 | 2026-10-23 |
| FATJUG | 49 | 30 | 302 | 280 | 2026-10-19 |
| FEYNUT | 93 | 30 | 302 | 286 | 2026-10-23 |
| GADFUO | 51 | 30 | 302 | 294 | 2026-10-23 |
| GAKKUY | 49 | 30 | 302 | 234 | 2026-10-21 |
| GALGEG | 49 | 30 | 302 | 298 | 2026-10-19 |
| GILZEG | 49 | 30 | 302 | 299 | 2026-10-23 |
| GUYHEN | 49 | 30 | 302 | 204 | 2026-10-21 |
| HEFHUX | 53 | 30 | 302 | 286 | 2026-10-23 |
| HOSXAR | 61 | 30 | 302 | 294 | 2026-10-23 |
| HUCCIU | 50 | 30 | 302 | 296 | 2026-10-19 |
| ICUCIT | 49 | 30 | 302 | 272 | 2026-10-23 |
| ICUCOZ | 49 | 30 | 302 | 295 | 2026-10-23 |
| JADMEK | 71 | 30 | 302 | 290 | 2026-10-23 |
| JEYTAI | 33 | 30 | 302 | 296 | 2026-10-23 |
| KOPYOD | 47 | 30 | 302 | 291 | 2026-10-23 |
| LAQBIP | 51 | 30 | 302 | 302 | 2026-10-21 |
| LEQHAU | 17 | 30 | 302 | 300 | 2026-10-23 |
| LUKREP | 53 | 30 | 302 | 291 | 2026-10-23 |
| MIYPAM | 89 | 30 | 302 | 245 | 2026-10-23 |
| MOZSIE | 53 | 30 | 302 | 282 | 2026-10-21 |
| NEHKIU | 53 | 30 | 302 | 300 | 2026-10-20 |
| NIGTEC | 96 | 30 | 302 | 302 | 2026-10-21 |
| OJELEU | 135 | 30 | 302 | 302 | 2026-10-22 |
| OKAROJ | 47 | 30 | 302 | 294 | 2026-10-23 |
| QOQYEA | 50 | 30 | 302 | 292 | 2026-10-19 |
| QORPUI | 52 | 30 | 302 | 302 | 2026-10-20 |
| QUFSAL | 17 | 30 | 302 | 298 | 2026-10-23 |
| RATHOL | 55 | 30 | 302 | 294 | 2026-10-21 |
| SENFOG | 59 | 30 | 302 | 296 | 2026-10-23 |
| SEWZUS | 57 | 30 | 302 | 261 | 2026-10-23 |
| SEYCIL | 61 | 30 | 302 | 281 | 2026-10-23 |
| SOCSAE | 51 | 30 | 302 | 299 | 2026-10-20 |
| SUYTIR | 53 | 30 | 302 | 291 | 2026-10-21 |
| TACIZN | 41 | 30 | 302 | 302 | 2026-10-23 |
| TBZZNP01 | 51 | 30 | 302 | 226 | 2026-10-21 |
| TIQLOU | 69 | 30 | 302 | 302 | 2026-10-23 |
| TIXQOH | 92 | 30 | 302 | 302 | 2026-10-22 |
| TIXREY | 48 | 30 | 302 | 302 | 2026-10-23 |
| VOJHIO | 53 | 30 | 302 | 97 | 2026-10-21 |
| VUVVAM | 55 | 30 | 302 | 254 | 2026-10-21 |
| WEDVEG | 51 | 30 | 302 | 293 | 2026-10-23 |
| WUCGIN | 51 | 30 | 302 | 249 | 2026-10-20 |
| XAJQAB | 95 | 30 | 302 | 277 | 2026-10-23 |
| XUSTAG | 21 | 30 | 302 | 302 | 2026-10-23 |
| ZEFGAS | 51 | 30 | 302 | 294 | 2026-10-19 |

## Lower minimum than stage 2

A branch fell more than 2 kJ/mol below its start (`energy_drop`), so the complex has a lower minimum than the stage-2 geometry; points past the drop are not exported.

- GAKKUY: angle_S2-Zn-S3 neg step 9 at -4.906 kJ/mol
- ICUCIT: angle_N2-Zn-N3 pos step 8 at -10.556 kJ/mol
- XAJQAB: angle_N22-Zn-N69 neg step 9 at -21.073 kJ/mol

## Finished but not exported

No branch start passes validation, so no point is usable as defined (for example a non-donor atom within 2.6 A of Zn at the stage-2 minimum).

- OGUGON: all 30 branches finished; branch starts fail validation (new_contact 30)
