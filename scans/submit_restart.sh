#!/bin/bash
# Prepare and submit continuations of stopped scan branches.
# Run from the project folder:  bash <repo>/scans/submit_restart.sh
# Environment options: SITE (s3df default, or nersc), ACCOUNT (S3DF default ssrl:default), MAX concurrent tasks (default 11)
set -e
SITE=${SITE:-s3df}
[ "$SITE" = s3df ] && ACCOUNT=${ACCOUNT:-ssrl:default}
MAX=${MAX:-11}
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(dirname "$HERE")
source "$REPO/sites/$SITE.sh"
python3 "$HERE/restart.py" .
[ -s scans/jobs_restart.txt ] || exit 0
mkdir -p logs scans/chunks
rm -f scans/chunks/jobs_restart_*
split -l 99 -d scans/jobs_restart.txt scans/chunks/jobs_restart_
for f in scans/chunks/jobs_restart_*; do
  n=$(grep -c . "$f")
  id=$(sbatch --parsable $SBATCH_SITE --array=1-${n}%${MAX} --export=ALL,LIST="$f",REPO="$REPO",SITE="$SITE" "$HERE/restart_array.slurm")
  echo "$(date '+%F %T') $f n=$n account=$ACCOUNT job=$id (restart)" | tee -a logs/submissions.txt
done
