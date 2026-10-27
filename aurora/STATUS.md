# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 00:43 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7473 done, 384 started (running/stopped/failed), 2207 continuations ready, 111 not started, 10175 total
queue main: 2072 of 40005 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,728.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | R | 01:48 |
| 8970790 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 295 finished (294 copied back to Aurora), 245 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 69
1008 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 14 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 26 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 17 / 30 |
| RAYBIC | 16 / 30 |
| REJBUD | 29 / 30 |
| SONROE | 13 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 26 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 00:14:31] scans/WORMAR/angle_N4-Zn-N8_neg finished (job 60241158)
[2026-10-27 00:14:31] status: 248 jobs queued/running, 292 branches finished (288 back on Aurora), 0 need review
[2026-10-27 00:26:02] scans/NAMSOJ/angle_N2-Zn-S4_pos finished (job 60240128)
[2026-10-27 00:26:34] scans/WORMAR/angle_S2-Zn-N4_neg finished (job 60241190)
[2026-10-27 00:30:12] copied 6 finished branches back to Aurora: SUCCEEDED
[2026-10-27 00:30:12] status: 246 jobs queued/running, 294 branches finished (294 back on Aurora), 0 need review
[2026-10-27 00:41:39] scans/WORMAR/angle_N4-Zn-N8_pos finished (job 60241161)
[2026-10-27 00:41:39] status: 245 jobs queued/running, 295 branches finished (294 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 22:19:12] publish: publish: 1 complexes added (154 passing points), 0 not exported; 189 complexes published in total pushed: 61de745 Aurora results: 189 complexes published (2026-10-26 22:19) 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 22:45:22] STATUS.md pushed
prioritize main: 0 of 2083 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2078 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2073 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
