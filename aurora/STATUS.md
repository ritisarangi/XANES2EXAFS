# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 03:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7707 done, 384 started (running/stopped/failed), 2069 continuations ready, 15 not started, 10175 total
queue main: 1992 of 40761 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | R | 01:02 |
| 8972593 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 449 finished (449 copied back to Aurora), 91 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 119; failed runs: 90
1247 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 22 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 28 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 29 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 29 / 30 |
| WIGBIX | 8 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 03:06:17] status: 93 jobs queued/running, 447 branches finished (447 back on Aurora), 0 need review
[2026-10-28 03:16:53] status: 93 jobs queued/running, 447 branches finished (447 back on Aurora), 0 need review
[2026-10-28 03:28:02] scans/RAYBIC/angle_N1-Zn-N3_pos finished (job 60360083)
[2026-10-28 03:28:02] status: 92 jobs queued/running, 448 branches finished (447 back on Aurora), 0 need review
[2026-10-28 03:39:17] cycle error: ('POST', 'https://transfer.api.globus.org/v0.10/transfer', 'Bearer', 502, 'ExternalError', "Error validating login to endpoint 'NERSC Perlmutter (6bdc7956-fc0f-4ad2-989c-7aa5ee643a79)', Error (connect)\nEndpoint: NERSC Perlmutter (6bdc7956-fc0f-4ad2-989c-7aa5ee643a79)\nServer: 128.55.64.33:443\nMess
[2026-10-28 03:50:56] scans/NONLEI/twist_N1-N3-N2-N4_pos finished (job 60359467)
[2026-10-28 03:52:43] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-28 03:52:43] status: 91 jobs queued/running, 449 branches finished (449 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-28 00:55:06] publish: publish: no newly finished complexes 
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 02:10:09] STATUS.md pushed
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
