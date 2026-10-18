#!/bin/bash
# Runs on every node of a farm job (started once per node by aurora/farm.pbs through mpiexec).
# Each slot (see slot_list in sites/aurora.sh) pulls the next branch from the shared queue, runs
# ORCA pinned to its cores, and stops it before the walltime so restart.py can continue it from
# the last converged step.
# Environment from farm.pbs: WORK REPO QDIR JOB DEADLINE, the layout settings of sites/aurora.sh,
# and optionally MIN_START_MIN.
set -u
source "$REPO/sites/aurora.sh"
setup_env
ulimit -s unlimited
cd "$WORK" || exit 1
HOST=$(hostname -s)
MIN_START=$(( ${MIN_START_MIN:-20} * 60 ))   # do not start a branch with less time than this left

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
  local s=$1 cores=$2 hbm=$3 seq=0 D mode out log pid why run mem
  mem=; [ "$HBM" = 1 ] && mem="numactl --preferred=$hbm"
  # each slot gets its own OpenMPI session and shared-memory directory: with many mpiruns per
  # node, shared ones collide and a rank dies with SIGBUS in btl_vader
  local ompi=/tmp/zn_ompi_${JOB}_$s; mkdir -p "$ompi"
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
    # parallel settings follow the slot; they do not change the chemistry
    sed -i -e "s/^%pal nprocs [0-9]* end/%pal nprocs $CORES end/" -e "s/^%maxcore [0-9]*/%maxcore $MAXCORE/" "$D/scan.inp"
    run=$WORK/$D
    if [ "$SCRATCH" = tmp ]; then run=/tmp/zn_${JOB}_$s; rm -rf "$run"; mkdir -p "$run"; cp "$D/scan.inp" "$run/"; fi
    # scan.out is written straight into $WORK, so a stopped branch can always be continued
    ( cd "$run" && export OMPI_MCA_orte_tmpdir_base="$ompi" OMPI_MCA_btl_vader_backing_directory="$ompi" \
        && exec taskset -c "$cores" setsid $mem "$ORCA/orca" scan.inp > "$WORK/$D/$out" 2>&1 ) &
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
    # keep the per-step geometries and scan tables; drop wavefunction and scratch files
    ( cd "$run" && rm -f scan.gbw scan*.tmp scan*.tmp.* scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null )
    if [ "$SCRATCH" = tmp ]; then
      find "$run" -maxdepth 1 -type f ! -name scan.inp ! -name '*.tmp*' ! -name '*.gbw' ! -name '*densities*' -exec cp -p {} "$D/" \;
      rm -rf "$run"
    fi
    # an MPI process killed by a signal, or mpirun failing to start, is an infrastructure failure,
    # not chemistry: tag it so restart.py continues the branch from its last converged step
    # (at most 2 retries)
    if [ -z "$why" ] && ! grep -q "ORCA TERMINATED NORMALLY" "$WORK/$D/$out" 2>/dev/null \
       && grep -qE "exited on signal|orte_init failed" "$WORK/$D/$out" 2>/dev/null && [ "$(ls "$D"/scan_try*.out 2>/dev/null | wc -l)" -lt 3 ]; then
      why="CANCELLED (MPI failure; retried)"
    fi
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
while read -r cl hb; do slot $i "$cl" "$hb" & i=$((i + 1)); done < <(slot_list)
wait

# Farms submitted before farm.pbs re-queued its own stopped branches: the head node does it here,
# a minute after its slots stop so the other nodes have tagged theirs (same lock as go.sh)
if [ -z "${FARM_REQUEUE:-}" ] && [ "$HOST" = "$(head -1 "$PBS_NODEFILE" | cut -d. -f1)" ]; then
  sleep 60
  pool=$(basename "$QDIR")
  if [ "$pool" = big ]; then export NATOMS_MIN=100 NATOMS_MAX=1000000; else export NATOMS_MIN=0 NATOMS_MAX=100; fi
  (
    flock 8
    echo "$(date '+%F %T') requeue after farm $JOB ($pool, from node.sh)"
    RESUME_PARTIAL=1 python3 "$REPO/scans/restart.py" . | tail -1
    python3 "$REPO/aurora/queue.py" add . scans/jobs_scan_full.txt "queue/$pool"
  ) 8>>"$WORK/.gosh.lock" >> "$WORK/logs/requeue_$JOB.log" 2>&1
fi
