#!/bin/bash
# Runs on every node of a farm job (started once per node by aurora/farm.pbs through mpiexec).
# Each 16-core slot pulls the next branch from the shared queue, runs ORCA pinned to its cores,
# and stops it before the walltime so restart.py can continue it from the last converged step.
# Environment from farm.pbs: WORK REPO QDIR JOB DEADLINE; optional MIN_START_MIN, SLOTS.
set -u
source "$REPO/sites/aurora.sh"
setup_env
ulimit -s unlimited
cd "$WORK" || exit 1
HOST=$(hostname -s)
MIN_START=$(( ${MIN_START_MIN:-45} * 60 ))   # do not start a branch with less time than this left

claim() {   # print the next task, or nothing when the queue is empty
  local n t
  exec 9>>"$QDIR/lock"
  flock 9
  n=$(cat "$QDIR/next")
  t=$(sed -n "$((n + 1))p" "$QDIR/tasks.txt")
  [ -n "$t" ] && echo $((n + 1)) > "$QDIR/next"
  flock -u 9
  exec 9>&-
  echo "$t"
}

slot() {
  local s=$1 cores=$2 seq=0 D mode out log pid why
  while :; do
    [ -e "$QDIR/STOP" ] || [ -e "$QDIR/stop_$JOB" ] && break
    [ $(( DEADLINE - $(date +%s) )) -lt $MIN_START ] && break
    D=$(claim)
    [ -n "$D" ] || break
    seq=$((seq + 1))
    if [ -e "$D/scan.out" ] || [ -e "$D/scan_cont.out" ]; then continue; fi   # already started elsewhere
    if [ -e "$D/scan_orig.inp" ]; then mode=scanr out=scan_cont.out; else mode=scan out=scan.out; fi
    log=$WORK/logs/${mode}_${JOB}_${HOST}_${s}_${seq}.log
    touch "$QDIR/active/${JOB}_${HOST}_${s}"
    echo "$D start $(date '+%F %T') on $HOST cores $cores" > "$log"
    ( cd "$D" && exec taskset -c "$cores" setsid "$ORCA/orca" scan.inp > "$out" 2>&1 ) &
    pid=$!     # setsid makes ORCA a session leader: the session holds orca, mpirun and all ranks
    why=
    while kill -0 $pid 2>/dev/null; do
      sleep 20
      if [ "$(date +%s)" -ge "$DEADLINE" ]; then why="DUE TO TIME LIMIT"
      elif [ -e "$QDIR/stop_$JOB" ]; then why="CANCELLED (tail cutoff)"
      else continue; fi
      pkill -TERM -s $pid 2>/dev/null; sleep 30; pkill -KILL -s $pid 2>/dev/null
      break
    done
    wait $pid 2>/dev/null
    # keep the output, per-step geometries and scan tables; drop wavefunction and scratch files
    ( cd "$D" && rm -f scan.gbw scan*.tmp scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null )
    if [ -n "$why" ]; then
      echo "$why" >> "$log"
    elif [ $mode = scanr ]; then
      python3 "$REPO/scans/restart.py" . --stitch "$D" >> "$log" 2>&1
    fi
    grep -q "ORCA TERMINATED NORMALLY" "$D/scan.out" 2>/dev/null || echo "$D ORCA did not terminate normally" >> "$log"
    echo "$D end $(date '+%F %T')" >> "$log"
    rm -f "$QDIR/active/${JOB}_${HOST}_${s}"
  done
}

i=0
for c in $SLOTS; do slot $i "$c" & i=$((i + 1)); done
wait
