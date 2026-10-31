# Zn relaxed-scan results from ALCF Aurora

`scan_results/` is the export of `scans/export_points.py` (the `scan_results.tar.gz` of `nersc/README.md`), added complex by complex as each finishes on Aurora. Code and run log: branch `aurora`, `aurora/README.md`.

- `scan_results/<REF>.xyz`: one frame per point that passes `scans/validate.py`; comment line `REF coordinate branch step= offset= value= E_rel_kJ= E_h=`
- `scan_results/validation_scan_full.csv`: the `validate.py` row of every point of the published complexes
- `scan_results/coords/<REF>.json`: the scanned coordinates

A complex is added when all its branches have terminated normally and `aurora/audit.py` finds no problem (every ORCA output matches its own folder's input; no folder run twice at once).

## Published (238 complexes, 65651 points)

| Complex | Atoms | Branches | Points | Passing | Published |
|---|---|---|---|---|---|
| ABIDEU | 69 | 30 | 302 | 302 | 2026-10-24 |
| ADOLOU | 81 | 53 | 541 | 477 | 2026-10-27 |
| AHOQIY | 39 | 30 | 302 | 293 | 2026-10-24 |
| ALACUL | 39 | 30 | 302 | 294 | 2026-10-23 |
| AMETZN | 33 | 30 | 302 | 294 | 2026-10-23 |
| AYIFAP | 43 | 30 | 302 | 291 | 2026-10-23 |
| AYUQOC | 51 | 30 | 302 | 290 | 2026-10-23 |
| AZIJIC | 78 | 30 | 302 | 302 | 2026-10-30 |
| BELDUS | 59 | 30 | 302 | 238 | 2026-10-26 |
| BELFEE | 47 | 30 | 302 | 297 | 2026-10-24 |
| BELFII | 44 | 30 | 302 | 297 | 2026-10-24 |
| BMBTZN | 61 | 30 | 302 | 297 | 2026-10-23 |
| BUNNII | 137 | 30 | 302 | 182 | 2026-10-31 |
| BUNTOW | 25 | 30 | 302 | 300 | 2026-10-23 |
| CADKUO | 45 | 30 | 302 | 302 | 2026-10-23 |
| CAPWIB | 65 | 30 | 302 | 292 | 2026-10-31 |
| CAXBEM | 69 | 30 | 302 | 286 | 2026-10-27 |
| CAXBIQ | 59 | 30 | 302 | 294 | 2026-10-24 |
| CAXBUC | 64 | 30 | 302 | 227 | 2026-10-25 |
| CUCJAL | 53 | 30 | 302 | 292 | 2026-10-23 |
| CURLOQ | 25 | 30 | 302 | 302 | 2026-10-24 |
| CURLUW | 39 | 30 | 302 | 302 | 2026-10-23 |
| CUSGEE | 82 | 30 | 302 | 275 | 2026-10-30 |
| DASFUY | 21 | 30 | 302 | 298 | 2026-10-24 |
| DASMOZ | 41 | 30 | 302 | 296 | 2026-10-24 |
| DASPOC | 43 | 30 | 302 | 295 | 2026-10-24 |
| DIFBIE | 45 | 30 | 302 | 293 | 2026-10-25 |
| DIFBOK | 55 | 30 | 302 | 264 | 2026-10-24 |
| DILGUA | 53 | 30 | 302 | 302 | 2026-10-20 |
| DOMMOH | 37 | 30 | 302 | 294 | 2026-10-24 |
| DOMMUN | 45 | 30 | 302 | 291 | 2026-10-24 |
| DOZVOF | 111 | 30 | 302 | 294 | 2026-10-29 |
| DUFYUY | 17 | 30 | 302 | 299 | 2026-10-23 |
| EBEXIS | 66 | 28 | 280 | 180 | 2026-10-27 |
| EDUPEZ | 47 | 30 | 302 | 225 | 2026-10-23 |
| EFEWUI | 38 | 30 | 302 | 298 | 2026-10-23 |
| EGORAT | 65 | 30 | 302 | 286 | 2026-10-23 |
| EQOFEW | 63 | 30 | 302 | 278 | 2026-10-27 |
| EVOJOO | 49 | 30 | 302 | 287 | 2026-10-23 |
| FADYOY | 41 | 30 | 302 | 280 | 2026-10-25 |
| FAJZAS | 78 | 30 | 302 | 300 | 2026-10-27 |
| FATJUG | 49 | 30 | 302 | 280 | 2026-10-19 |
| FEKRAO | 65 | 30 | 302 | 228 | 2026-10-27 |
| FEKTAQ | 29 | 30 | 302 | 291 | 2026-10-24 |
| FEYNUT | 93 | 30 | 302 | 286 | 2026-10-23 |
| FILGEN | 43 | 30 | 302 | 298 | 2026-10-24 |
| FIYQIP | 69 | 26 | 258 | 248 | 2026-10-24 |
| GADFUO | 51 | 30 | 302 | 294 | 2026-10-23 |
| GAKKUY | 49 | 30 | 302 | 234 | 2026-10-21 |
| GALGAC | 47 | 30 | 302 | 296 | 2026-10-24 |
| GALGEG | 49 | 30 | 302 | 298 | 2026-10-19 |
| GALGIK | 47 | 30 | 302 | 274 | 2026-10-24 |
| GEXZOY | 81 | 30 | 302 | 276 | 2026-10-25 |
| GILZEG | 49 | 30 | 302 | 299 | 2026-10-23 |
| GIXTAL | 57 | 30 | 302 | 153 | 2026-10-28 |
| GOLCIU01 | 43 | 30 | 302 | 295 | 2026-10-25 |
| GOWRAL | 53 | 30 | 302 | 240 | 2026-10-25 |
| GUCSED | 105 | 30 | 302 | 288 | 2026-10-28 |
| GUFHEU | 105 | 30 | 302 | 284 | 2026-10-30 |
| GUYHEN | 49 | 30 | 302 | 204 | 2026-10-21 |
| HEFHUX | 53 | 30 | 302 | 286 | 2026-10-23 |
| HIJGEM | 13 | 30 | 302 | 298 | 2026-10-24 |
| HOMQAC | 115 | 30 | 302 | 297 | 2026-10-27 |
| HOSXAR | 61 | 30 | 302 | 294 | 2026-10-23 |
| HOZGEJ | 99 | 30 | 302 | 282 | 2026-10-25 |
| HOZGIN | 95 | 30 | 302 | 298 | 2026-10-24 |
| HUBBIQ | 80 | 30 | 302 | 300 | 2026-10-30 |
| HUCCIU | 50 | 30 | 302 | 296 | 2026-10-19 |
| HULBIZ | 57 | 30 | 302 | 243 | 2026-10-24 |
| ICATOW | 77 | 30 | 302 | 272 | 2026-10-25 |
| ICAVAK | 101 | 30 | 302 | 291 | 2026-10-27 |
| ICAVEO | 81 | 30 | 302 | 300 | 2026-10-31 |
| ICEHOP | 73 | 30 | 302 | 293 | 2026-10-24 |
| ICONOE | 85 | 30 | 302 | 302 | 2026-10-30 |
| ICUCAL | 46 | 30 | 302 | 218 | 2026-10-24 |
| ICUCEP | 46 | 30 | 302 | 296 | 2026-10-24 |
| ICUCIT | 49 | 30 | 302 | 272 | 2026-10-23 |
| ICUCOZ | 49 | 30 | 302 | 295 | 2026-10-23 |
| ICUDAM | 49 | 30 | 302 | 242 | 2026-10-24 |
| IGURAD | 81 | 30 | 302 | 296 | 2026-10-30 |
| IGURIL | 78 | 30 | 302 | 288 | 2026-10-31 |
| IQETOP | 39 | 30 | 302 | 268 | 2026-10-24 |
| JADMAG | 65 | 30 | 302 | 257 | 2026-10-24 |
| JADMEK | 71 | 30 | 302 | 290 | 2026-10-23 |
| JAMJAJ | 47 | 30 | 302 | 298 | 2026-10-24 |
| JAXFEW | 81 | 30 | 302 | 289 | 2026-10-31 |
| JEYTAI | 33 | 30 | 302 | 296 | 2026-10-23 |
| KAKVAT | 45 | 30 | 302 | 221 | 2026-10-25 |
| KAKVEX | 53 | 30 | 302 | 286 | 2026-10-24 |
| KAKVIB01 | 49 | 30 | 302 | 204 | 2026-10-25 |
| KAKYAW | 51 | 30 | 302 | 231 | 2026-10-25 |
| KAKYEA | 51 | 30 | 302 | 299 | 2026-10-24 |
| KAKYUQ | 47 | 30 | 302 | 244 | 2026-10-25 |
| KALDIK | 49 | 30 | 302 | 271 | 2026-10-25 |
| KEXPEJ | 80 | 30 | 302 | 285 | 2026-10-31 |
| KEXQEK | 82 | 30 | 302 | 264 | 2026-10-30 |
| KOMLIH01 | 53 | 30 | 302 | 295 | 2026-10-24 |
| KOPYOD | 47 | 30 | 302 | 291 | 2026-10-23 |
| KOXDIN | 55 | 30 | 302 | 297 | 2026-10-24 |
| KUBVIN | 49 | 30 | 302 | 264 | 2026-10-25 |
| KUNDIH | 67 | 30 | 302 | 297 | 2026-10-25 |
| LAPYOR | 75 | 30 | 302 | 286 | 2026-10-24 |
| LAQBIP | 51 | 30 | 302 | 302 | 2026-10-21 |
| LEMVAB | 37 | 30 | 302 | 294 | 2026-10-24 |
| LEMVEF | 49 | 30 | 302 | 292 | 2026-10-24 |
| LEQHAU | 17 | 30 | 302 | 300 | 2026-10-23 |
| LIYFEG01 | 59 | 30 | 302 | 281 | 2026-10-24 |
| LUKREP | 53 | 30 | 302 | 291 | 2026-10-23 |
| LUVFUD | 60 | 30 | 302 | 301 | 2026-10-25 |
| LUZTEF | 81 | 30 | 302 | 298 | 2026-10-26 |
| MAZBZN10 | 49 | 30 | 302 | 288 | 2026-10-27 |
| MEPWOT | 38 | 28 | 280 | 248 | 2026-10-24 |
| MIYPAM | 89 | 30 | 302 | 245 | 2026-10-23 |
| MIYVIA | 63 | 30 | 302 | 294 | 2026-10-24 |
| MIYVOG | 59 | 30 | 302 | 294 | 2026-10-24 |
| MIYVUM | 67 | 30 | 302 | 294 | 2026-10-24 |
| MOYBAD | 57 | 30 | 302 | 270 | 2026-10-25 |
| MOZSIE | 53 | 30 | 302 | 282 | 2026-10-21 |
| MUJJOQ | 49 | 30 | 302 | 295 | 2026-10-25 |
| MUJJUW | 55 | 30 | 302 | 249 | 2026-10-24 |
| NAMSOJ | 104 | 30 | 302 | 212 | 2026-10-27 |
| NAYXAM | 71 | 30 | 302 | 282 | 2026-10-25 |
| NECTOG | 102 | 30 | 302 | 278 | 2026-10-27 |
| NEHKIU | 53 | 30 | 302 | 300 | 2026-10-20 |
| NESCAR | 63 | 30 | 302 | 168 | 2026-10-25 |
| NIGTEC | 96 | 30 | 302 | 302 | 2026-10-21 |
| NIHTEG | 45 | 30 | 302 | 280 | 2026-10-25 |
| NIHTIK | 51 | 30 | 302 | 294 | 2026-10-25 |
| NITZEW | 35 | 30 | 302 | 292 | 2026-10-24 |
| NOCNEY | 65 | 30 | 302 | 270 | 2026-10-24 |
| NONLEI | 117 | 30 | 302 | 288 | 2026-10-28 |
| NUYWOV | 55 | 30 | 302 | 282 | 2026-10-24 |
| OCOZAJ | 43 | 30 | 302 | 286 | 2026-10-24 |
| OCOZOX | 37 | 30 | 302 | 296 | 2026-10-24 |
| OGUWUJ | 86 | 30 | 302 | 291 | 2026-10-31 |
| OJEKIX | 95 | 30 | 302 | 174 | 2026-10-24 |
| OJEKOD | 135 | 30 | 302 | 291 | 2026-10-25 |
| OJEKUJ | 137 | 30 | 302 | 266 | 2026-10-26 |
| OJELEU | 135 | 30 | 302 | 302 | 2026-10-22 |
| OJELOE | 109 | 30 | 302 | 229 | 2026-10-28 |
| OKAROJ | 47 | 30 | 302 | 294 | 2026-10-23 |
| OLIPEG | 57 | 30 | 302 | 189 | 2026-10-25 |
| OVAQIM | 81 | 30 | 302 | 267 | 2026-10-30 |
| OYASOZ | 89 | 30 | 302 | 287 | 2026-10-30 |
| OYASUF | 87 | 30 | 302 | 295 | 2026-10-31 |
| OYATEQ | 92 | 30 | 302 | 291 | 2026-10-28 |
| PAGFEM | 33 | 30 | 302 | 295 | 2026-10-24 |
| PEQSEK | 70 | 30 | 302 | 287 | 2026-10-24 |
| POHTOV | 43 | 30 | 302 | 290 | 2026-10-24 |
| PTOLZN01 | 53 | 30 | 302 | 171 | 2026-10-26 |
| PUMRAQ | 57 | 30 | 302 | 285 | 2026-10-24 |
| PUZKUQ | 33 | 30 | 302 | 289 | 2026-10-24 |
| QAGWII | 73 | 30 | 302 | 284 | 2026-10-25 |
| QASRIL | 53 | 30 | 302 | 263 | 2026-10-24 |
| QASROR | 81 | 30 | 302 | 281 | 2026-10-31 |
| QAWBAS | 79 | 30 | 302 | 302 | 2026-10-30 |
| QELPED | 49 | 30 | 302 | 282 | 2026-10-24 |
| QIBVAZ | 45 | 30 | 302 | 300 | 2026-10-25 |
| QOBKAW | 37 | 30 | 302 | 291 | 2026-10-24 |
| QOQYAW | 71 | 30 | 302 | 289 | 2026-10-25 |
| QOQYEA | 50 | 30 | 302 | 292 | 2026-10-19 |
| QORPUI | 52 | 30 | 302 | 302 | 2026-10-20 |
| QUFSAL | 17 | 30 | 302 | 298 | 2026-10-23 |
| QUQGEO | 31 | 30 | 302 | 295 | 2026-10-24 |
| RADPOB | 81 | 26 | 258 | 254 | 2026-10-24 |
| RAGDUY | 49 | 30 | 302 | 267 | 2026-10-25 |
| RAJHOA | 57 | 40 | 405 | 317 | 2026-10-24 |
| RATHOL | 55 | 30 | 302 | 294 | 2026-10-21 |
| RAXDAV | 37 | 30 | 302 | 292 | 2026-10-24 |
| RAYBIC | 124 | 30 | 302 | 156 | 2026-10-28 |
| REJBUD | 102 | 30 | 302 | 284 | 2026-10-27 |
| RIBMEV | 59 | 30 | 302 | 205 | 2026-10-25 |
| RIBMIZ | 53 | 30 | 302 | 235 | 2026-10-24 |
| RUKJAL | 37 | 30 | 302 | 294 | 2026-10-24 |
| SENFOG | 59 | 30 | 302 | 296 | 2026-10-23 |
| SEWZUS | 57 | 30 | 302 | 261 | 2026-10-23 |
| SEYCIL | 61 | 30 | 302 | 281 | 2026-10-23 |
| SIJKUR | 47 | 30 | 302 | 293 | 2026-10-24 |
| SOCSAE | 51 | 30 | 302 | 299 | 2026-10-20 |
| SONROE | 125 | 30 | 302 | 289 | 2026-10-28 |
| SUYTIR | 53 | 30 | 302 | 291 | 2026-10-21 |
| SUYTOX | 67 | 30 | 302 | 281 | 2026-10-24 |
| TACIZN | 41 | 30 | 302 | 302 | 2026-10-23 |
| TAKZIQ | 69 | 30 | 302 | 292 | 2026-10-25 |
| TAKZUB | 17 | 30 | 302 | 294 | 2026-10-24 |
| TANRAE | 63 | 30 | 302 | 200 | 2026-10-25 |
| TARNIJ | 53 | 30 | 302 | 281 | 2026-10-24 |
| TAVZEW | 75 | 48 | 486 | 484 | 2026-10-24 |
| TBZZNP01 | 51 | 30 | 302 | 226 | 2026-10-21 |
| TIFNOO | 55 | 30 | 302 | 241 | 2026-10-27 |
| TIQLEK | 83 | 30 | 302 | 285 | 2026-10-30 |
| TIQLOU | 69 | 30 | 302 | 302 | 2026-10-23 |
| TIXQOH | 92 | 30 | 302 | 302 | 2026-10-22 |
| TIXREY | 48 | 30 | 302 | 302 | 2026-10-23 |
| UDOCUL | 70 | 30 | 302 | 300 | 2026-10-26 |
| UDODOG | 90 | 30 | 302 | 234 | 2026-10-27 |
| UFUROC | 29 | 30 | 302 | 181 | 2026-10-24 |
| UMEVOY | 39 | 30 | 302 | 291 | 2026-10-24 |
| UQOWIH | 65 | 30 | 302 | 287 | 2026-10-24 |
| UTAXAQ | 81 | 30 | 302 | 242 | 2026-10-30 |
| VAGJES | 35 | 30 | 302 | 296 | 2026-10-24 |
| VAGJIW | 55 | 30 | 302 | 292 | 2026-10-25 |
| VEKDUL | 65 | 30 | 302 | 212 | 2026-10-25 |
| VEKFAT | 74 | 30 | 302 | 298 | 2026-10-27 |
| VEPXOD | 49 | 30 | 302 | 293 | 2026-10-24 |
| VIBLAT | 72 | 30 | 302 | 302 | 2026-10-25 |
| VIKDUP | 37 | 30 | 302 | 289 | 2026-10-25 |
| VOJHIO | 53 | 30 | 302 | 97 | 2026-10-21 |
| VOYFUN | 81 | 30 | 302 | 289 | 2026-10-31 |
| VUHDIL | 89 | 30 | 302 | 294 | 2026-10-25 |
| VUVVAM | 55 | 30 | 302 | 254 | 2026-10-21 |
| WACPAS | 61 | 30 | 302 | 278 | 2026-10-25 |
| WAJNEA | 65 | 30 | 302 | 297 | 2026-10-24 |
| WEDVEG | 51 | 30 | 302 | 293 | 2026-10-23 |
| WIGBIX | 121 | 30 | 302 | 216 | 2026-10-29 |
| WITLAM | 43 | 30 | 302 | 291 | 2026-10-25 |
| WONYUW | 33 | 28 | 280 | 254 | 2026-10-25 |
| WORLUK | 69 | 30 | 302 | 293 | 2026-10-27 |
| WORMAR | 113 | 30 | 302 | 302 | 2026-10-27 |
| WUCGIN | 51 | 30 | 302 | 249 | 2026-10-20 |
| WUJZOS | 127 | 30 | 302 | 154 | 2026-10-26 |
| XAJQAB | 95 | 30 | 302 | 277 | 2026-10-23 |
| XAYGEL | 77 | 30 | 302 | 222 | 2026-10-25 |
| XENWET | 25 | 30 | 302 | 298 | 2026-10-24 |
| XIGZUI | 69 | 30 | 302 | 223 | 2026-10-25 |
| XILGIJ | 49 | 30 | 302 | 290 | 2026-10-24 |
| XIXTEG | 59 | 30 | 302 | 195 | 2026-10-25 |
| XOGYUQ | 49 | 30 | 302 | 204 | 2026-10-25 |
| XOGZAX | 61 | 30 | 302 | 272 | 2026-10-24 |
| XUSTAG | 21 | 30 | 302 | 302 | 2026-10-23 |
| YACTUV | 78 | 30 | 302 | 243 | 2026-10-31 |
| YOLCOR | 45 | 30 | 302 | 234 | 2026-10-24 |
| YOTFEU | 17 | 30 | 302 | 299 | 2026-10-24 |
| ZACWOP | 45 | 30 | 302 | 294 | 2026-10-24 |
| ZAHCAM | 71 | 30 | 302 | 302 | 2026-10-24 |
| ZEFGAS | 51 | 30 | 302 | 294 | 2026-10-19 |
| ZIBCAR | 57 | 30 | 302 | 282 | 2026-10-24 |
| ZNDITZ11 | 59 | 30 | 302 | 178 | 2026-10-24 |

## Lower minimum than stage 2

A branch fell more than 2 kJ/mol below its start (`energy_drop`), so the complex has a lower minimum than the stage-2 geometry; points past the drop are not exported.

- FEKRAO: angle_S1-Zn-N3 neg step 2 at -2.508 kJ/mol; angle_S1-Zn-N4 neg step 3 at -2.483 kJ/mol; angle_S2-Zn-N3 neg step 2 at -2.345 kJ/mol; twist_S1-S2-N3-N4 neg step 3 at -2.489 kJ/mol; tilt_Zn-S2-C32-C38 neg step 9 at -3.29 kJ/mol
- GAKKUY: angle_S2-Zn-S3 neg step 9 at -4.906 kJ/mol
- GIXTAL: angle_N6-Zn-N7 pos step 6 at -4.886 kJ/mol
- ICAVAK: angle_S1-Zn-N2 pos step 8 at -2.533 kJ/mol
- ICUCIT: angle_N2-Zn-N3 pos step 8 at -10.556 kJ/mol
- KAKYAW: angle_N29-Zn-N50 pos step 3 at -10.288 kJ/mol
- NAMSOJ: bond_Zn-N1 neg step 2 at -16.558 kJ/mol; bond_Zn-S4 neg step 3 at -15.584 kJ/mol; angle_N1-Zn-N2 pos step 3 at -15.459 kJ/mol; angle_N1-Zn-N3 neg step 2 at -16.738 kJ/mol; angle_N1-Zn-S4 neg step 1 at -16.718 kJ/mol; angle_N2-Zn-S4 neg step 3 at -15.969 kJ/mol; angle_N2-Zn-S4 pos step 4 at -16.305 kJ/mol; angle_N3-Zn-S4 pos step 1 at -16.76 kJ/mol; twist_N1-N2-N3-S4 neg step 1 at -16.653 kJ/mol; tilt_Zn-N1-C19-C24 pos step 3 at -4.152 kJ/mol; tilt_Zn-S4-C5-O7 neg step 8 at -15.792 kJ/mol
- OJELOE: angle_S4-Zn-N100 pos step 4 at -2.003 kJ/mol; twist_S3-S4-N100-S5 neg step 7 at -2.511 kJ/mol
- TARNIJ: angle_S1-Zn-S2 neg step 8 at -2.476 kJ/mol
- UFUROC: bond_Zn-S1 neg step 3 at -2.655 kJ/mol; bond_Zn-S2 pos step 2 at -3.299 kJ/mol; bond_Zn-S3 neg step 1 at -3.613 kJ/mol; bond_Zn-S4 pos step 3 at -3.064 kJ/mol; angle_S1-Zn-S2 neg step 1 at -3.621 kJ/mol; angle_S1-Zn-S3 pos step 1 at -3.152 kJ/mol; angle_S1-Zn-S4 neg step 1 at -2.971 kJ/mol; angle_S2-Zn-S3 pos step 3 at -3.3 kJ/mol; angle_S2-Zn-S4 neg step 1 at -3.606 kJ/mol; angle_S3-Zn-S4 pos step 2 at -3.615 kJ/mol; twist_S1-S2-S3-S4 neg step 1 at -3.334 kJ/mol; tilt_Zn-S2-C12-O11 neg step 3 at -3.564 kJ/mol; tilt_Zn-S3-C18-C19 neg step 2 at -3.22 kJ/mol; tilt_Zn-S4-C24-O23 neg step 2 at -3.615 kJ/mol
- WIGBIX: angle_S20-Zn-N39 pos step 7 at -2.309 kJ/mol
- WUJZOS: bond_Zn-N4 pos step 5 at -4.526 kJ/mol; angle_N1-Zn-N6 neg step 5 at -2.591 kJ/mol; angle_N1-Zn-N9 pos step 2 at -5.665 kJ/mol; angle_N4-Zn-N6 neg step 2 at -5.635 kJ/mol; twist_N1-N4-N6-N9 neg step 3 at -5.18 kJ/mol; tilt_Zn-N1-C11-C43 neg step 4 at -5.43 kJ/mol; tilt_Zn-N4-C43-C11 neg step 5 at -4.602 kJ/mol; tilt_Zn-N6-C69-C101 pos step 9 at -4.898 kJ/mol; tilt_Zn-N9-C75-C74 neg step 3 at -5.495 kJ/mol
- XAJQAB: angle_N22-Zn-N69 neg step 9 at -21.073 kJ/mol
- XIXTEG: bond_Zn-N5 pos step 4 at -6.315 kJ/mol; bond_Zn-N9 pos step 4 at -6.38 kJ/mol; angle_S2-Zn-S4 pos step 3 at -6.376 kJ/mol; angle_S2-Zn-N5 neg step 3 at -4.432 kJ/mol; angle_S4-Zn-N5 pos step 6 at -3.541 kJ/mol; angle_S4-Zn-N9 neg step 3 at -4.737 kJ/mol; angle_N5-Zn-N9 neg step 2 at -6.213 kJ/mol; twist_S2-N5-S4-N9 neg step 8 at -3.992 kJ/mol; tilt_Zn-S4-C54-N10 pos step 10 at -6.57 kJ/mol; tilt_Zn-N5-C26-C27 pos step 4 at -4.229 kJ/mol; tilt_Zn-N9-C49-C50 pos step 4 at -4.473 kJ/mol
- ZNDITZ11: bond_Zn-N3 pos step 4 at -2.047 kJ/mol; angle_S1-Zn-S2 pos step 4 at -2.225 kJ/mol; angle_S1-Zn-N3 neg step 2 at -2.201 kJ/mol; angle_S1-Zn-N7 pos step 2 at -2.522 kJ/mol; angle_S2-Zn-N3 pos step 1 at -2.373 kJ/mol; tilt_Zn-S1-C11-N4 pos step 7 at -2.373 kJ/mol; tilt_Zn-S2-C34-N8 neg step 6 at -2.658 kJ/mol; tilt_Zn-S2-C34-N8 pos step 5 at -2.413 kJ/mol

## Finished but not exported

No branch start passes validation, so no point is usable as defined (for example a non-donor atom within 2.6 A of Zn at the stage-2 minimum).

- GECLUZ: all 29 branches finished; branch starts fail validation (new_contact 29)
- KECGEI: all 30 branches finished; branch starts fail validation (new_contact 30)
- KERJOI: all 29 branches finished; branch starts fail validation (shell 29)
- KUBVEJ: all 30 branches finished; branch starts fail validation (new_contact 30)
- LIVNAG: all 30 branches finished; branch starts fail validation (new_contact 30)
- OGUGON: all 30 branches finished; branch starts fail validation (new_contact 30)
