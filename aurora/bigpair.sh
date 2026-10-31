#!/bin/bash
# Keeps our queued 256-node farms from running at the same time: when one starts, the others still
# queued are held (qhold keeps their eligible time); when none runs, the held ones are released.
# Farms are found by name (zn_main) and size (>= 256 nodes), so new ones are picked up by themselves.
# Run in `screen -S zn_bigpair`; log in $WORK/autopilot/bigpair.log.
L=/lus/flare/projects/ModCon/dsokaras/zn_scans/autopilot/bigpair.log
echo "[$(date -u '+%F %T')] watching all zn_main farms of 256 nodes or more" >> $L
while true; do
  big=$(qstat -u "$USER" 2>/dev/null | awk '$4 == "zn_main" && $6 >= 256 {sub(/\..*/, "", $1); print $1, $10}')
  run=$(echo "$big" | awk '$2 == "R" {print $1; exit}')
  echo "$big" | while read -r j s; do
    [ -z "$j" ] && continue
    if [ -n "$run" ] && [ "$s" = Q ]; then qhold "$j" && echo "[$(date -u '+%F %T')] $run running: held $j" >> $L; fi
    if [ -z "$run" ] && [ "$s" = H ]; then qrls "$j" && echo "[$(date -u '+%F %T')] none running: released $j" >> $L; fi
  done
  sleep 60
done
