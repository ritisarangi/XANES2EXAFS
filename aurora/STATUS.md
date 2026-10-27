# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 08:46 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7608 done, 385 started (running/stopped/failed), 2129 continuations ready, 53 not started, 10175 total
queue main: 2011 of 40383 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,632.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8970790 | zn_main | capacity | 16 | 06:00 | R | 02:40 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 369 finished (369 copied back to Aurora), 138 running, 33 queued, 0 need review, 540 total
stops at the 48 h limit so far: 91; failed runs: 80
1104 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 27 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 24 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 28 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 9 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 25 / 30 |
| RAYBIC | 18 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 19 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 08:43:16] scans/WIGBIX/angle_S20-Zn-N45_pos stopped at the time limit (job 60241017); continues
[2026-10-27 08:43:49] scans/WIGBIX/angle_S20-Zn-N45_neg stopped at the time limit (job 60241014); continues
[2026-10-27 08:44:21] scans/SONROE/angle_N114-Zn-N115_pos stopped at the time limit (job 60240824); continues
[2026-10-27 08:44:53] scans/WIGBIX/angle_S1-Zn-N39_neg stopped at the time limit (job 60240973); continues
[2026-10-27 08:45:25] scans/WIGBIX/angle_S1-Zn-S20_neg stopped at the time limit (job 60240997); continues
[2026-10-27 08:46:34] submitted 16 jobs
[2026-10-27 08:48:51] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-27 08:48:51] status: 171 jobs queued/running, 369 branches finished (369 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-27 06:15:52] autopilot started (pid 1278214, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 1079b2f, accounts: isaac ModCon)
[2026-10-27 06:26:18] new farms go to project ModCon (43632 node-hours left)
prioritize main: 0 of 2019 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 06:40:49] publish: publish: no newly finished complexes 
[2026-10-27 06:52:49] STATUS.md pushed
prioritize main: 0 of 2019 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2019 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2015 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
