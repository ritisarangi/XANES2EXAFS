#!/bin/bash
# Writes the campaign status page (markdown) to stdout; aurora/autopilot.sh commits it as aurora/STATUS.md.
set -u
cd "${WORK:?}" || exit 1
R=$(cd "$(dirname "$0")" && pwd)
echo "# Zn scan campaign on Aurora: status"
echo
echo "Generated $(date '+%F %H:%M %Z') by \`aurora/autopilot.sh\`. Human-written notes are in the run log of \`aurora/README.md\`; validated results are on the \`aurora-results\` branch."
echo
echo "## Branches"
echo
echo '```'
python3 "$R/queue.py" status . scans/jobs_scan_full.txt
for p in main big; do
  echo "queue $p: $(( $(grep -c . queue/$p/tasks.txt) - $(cat queue/$p/next) )) of $(grep -c . queue/$p/tasks.txt) waiting, $(ls queue/$p/active | wc -l) ORCA runs active"
done
echo "failed ORCA runs not retried: $(grep -l 'did not terminate normally' logs/scan*_*.log 2>/dev/null | xargs -r grep -L -E 'DUE TO TIME LIMIT|CANCELLED' | wc -l)"
echo "allocation: $(sbank-list-allocations -p "${ACCOUNT:-isaac}" 2>/dev/null | awk '/Available Balance:/ {print $3, $4, $5; exit}') available on ${ACCOUNT:-isaac}"
echo '```'
echo
echo "## Farm jobs"
echo
echo '| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |'
echo '|---|---|---|---|---|---|---|'
qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_(main|big)$/ {sub(/\..*/, "", $1); printf "| %s | %s | %s | %s | %s | %s | %s |\n", $1, $4, $3, $6, $9, $10, $11}'
echo
echo "## Last autopilot actions"
echo
echo '```'
tail -12 autopilot/autopilot.log 2>/dev/null
echo '```'
