# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 18:02 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7097 done, 0 started (running/stopped/failed), 2781 continuations ready, 297 not started, 10175 total
queue main: 2600 of 39624 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,850.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 65 finished (65 copied back to Aurora), 475 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 18
284 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 0 / 30 |
| NAMSOJ | 2 / 30 |
| NECTOG | 0 / 30 |
| NONLEI | 0 / 30 |
| OJEKUJ | 21 / 30 |
| OJELOE | 1 / 30 |
| RAYBIC | 3 / 30 |
| REJBUD | 4 / 30 |
| SONROE | 3 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 27 / 30 |

Last driver actions:

```
[2026-10-25 17:35:42] status: 477 jobs queued/running, 63 branches finished (62 back on Aurora), 0 need review
[2026-10-25 17:48:16] scans/BUNNII/angle_S132-Zn-S134_pos FAILED (job 60239238, state completed): ['scans/BUNNII/angle_S132-Zn-S134_pos end 2026-10-25 10:35:27']
[2026-10-25 17:48:48] scans/OJEKUJ/angle_S1-Zn-S4_pos finished (job 60240449)
[2026-10-25 17:49:21] scans/WIGBIX/bond_Zn-N39_neg finished (job 60241022)
[2026-10-25 17:49:24] submitted 1 jobs
[2026-10-25 17:49:24] status: 475 jobs queued/running, 65 branches finished (62 back on Aurora), 0 need review
[2026-10-25 18:03:25] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-10-25 18:03:25] status: 475 jobs queued/running, 65 branches finished (65 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-25 15:28:40] publish: publish: no newly finished complexes 
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 15:52:34] STATUS.md pushed
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
