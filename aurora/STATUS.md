# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 18:42 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8134 done, 0 started (running/stopped/failed), 2039 continuations ready, 2 not started, 10175 total
queue main: 1875 of 42898 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,923.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8985662 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8986279 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 494 finished (494 copied back to Aurora), 67 running, 99 queued, 0 need review, 660 total
stops at the 48 h limit so far: 172; failed runs: 91
1402 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 7 / 30 |
| CAPWIB | 0 / 30 |
| CATZUS10 | 9 / 30 |
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
[2026-10-29 17:56:41] scans/CATZUS10/twist_N4-N22-N40-N58_pos finished (job 60483073)
[2026-10-29 17:56:41] status: 167 jobs queued/running, 493 branches finished (492 back on Aurora), 0 need review
[2026-10-29 18:08:15] scans/CATZUS10/tilt_Zn-N40-C46-H100_pos finished (job 60482756)
[2026-10-29 18:09:43] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-29 18:09:43] status: 166 jobs queued/running, 494 branches finished (494 back on Aurora), 0 need review
[2026-10-29 18:20:48] status: 166 jobs queued/running, 494 branches finished (494 back on Aurora), 0 need review
[2026-10-29 18:31:49] status: 166 jobs queued/running, 494 branches finished (494 back on Aurora), 0 need review
[2026-10-29 18:42:52] status: 166 jobs queued/running, 494 branches finished (494 back on Aurora), 0 need review
```

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
[2026-10-29 18:05:39] submitting main capacity farm on ModCon, 6 h (queue 1875 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8985662): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1875 pending now)
2026-10-29 18:26:20 farm 8986279.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1875
prioritize main: 182 of 1875 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 18:28:01] publish: publish: no newly finished complexes 
prioritize main: 182 of 1875 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
