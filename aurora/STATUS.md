# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-02 13:21 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10175 done, 0 started (running/stopped/failed), 0 continuations ready, 0 not started, 10175 total
queue main: 0 of 0 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,119.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|

## NERSC Perlmutter (big pool)

The 39 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 1170 finished (1170 copied back to Aurora), 0 running, 0 queued, 0 need review, 1170 total
stops at the 48 h limit so far: 201; failed runs: 93
1455 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 30 / 30 |
| CAWKIW | 30 / 30 |
| DIVKAW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 30 / 30 |
| FAZJAT | 30 / 30 |
| FEKQUH | 30 / 30 |
| FUXMAM | 30 / 30 |
| GIXSUE | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 30 / 30 |
| LOHZAM | 30 / 30 |
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
| UCOLON | 30 / 30 |
| UWAVOF | 30 / 30 |
| UYORAE | 30 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-02 12:07:08] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 12:17:11] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 12:27:14] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 12:37:18] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 12:47:22] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 12:57:25] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 13:07:28] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
[2026-11-02 13:17:31] status: 0 jobs queued/running, 1170 branches finished (1170 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-02 11:20:47] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
