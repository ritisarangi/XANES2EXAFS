#!/bin/bash
# Restart slow-converging redox optimisations with normal (not tight) convergence.
# Run from the project folder:  bash ../XANES2EXAFS/redox/loosen.sh GUCSED NONLEI
# For each complex: cancels its running Slurm task, continues from the last geometry
# (resume.py), switches TightOpt to Opt in REF.inp and REF_orig.inp (so a later requeue
# keeps the looser setting), and resubmits all of them in one array on the preemptable QOS.
# Frequencies are still computed after the optimisation.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
[ $# -gt 0 ] || { echo "give one or more complex names"; exit 1; }
for R in "$@"; do
  squeue -u "$USER" -n zn_redox -h -o "%i %F %K" | while read id a k; do
    grep -qE "^$R (primary|fallback) start" "logs/redox_${a}_${k}.log" 2>/dev/null && { echo "$R: cancelling task $id"; scancel "$id"; }
  done
done
sleep 20
: > redox/jobs_loosen.txt
for R in "$@"; do
  d=redox/primary/$R
  [ -d "$d" ] || { echo "$R: no folder $d"; continue; }
  (cd "$d" && rm -f FAILED && python3 "$HERE/resume.py" "$R" && sed -i 's/\bTightOpt\b/Opt/' "$R.inp" ${R}_orig.inp 2>/dev/null; grep -m1 '^!' "$R.inp")
  echo "$R" >> redox/jobs_loosen.txt
done
bash "$HERE/submit_redox.sh" redox/jobs_loosen.txt
