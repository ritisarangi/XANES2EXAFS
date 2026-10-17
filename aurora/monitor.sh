#!/bin/bash
# One status line per minute for the Zn campaign: farm jobs, ORCA runs per pool, queue progress,
# failed ORCA runs (abnormal ends that are not walltime stops); branch states every 10 minutes.
# ALERT lines when a new failure appears or a farm job leaves the queue.
#   WORK=<run folder> bash XANES2EXAFS/aurora/monitor.sh
W=${WORK:?set WORK to the run folder}; cd "$W" || exit 1
R=$(cd "$(dirname "$0")" && pwd)
prevfail=-1; prevjobs=""; i=0
while true; do
  jobs=$(qstat -u $USER 2>/dev/null | awk '$4 ~ /^zn_(main|big)$/ {sub(/\..*/,"",$1); printf "%s:%s:%s:%s ", $1, $4, $6, $10}')
  line="[$(date +%H:%M)] ${jobs:-no farm jobs}|"
  for p in main big; do
    [ -f queue/$p/tasks.txt ] || continue
    line="$line $p: $(ls queue/$p/active 2>/dev/null | wc -l) ORCA running, $(cat queue/$p/next)/$(grep -c . queue/$p/tasks.txt) handed out |"
  done
  fail=$(grep -L -E 'DUE TO TIME LIMIT|CANCELLED' $(grep -l 'did not terminate normally' logs/scan*_*.log 2>/dev/null) /dev/null 2>/dev/null | grep -vc /dev/null)
  line="$line failed runs: $fail"
  [ $((i % 10)) -eq 0 ] && line="$line | $(python3 $R/queue.py status . scans/jobs_scan_full.txt 2>/dev/null | sed 's/ (running\/stopped\/failed)//')"
  echo "$line"
  [ $prevfail -ge 0 ] && [ $fail -gt $prevfail ] && echo "ALERT: $((fail - prevfail)) new failed ORCA run(s)"
  for j in $prevjobs; do echo "$jobs" | grep -q "${j%%:*}:" || echo "ALERT: farm ${j%%:*} (${j}) left the queue"; done
  prevfail=$fail; prevjobs=$(echo $jobs | tr ' ' '\n' | cut -d: -f1,2 | tr '\n' ' '); i=$((i + 1))
  sleep 60
done
