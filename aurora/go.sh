#!/bin/bash
# One command for the Zn scan production run on ALCF Aurora (CPU only, PBS).
#
#   bash XANES2EXAFS/aurora/go.sh setup  <scan_bundle.tar.gz>   unpack into $WORK, check ORCA/MPI
#   bash XANES2EXAFS/aurora/go.sh test                          1 node, 6 packed ORCA test runs (debug queue)
#   bash XANES2EXAFS/aurora/go.sh submit [REF ...]              continue stopped branches, queue the rest, submit a farm job
#   bash XANES2EXAFS/aurora/go.sh status                        jobs, branch states, validated points
#   bash XANES2EXAFS/aurora/go.sh drain                         farm jobs start no new branches (running ones finish)
#   bash XANES2EXAFS/aurora/go.sh export                        validate and pack passing geometries into scan_results.tar.gz
#
# Aurora has no per-core charging, so instead of Slurm arrays one PBS job ("farm") runs 6 ORCA
# jobs of 16 cores on each node and keeps them fed from a shared queue. Branches still running
# near the walltime are stopped and continued by the next 'submit' from their last converged step.
#
# Needs in the environment (put them in ~/.bashrc): ACCOUNT (ALCF project), ORCA_DIR, MPI_DIR, WORK.
# Options for submit: QUEUE (default capacity), NODES (16), HOURS (48), TAIL_FRAC (0.25, 0 = off),
# MIN_START_MIN (45: no new branch with less time left).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(dirname "$HERE")
WORK=${WORK:?set WORK to the run folder on /lus/flare}
cmd=${1:-status}

need() { for v in ACCOUNT ORCA_DIR MPI_DIR; do [ -n "${!v}" ] || { echo "set $v first (see the header of this script)"; exit 1; }; done; }
active_jobs() { qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_farm/ && $10 ~ /[QRHE]/ {sub(/\..*/, "", $1); print $1}'; }

farm() {  # farm <queue dir> <queue> <nodes> <hours> [extra -v settings]
  local qd=$1 q=$2 n=$3 h=$4 extra=${5:-}
  local wt=$(printf '%02d:%02d:00' $((h)) 0)
  source "$REPO/sites/aurora.sh"
  qsub $QSUB_SITE -q "$q" -l select="$n" -l walltime="$wt" -o "$WORK/logs/" \
       -v "WORK=$WORK,REPO=$REPO,QDIR=$qd,HOURS=$h,TAIL_FRAC=${TAIL_FRAC:-0.25},MIN_START_MIN=${MIN_START_MIN:-45}${extra}" \
       "$HERE/farm.pbs"
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
  id=$(MIN_START_MIN=1 TAIL_FRAC=0 farm "$WORK/test/queue" debug 1 1 ",TEST=1,MARGIN_MIN=30")
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
  if [ -n "$act" ]; then
    echo "farm jobs already queued or running ($(echo $act)); adding one more on the same queue"
  else
    python3 "$HERE/queue.py" mark-lost .
    python3 "$REPO/scans/restart.py" . | tail -2
    python3 "$HERE/queue.py" build . scans/jobs_scan_full.txt queue "$@"
    rm -f queue/STOP
  fi
  left=$(( $(grep -c . queue/tasks.txt) - $(cat queue/next) ))
  [ $left -gt 0 ] || { echo "nothing left to run"; exit 0; }
  Q=${QUEUE:-capacity} N=${NODES:-16} H=${HOURS:-48}
  id=$(farm "$WORK/queue" "$Q" "$N" "$H")
  echo "$(date '+%F %T') farm $id queue=$Q nodes=$N hours=$H account=$ACCOUNT tasks_left=$left" | tee -a logs/submissions.txt
  ;;
status)
  cd "$WORK"
  qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_/' || true
  [ -f queue/tasks.txt ] && echo "queue: $(( $(grep -c . queue/tasks.txt) - $(cat queue/next) )) of $(grep -c . queue/tasks.txt) not yet handed out; $(ls queue/active 2>/dev/null | wc -l) ORCA runs active"
  [ -f scans/jobs_scan_full.txt ] && python3 "$HERE/queue.py" status . scans/jobs_scan_full.txt
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt 2>/dev/null | head -4
  ;;
drain)
  touch "$WORK/queue/STOP"
  echo "farm jobs will start no new branches; running ones finish or stop at the walltime. 'submit' clears this."
  ;;
export)
  cd "$WORK"
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt > /dev/null
  python3 "$REPO/scans/export_points.py" . lists/scan_full.txt
  echo "send $WORK/scan_results.tar.gz back to Riti"
  ;;
*) echo "commands: setup <bundle> | test | submit [REF ...] | status | drain | export"; exit 1 ;;
esac
