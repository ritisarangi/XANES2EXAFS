#!/bin/bash
# One command for the Zn scan production run on ALCF Aurora (CPU only, PBS).
#
#   bash XANES2EXAFS/aurora/go.sh setup  <scan_bundle.tar.gz>   unpack into $WORK, check ORCA/MPI
#   bash XANES2EXAFS/aurora/go.sh test                          1 node, 6 packed ORCA test runs (debug queue)
#   bash XANES2EXAFS/aurora/go.sh submit [REF ...]              continue stopped branches, queue the rest, submit a farm job
#   bash XANES2EXAFS/aurora/go.sh status                        jobs, branch states, validated points
#   bash XANES2EXAFS/aurora/go.sh watch [seconds]               one progress line every 300 s (or the given interval)
#   bash XANES2EXAFS/aurora/go.sh drain                         farm jobs start no new branches (running ones finish)
#   bash XANES2EXAFS/aurora/go.sh export                        validate and pack passing geometries into scan_results.tar.gz
#
# Aurora has no per-core charging, so instead of Slurm arrays one PBS job ("farm") runs several
# pinned ORCA jobs on each node and keeps them fed from a shared queue. Branches still running
# near the walltime are stopped and continued by the next 'submit' from their last converged step.
#
# Two pools with separate queues and farms: POOL=main (default; complexes below BIG_ATOMS=100
# atoms, CORES=4) and POOL=big (BIG_ATOMS and up, CORES=8). Small ORCA jobs give the most
# node throughput; the large complexes get more cores so their branches do not trail for days.
#
# Needs in the environment (put them in ~/.bashrc): ACCOUNT (ALCF project), ORCA_DIR, MPI_DIR, WORK.
# Options for submit: QUEUE (default capacity), NODES (16), HOURS (48), TAIL_FRAC (0.25, 0 = off),
# MIN_START_MIN (20: no new branch with less time left), and the layout settings CORES, HT, HBM,
# MAXCORE, SCRATCH described in sites/aurora.sh.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(dirname "$HERE")
WORK=${WORK:?set WORK to the run folder on /lus/flare}
cmd=${1:-status}
POOL=${POOL:-main} BIG_ATOMS=${BIG_ATOMS:-100}
case "$POOL" in
  main) export CORES=${CORES:-4} NATOMS_MIN=0 NATOMS_MAX=$BIG_ATOMS ;;
  big)  export CORES=${CORES:-8} NATOMS_MIN=$BIG_ATOMS NATOMS_MAX=1000000 ;;
  *) echo "POOL is main or big"; exit 1 ;;
esac
QD=queue/$POOL

need() { for v in ACCOUNT ORCA_DIR MPI_DIR; do [ -n "${!v}" ] || { echo "set $v first (see the header of this script)"; exit 1; }; done; }
all_farm_jobs() { qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_(main|big)$/ && $10 ~ /[QRHE]/ {sub(/\..*/, "", $1); print $1}'; }
active_jobs() { qstat -u "$USER" 2>/dev/null | awk -v n="zn_$POOL" '$4 == n && $10 ~ /[QRHE]/ {sub(/\..*/, "", $1); print $1}'; }

farm() {  # farm <job name> <queue dir> <queue> <nodes> <hours> [extra -v settings]
  local name=$1 qd=$2 q=$3 n=$4 h=$5 extra=${6:-}
  local wt=$(printf '%02d:00:00' "$h") snap=$WORK/.repo/$(date +%Y%m%d_%H%M%S)
  # jobs run from a frozen copy of the scripts on /lus/flare: a later git pull cannot change a
  # queued or running farm, and the job does not depend on the home file system
  mkdir -p "$snap" && cp -r "$REPO/aurora" "$REPO/scans" "$REPO/sites" "$snap/"
  source "$snap/sites/aurora.sh"
  qsub $QSUB_SITE -N "$name" -q "$q" -l select="$n" -l walltime="$wt" -o "$WORK/logs/" \
       -v "WORK=$WORK,REPO=$snap,QDIR=$qd,HOURS=$h,ACCOUNT=$ACCOUNT,ORCA_DIR=$ORCA_DIR,MPI_DIR=$MPI_DIR,CORES=$CORES,HT=$HT,HBM=$HBM,MAXCORE=$MAXCORE,SCRATCH=$SCRATCH,TAIL_FRAC=${TAIL_FRAC:-0.25},MIN_START_MIN=${MIN_START_MIN:-20}${extra}" \
       "$snap/aurora/farm.pbs"
}

case "$cmd" in
setup)
  need
  B=${2:?give the path to scan_bundle.tar.gz}
  mkdir -p "$WORK/logs" && tar -xzf "$B" -C "$WORK"
  [ -x "$ORCA_DIR/orca" ] || { echo "no orca binary in $ORCA_DIR"; exit 1; }
  [ -x "$MPI_DIR/bin/mpirun" ] || { echo "no mpirun in $MPI_DIR/bin"; exit 1; }
  echo "unpacked to $WORK; $(wc -l < "$WORK/lists/scan_full.txt") complexes in lists/scan_full.txt"
  echo "next:  bash $HERE/go.sh test"
  ;;
