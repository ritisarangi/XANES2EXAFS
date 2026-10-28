# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 23:24 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7962 done, 0 started (running/stopped/failed), 2207 continuations ready, 6 not started, 10175 total
queue main: 2152 of 42267 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,150.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8978755 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 479 finished (479 copied back to Aurora), 60 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 123; failed runs: 91
1340 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 29 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 25 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| WIGBIX | 27 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 22:49:49] status: 62 jobs queued/running, 478 branches finished (478 back on Aurora), 0 need review
[2026-10-28 23:00:55] scans/WIGBIX/angle_S20-Zn-N45_neg finished (job 60361259)
[2026-10-28 23:00:55] status: 61 jobs queued/running, 479 branches finished (478 back on Aurora), 0 need review
[2026-10-28 23:11:20] status: 61 jobs queued/running, 479 branches finished (478 back on Aurora), 0 need review
[2026-10-28 23:22:19] scans/BUNNII/angle_S132-Zn-S134_pos stopped at the time limit (job 60341606); continues
[2026-10-28 23:22:22] submitted 1 jobs
[2026-10-28 23:23:16] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-28 23:23:16] status: 61 jobs queued/running, 479 branches finished (479 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 21:39:45] STATUS.md pushed
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 23:13:04] publish: publish: no newly finished complexes 
```
