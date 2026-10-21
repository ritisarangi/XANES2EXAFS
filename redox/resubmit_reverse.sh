#!/bin/bash
# Resubmit reverse runs that stopped without finishing (killed, not requeued) or never started.
# Run from the project folder:  bash ../XANES2EXAFS/redox/resubmit_reverse.sh
# Skips complexes that finished, that are RUNNING or PENDING now, and those with a FAILED marker
# (those need a changed input, not a rerun). Requeued tasks resume from their last geometry.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
active=$(bash "$HERE/running_refs.sh")
done_ok() { grep -q "ORCA TERMINATED NORMALLY" "$1" 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" "$1"; }
: > redox/jobs_reverse_remaining.txt
nd=0; na=0; nf=0
for r in $(cat lists/reverse_*.txt | sort -u); do
  d=redox/reverse/$r
  if done_ok "$d/$r.out"; then nd=$((nd+1)); continue; fi
  if echo "$active" | grep -qx "$r"; then na=$((na+1)); continue; fi
  if [ -f "$d/FAILED" ]; then
    # jobs started before the preemption fix marked killed runs as FAILED; keep only real failures
    nt=$(ls $d/${r}_try*.out 2>/dev/null | wc -l)
    if grep -q "ORCA TERMINATED NORMALLY" "$d/$r.out" 2>/dev/null || [ "$nt" -ge 12 ]; then nf=$((nf+1)); continue; fi
    rm -f "$d/FAILED"; echo "$r: cleared a FAILED marker left by a killed run"
  fi
  echo "$r" >> redox/jobs_reverse_remaining.txt
done
echo "finished $nd, running or queued $na, FAILED $nf, to submit $(grep -c . redox/jobs_reverse_remaining.txt || true)"
[ -s redox/jobs_reverse_remaining.txt ] && MODE=reverse MAX=${MAX:-60} bash "$HERE/submit_redox.sh" redox/jobs_reverse_remaining.txt
exit 0
