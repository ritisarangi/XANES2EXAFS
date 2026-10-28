# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 10:43 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7812 done, 0 started (running/stopped/failed), 2352 continuations ready, 11 not started, 10175 total
queue main: 2285 of 41520 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,343.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8976721 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8976814 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 463 finished (462 copied back to Aurora), 77 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 120; failed runs: 91
1284 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 23 / 30 |
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
| WIGBIX | 16 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 09:46:33] scans/GUFHEU/tilt_Zn-S2-C33-C41_pos finished (job 60364814)
[2026-10-28 09:46:33] status: 78 jobs queued/running, 462 branches finished (457 back on Aurora), 0 need review
[2026-10-28 09:59:55] cycle error: ('POST', 'https://transfer.api.globus.org/v0.10/transfer', 'Bearer', 502, 'ExternalError', "Error validating login to endpoint 'alcf#dtn_flare (f39a7a0f-5bfc-46ce-9615-ba9f8592814f)', Error (connect)\nEndpoint: alcf#dtn_flare (f39a7a0f-5bfc-46ce-9615-ba9f8592814f)\nServer: 140.221.68.113:443\nMessag
[2026-10-28 10:13:35] copied 5 finished branches back to Aurora: SUCCEEDED
[2026-10-28 10:13:35] status: 78 jobs queued/running, 462 branches finished (462 back on Aurora), 0 need review
[2026-10-28 10:24:07] status: 78 jobs queued/running, 462 branches finished (462 back on Aurora), 0 need review
[2026-10-28 10:35:09] scans/WIGBIX/twist_S1-S20-N39-N45_pos finished (job 60361687)
[2026-10-28 10:35:09] status: 77 jobs queued/running, 463 branches finished (462 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-28 10:12:52] STATUS.md pushed
[2026-10-28 10:23:15] farm 8972593 (zn_main) ended: farm 8972593 done 2026-10-28 10:09:33; queue next 39235 of 41520
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8976721 8976814): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2285 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-28 10:36:42] autopilot started (pid 3343153, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 3f10a92, accounts: isaac ModCon)
[2026-10-28 10:40:14] new farms go to project ModCon (43343 node-hours left)
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 10:43:53] publish: publish: 3 complexes added (809 passing points), 0 not exported; 212 complexes published in total pushed: 7695bd0 Aurora results: 212 complexes published (2026-10-28 10:43) 
```
