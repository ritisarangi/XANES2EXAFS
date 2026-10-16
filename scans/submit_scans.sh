#!/bin/bash
# Submit a scan jobs file in chunks of 99 (S3DF MaxArraySize is 100).
# Run from the project folder (the one holding scans/ and stage2_b3lyp/):
#   bash <repo>/scans/submit_scans.sh scans/jobs_pilot.txt
# Options through the environment:
#   ACCOUNT  Slurm account (default ssrl:smbxas)
#   MAX      concurrent tasks per chunk (default 30; 16 cores each)
set -e
JOBS=${1:?give a jobs file, e.g. scans/jobs_pilot.txt}
ACCOUNT=${ACCOUNT:-ssrl:smbxas}
MAX=${MAX:-30}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p logs scans/chunks
base=$(basename "$JOBS" .txt)
rm -f scans/chunks/${base}_*
split -l 99 -d "$JOBS" scans/chunks/${base}_
for f in scans/chunks/${base}_*; do
  n=$(grep -c . "$f")
  id=$(sbatch --parsable --account="$ACCOUNT" --array=1-${n}%${MAX} --export=ALL,LIST="$f" "$HERE/scan_array.slurm")
  echo "$(date '+%F %T') $f n=$n account=$ACCOUNT job=$id" | tee -a logs/submissions.txt
done
