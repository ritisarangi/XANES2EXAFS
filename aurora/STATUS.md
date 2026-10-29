# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 20:52 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8139 done, 768 started (running/stopped/failed), 1266 continuations ready, 2 not started, 10175 total
queue main: 1106 of 42898 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation:  available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8985662 | zn_main | capacity | 16 | 06:00 | R | 00:46 |
| 8986279 | zn_main | capacity | 16 | 06:00 | R | 00:46 |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 501 finished (498 copied back to Aurora), 91 running, 68 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1408 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 8 / 30 |
| CAPWIB | 3 / 30 |
| CATZUS10 | 12 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 28 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 0 / 30 |
| LAJGIM | 0 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| UYORAE | 0 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-29 20:26:31] scans/CATZUS10/tilt_Zn-N58-C64-H113_pos finished (job 60483068)
[2026-10-29 20:28:34] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-10-29 20:28:34] status: 162 jobs queued/running, 498 branches finished (498 back on Aurora), 0 need review
[2026-10-29 20:40:09] scans/BUNNII/angle_S128-Zn-S134_pos finished (job 60481447)
[2026-10-29 20:40:41] scans/CATZUS10/tilt_Zn-N22-C28-H87_pos finished (job 60482115)
[2026-10-29 20:41:14] scans/CAPWIB/bond_Zn-N14_neg finished (job 60502437)
[2026-10-29 20:41:14] status: 159 jobs queued/running, 501 branches finished (498 back on Aurora), 0 need review
[2026-10-29 20:52:14] status: 159 jobs queued/running, 501 branches finished (498 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 182 of 1875 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 18:28:01] publish: publish: no newly finished complexes 
prioritize main: 182 of 1875 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 18:43:54] STATUS.md pushed
prioritize main: 182 of 1875 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1107 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1106 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
