#!/bin/bash
# Keeps the two queued 256-node farms from running at the same time: when one starts, the other is
# held (qhold keeps its eligible time); when the running one has ended, the held one is released.
# Run in `screen -S zn_bigpair`; log in $WORK/autopilot/bigpair.log. Jobs as arguments.
L=/lus/flare/projects/ModCon/dsokaras/zn_scans/autopilot/bigpair.log
st() { qstat -f "$1" 2>/dev/null | awk '/job_state/ {print $3}'; }
echo "[$(date -u '+%F %T')] watching $*" >> $L
while true; do
  run=; for j in "$@"; do [ "$(st $j)" = R ] && run=$j; done
  for j in "$@"; do
    s=$(st $j)
    if [ -n "$run" ] && [ "$j" != "$run" ] && [ "$s" = Q ]; then qhold "$j" && echo "[$(date -u '+%F %T')] $run running: held $j" >> $L; fi
    if [ -z "$run" ] && [ "$s" = H ]; then qrls "$j" && echo "[$(date -u '+%F %T')] none running: released $j" >> $L; fi
  done
  sleep 60
done