test)
  need
  mkdir -p "$WORK/logs" "$WORK/test/queue"
  : > "$WORK/test/queue/tasks.txt"
  for i in 1 2 3 4 5 6; do
    d=$WORK/test/t$i
    rm -rf "$d" && mkdir -p "$d"
    # benzene opt + analytic freq: a few minutes on 16 cores, long enough to see core placement
    printf '! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) Opt Freq TightSCF\n%%pal nprocs 16 end\n%%maxcore 3000\n* xyz 0 1\nC 0.000 1.396 0\nC 1.209 0.698 0\nC 1.209 -0.698 0\nC 0.000 -1.396 0\nC -1.209 -0.698 0\nC -1.209 0.698 0\nH 0.000 2.480 0\nH 2.148 1.240 0\nH 2.148 -1.240 0\nH 0.000 -2.480 0\nH -2.148 -1.240 0\nH -2.148 1.240 0\n*\n' > "$d/scan.inp"
    echo "test/t$i" >> "$WORK/test/queue/tasks.txt"
  done
  echo 0 > "$WORK/test/queue/next"
  id=$(MIN_START_MIN=1 TAIL_FRAC=0 farm zn_test "$WORK/test/queue" debug 1 1 ",TEST=1,MARGIN_MIN=30")
  echo "test job $id submitted (6 benzene opt+freq runs packed on one node)."
  echo "when it has finished:  grep -c 'TERMINATED NORMALLY' $WORK/test/t*/scan.out   (expect 6 x 1)"
  echo "                       cat $WORK/logs/test_placement_${id%%.*}.txt             (6 disjoint 16-core groups)"
  ;;
submit)
  need
  shift
  cd "$WORK"
  mkdir -p logs scans
  [ -f scans/jobs_scan_full.txt ] || python3 "$REPO/scans/make_scans.py" . lists/scan_full.txt | tail -3
  act=$(active_jobs)
  # logs of branches whose job is gone without an end line are tagged as cancelled (never those of
  # any queued or running farm), then restart.py prepares every stopped branch for continuation;
  # neither touches a branch that is running
  python3 "$HERE/queue.py" mark-lost . $(all_farm_jobs)
  # interrupted steps restart from their last optimisation geometry (RESUME_PARTIAL=0: from the last converged step)
  RESUME_PARTIAL=${RESUME_PARTIAL:-1} python3 "$REPO/scans/restart.py" . | tail -2
  if [ -n "$act" ]; then
    echo "$POOL farm jobs already queued or running ($(echo $act)): continuations go to the front of the live queue"
    python3 "$HERE/queue.py" add . scans/jobs_scan_full.txt "$QD"
  else
    python3 "$HERE/queue.py" build . scans/jobs_scan_full.txt "$QD" "$@"
    rm -f "$QD/STOP"
  fi
  left=$(( $(grep -c . "$QD/tasks.txt") - $(cat "$QD/next") ))
  [ $left -gt 0 ] || { echo "nothing left to run"; exit 0; }
  [ "${NODES:-16}" = 0 ] && { echo "NODES=0: queue updated, no farm submitted"; exit 0; }
  Q=${QUEUE:-capacity} N=${NODES:-16} H=${HOURS:-48}
  id=$(farm "zn_$POOL" "$WORK/$QD" "$Q" "$N" "$H")
  echo "$(date '+%F %T') farm $id pool=$POOL cores=$CORES queue=$Q nodes=$N hours=$H account=$ACCOUNT tasks_left=$left" | tee -a logs/submissions.txt
  ;;
status)
  cd "$WORK"
  qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_/' || true
  for qd in queue/*/; do [ -f "$qd/tasks.txt" ] && echo "queue $(basename "$qd"): $(( $(grep -c . "$qd/tasks.txt") - $(cat "$qd/next") )) of $(grep -c . "$qd/tasks.txt") not yet handed out; $(ls "$qd/active" 2>/dev/null | wc -l) ORCA runs active"; done
  [ -f scans/jobs_scan_full.txt ] && python3 "$HERE/queue.py" status . scans/jobs_scan_full.txt
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt 2>/dev/null | head -4
  ;;
watch)
  # one line every N seconds (default 300): farm jobs, busy ORCA slots, queue left, branch states
  cd "$WORK"
  while :; do
    j=$(qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_(main|big)$/ {n[$10]++; if ($10 == "R") nd += $6} END {printf "%dR/%dQ jobs, %d nodes", n["R"], n["Q"], nd}')
    q=$(for qd in queue/*/; do [ -f "$qd/tasks.txt" ] && printf '%s %d queued, %d running; ' "$(basename "$qd")" $(( $(grep -c . "$qd/tasks.txt") - $(cat "$qd/next") )) "$(ls "$qd/active" | wc -l)"; done)
    b=$(python3 "$HERE/queue.py" status . scans/jobs_scan_full.txt 2>/dev/null | sed 's/^branches: //; s/ (running\/stopped\/failed)//')
    echo "[$(date '+%F %T')] $j | $q| $b"
    sleep "${2:-300}"
  done
  ;;
drain)
  touch "$WORK/$QD/STOP"
  echo "$POOL farm jobs will start no new branches; running ones finish or stop at the walltime. 'submit' clears this."
  ;;
export)
  cd "$WORK"
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt > /dev/null
  python3 "$REPO/scans/export_points.py" . lists/scan_full.txt
  echo "send $WORK/scan_results.tar.gz back to Riti"
  ;;
*) echo "commands: setup <bundle> | test | submit [REF ...] | status | drain | export"; exit 1 ;;
esac
