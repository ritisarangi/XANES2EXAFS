# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 22:03 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10155 done, 0 started (running/stopped/failed), 20 continuations ready, 0 not started, 10175 total
queue main: 0 of 45552 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,318.4 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9024268 | zn_main | capacity | 16 | 06:00 | H | -- |
| 9027818 | zn_main | capacity | 16 | 06:00 | H | -- |

## NERSC Perlmutter (big pool)

The 39 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 1151 finished (1150 copied back to Aurora), 19 running, 0 queued, 0 need review, 1170 total
stops at the 48 h limit so far: 201; failed runs: 93
1455 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 30 / 30 |
| CAWKIW | 30 / 30 |
| DIVKAW | 25 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 30 / 30 |
| FAZJAT | 27 / 30 |
| FEKQUH | 28 / 30 |
| FUXMAM | 30 / 30 |
| GIXSUE | 28 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 30 / 30 |
| LOHZAM | 29 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| QISJUA | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 30 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 30 / 30 |
| TEYSOG | 30 / 30 |
| TIFNUU | 30 / 30 |
| UCOLON | 27 / 30 |
| UWAVOF | 30 / 30 |
| UYORAE | 27 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 21:28:08] scans/GIXSUE/angle_N5-Zn-N9_neg finished (job 60653939)
[2026-11-01 21:28:08] status: 21 jobs queued/running, 1149 branches finished (1148 back on Aurora), 0 need review
[2026-11-01 21:38:51] scans/LOHZAM/angle_N37-Zn-N38_neg finished (job 60653942)
[2026-11-01 21:38:51] status: 20 jobs queued/running, 1150 branches finished (1148 back on Aurora), 0 need review
[2026-11-01 21:50:32] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-11-01 21:50:32] status: 20 jobs queued/running, 1150 branches finished (1150 back on Aurora), 0 need review
[2026-11-01 22:01:16] scans/UCOLON/angle_S4-Zn-N6_neg finished (job 60653957)
[2026-11-01 22:01:16] status: 19 jobs queued/running, 1151 branches finished (1150 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 18:55:27] publish: publish: no newly finished complexes 
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 19:59:09] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
