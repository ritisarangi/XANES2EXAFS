#!/bin/bash
# One-screen status for the Zn project. Run from the project folder on S3DF:
#   bash ../XANES2EXAFS/status.sh
REPO=$(cd "$(dirname "$0")" && pwd)
cd "${1:-.}"
echo "== queue (pending array tasks counted one by one) =="
squeue -u "$USER" -h -r -o "%.10j %.8T" | sort | uniq -c
echo "== last 6 h =="
sacct -u "$USER" -S now-6hours -X -n -o JobName%10,State | grep -v RUNNING | sort | uniq -c
echo "== redox =="
tot=$(cat redox/jobs_*.txt 2>/dev/null | grep . | sort -u | wc -l)
p=0; f=0
for d in redox/primary/*/; do r=$(basename "$d"); grep -q "VIBRATIONAL FREQUENCIES" "$d$r.out" 2>/dev/null && grep -q "ORCA TERMINATED NORMALLY" "$d$r.out" && p=$((p+1)); done
for d in redox/fallback/*/; do r=$(basename "$d"); grep -q "VIBRATIONAL FREQUENCIES" "$d$r.out" 2>/dev/null && grep -q "ORCA TERMINATED NORMALLY" "$d$r.out" && f=$((f+1)); done
echo "finished: $((p+f)) of $tot  (+1/-1 primary $p, fallback $f)"
rv=0; nr=$(grep -c . lists/reverse_S.txt 2>/dev/null || echo 0)
for d in redox/reverse/*/; do [ -d "$d" ] || continue; r=$(basename "$d"); grep -q "VIBRATIONAL FREQUENCIES" "$d$r.out" 2>/dev/null && grep -q "ORCA TERMINATED NORMALLY" "$d$r.out" && rv=$((rv+1)); done
echo "reverse (S closed-shell check): $rv of $nr finished"
echo "FAILED markers: $(ls redox/*/*/FAILED 2>/dev/null | wc -l)   resumed after preemption: $(grep -l 'resuming from' logs/redox_*.log 2>/dev/null | wc -l)"
echo "== scan pilot =="
python3 "$REPO/scans/validate.py" . lists/pilot.txt > logs/validate_last.txt 2>&1 || echo "validate.py failed; see logs/validate_last.txt"
grep -E "minutes per scan point|first-failure|Traceback|Error" logs/validate_last.txt
