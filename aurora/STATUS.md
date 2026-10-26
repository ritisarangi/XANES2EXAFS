# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 11:29 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7304 done, 0 started (running/stopped/failed), 2625 continuations ready, 246 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,730.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 138 finished (137 copied back to Aurora), 402 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 47
748 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 9 / 30 |
| NAMSOJ | 12 / 30 |
| NECTOG | 13 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 28 / 30 |
| OJELOE | 5 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 16 / 30 |
| SONROE | 10 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 29 / 30 |

Last driver actions:

```
[2026-10-26 11:06:20] scans/NECTOG/tilt_Zn-N4-C8-C11_neg finished (job 60252779)
[2026-10-26 11:06:52] scans/REJBUD/bond_Zn-S4_pos finished (job 60280631)
[2026-10-26 11:07:24] scans/WUJZOS/tilt_Zn-N9-C75-C74_pos finished (job 60241288)
[2026-10-26 11:11:12] copied 5 finished branches back to Aurora: SUCCEEDED
[2026-10-26 11:11:12] status: 403 jobs queued/running, 137 branches finished (137 back on Aurora), 0 need review
[2026-10-26 11:23:16] scans/NAMSOJ/tilt_Zn-N3-C77-C82_pos finished (job 60240179)
[2026-10-26 11:23:16] status: 402 jobs queued/running, 138 branches finished (137 back on Aurora), 0 need review
[2026-10-26 11:34:46] status: 402 jobs queued/running, 138 branches finished (137 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 09:34:56] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 10:02:41] publish: publish: no newly finished complexes 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
