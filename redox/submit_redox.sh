#!/bin/bash
# Submit a redox jobs file in chunks of 99 (S3DF MaxArraySize is 100).
# Run from the project folder:  bash <repo>/redox/submit_redox.sh redox/jobs_pilot.txt
# Environment options: ACCOUNT (default ssrl:default), MAX concurrent tasks per chunk (default 20)
set -e
JOBS=${1:?give a jobs file, e.g. redox/jobs_pilot.txt}
ACCOUNT=${ACCOUNT:-ssrl:default}
MAX=${MAX:-20}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p logs redox/chunks
base=$(basename "$JOBS" .txt)
rm -f redox/chunks/${base}_*
split -l 99 -d "$JOBS" redox/chunks/${base}_
for f in redox/chunks/${base}_*; do
  n=$(grep -c . "$f")
  id=$(sbatch --parsable --account="$ACCOUNT" --array=1-${n}%${MAX} --export=ALL,LIST="$f" "$HERE/redox_array.slurm")
  echo "$(date '+%F %T') $f n=$n account=$ACCOUNT job=$id (redox)" | tee -a logs/submissions.txt
done
