#!/bin/bash
# Submit a redox jobs file in chunks of 99 (S3DF MaxArraySize is 100).
# Run from the project folder:  bash <repo>/redox/submit_redox.sh redox/jobs_pilot.txt
# Environment options: EXCLUDE=node1,node2 keeps jobs off bad nodes (default sdfmilan105); MODE=reverse runs redox/reverse inputs only; ACCOUNT (default ssrl:default, the preemptable QOS; requeued tasks resume), MAX concurrent tasks per chunk (default 20)
set -e
EXCLUDE=${EXCLUDE-sdfmilan105}
JOBS=${1:?give a jobs file, e.g. redox/jobs_pilot.txt}
ACCOUNT=${ACCOUNT:-ssrl:default}
MAX=${MAX:-20}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p logs redox/chunks
base=$(basename "$JOBS" .txt)
stamp=$(date +%Y%m%d%H%M%S)   # unique chunk names: running arrays keep reading their own list
split -l 99 -d "$JOBS" redox/chunks/${base}_${stamp}_
for f in redox/chunks/${base}_${stamp}_*; do
  n=$(grep -c . "$f")
  id=$(sbatch --parsable --account="$ACCOUNT" ${EXCLUDE:+--exclude=$EXCLUDE} --requeue --array=1-${n}%${MAX} --export=ALL,MODE="${MODE:-}",LIST="$f",REPO="$(dirname "$HERE")" "$HERE/redox_array.slurm")
  echo "$(date '+%F %T') $f n=$n account=$ACCOUNT job=$id (redox ${MODE:-primary})" | tee -a logs/submissions.txt
done
