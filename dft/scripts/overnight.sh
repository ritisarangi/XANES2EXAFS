#!/bin/bash
# One command for the whole run: pilot (stage 1 -> stage 2), then a gate job that
# submits the other 340 once the pilot stage 1 has finished and passed.
set -e
cd "$(dirname "$0")/.."
mkdir -p logs
OUT=$(bash scripts/submit.sh lists/pilot.txt 7)
S1=$(echo "$OUT" | sed -n 's/.*stage1=\([0-9]*\).*/\1/p')
G=$(sbatch --parsable --dependency=afterany:${S1} scripts/gate.slurm)
echo "$(date '+%F %T') gate=$G after pilot stage1=$S1" | tee -a logs/submissions.txt
