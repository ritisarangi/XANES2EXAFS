#!/bin/bash
# Submit a dielectric jobs file in chunks of 99 (S3DF MaxArraySize is 100).
# Run from the project folder:  bash <repo>/dielectric/submit_eps.sh dielectric/jobs_pilot.txt
# Environment options: ACCOUNT (default ssrl:smbxas), MAX concurrent tasks per chunk (default 14)
set -e
JOBS=${1:?give a jobs file, e.g. dielectric/jobs_pilot.txt}
ACCOUNT=${ACCOUNT:-ssrl:smbxas}
MAX=${MAX:-14}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p logs dielectric/chunks
base=$(basename "$JOBS" .txt)
rm -f dielectric/chunks/${base}_*
split -l 99 -d "$JOBS" dielectric/chunks/${base}_
for f in dielectric/chunks/${base}_*; do
  n=$(grep -c . "$f")
  id=$(sbatch --parsable --account="$ACCOUNT" --array=1-${n}%${MAX} --export=ALL,LIST="$f" "$HERE/eps_array.slurm")
  echo "$(date '+%F %T') $f n=$n account=$ACCOUNT job=$id" | tee -a logs/submissions.txt
done
