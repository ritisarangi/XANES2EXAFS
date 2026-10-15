#!/bin/bash
# Usage (on S3DF, from the project root): bash scripts/submit.sh lists/pilot.txt
#                                         bash scripts/submit.sh lists/all.txt
# Submits stage 1 as a job array and stage 2 as a second array whose task i starts only
# after stage-1 task i succeeds (aftercorr). Tasks already finished are skipped, so the
# full list can be submitted after the pilot without rerunning pilot complexes.
# Concurrency: %MAX per array; the account's node limit queues anything beyond it.
set -e
LIST=${1:?give a list file, e.g. lists/pilot.txt}
MAX=${2:-18}; S1MAX=${S1MAX:-80}; S2MAX=${S2MAX:-40}
cd "$(dirname "$0")/.."
mkdir -p logs
N=$(grep -c . "$LIST")
S1=$(sbatch --parsable --array=1-${N}%${S1MAX} --export=ALL,LIST="$LIST" scripts/stage1_array.slurm)
S2=$(sbatch --parsable --array=1-${N}%${S2MAX} --dependency=aftercorr:${S1} --export=ALL,LIST="$LIST" scripts/stage2_array.slurm)
echo "$(date '+%F %T') $LIST n=$N stage1=$S1 stage2=$S2" | tee -a logs/submissions.txt
