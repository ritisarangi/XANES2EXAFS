#!/bin/bash
# Move unfinished redox work onto the current, requeue-safe job script.
# Run from the project folder:  bash <repo>/redox/resubmit_remaining.sh
# 1. Cancels only the PENDING zn_redox tasks (running tasks keep going).
# 2. Lists every complex in redox/jobs_*.txt that has neither finished nor is running now.
# 3. Submits those through submit_redox.sh (preemptable QOS, resume on requeue).
# A complex that is running now is left out, so no folder ever has two ORCA runs at once.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p logs
scancel -u "$USER" -n zn_redox -t PENDING || true
sleep 2
running=$(squeue -u "$USER" -n zn_redox -t RUNNING,COMPLETING -h -o "%F %K" | while read a k; do
  f="logs/redox_${a}_${k}.log"; [ -f "$f" ] && grep -oE "^[A-Z0-9]+ (primary|fallback) start" "$f" | tail -1 | cut -d' ' -f1
done | sort -u)
done_ok() { grep -q "ORCA TERMINATED NORMALLY" "$1" 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" "$1"; }
cat redox/jobs_*.txt | grep . | sort -u | while read r; do
  done_ok "redox/primary/$r/$r.out" && continue
  done_ok "redox/fallback/$r/$r.out" && continue
  echo "$running" | grep -qx "$r" && continue
  echo "$r"
done > redox/jobs_remaining.txt
echo "running now (left alone): $(echo "$running" | grep -c . || true)"
echo "to submit: $(grep -c . redox/jobs_remaining.txt || true)"
[ -s redox/jobs_remaining.txt ] && bash "$HERE/submit_redox.sh" redox/jobs_remaining.txt
