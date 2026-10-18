#!/bin/bash
# One relaxed-scan branch per array task. LIST names a chunk of a jobs file (<= 99 lines);
# each line is a job folder relative to the project folder (the submit directory).
# A task that Slurm requeues after preemption finds its partial scan.out and continues from
# the last converged step (restart.py --prepare), then stitches the pieces into one scan.out.
#SBATCH --job-name=zn_scan
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --open-mode=append
#SBATCH --output=logs/scan_%A_%a.log
source "${REPO:?}/sites/${SITE:-s3df}.sh"
setup_env
ROOT=$SLURM_SUBMIT_DIR
HERE=$REPO/scans
trap 'echo "stopped by Slurm $(date "+%F %T")"; exit 143' TERM
D=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
cd "$ROOT/$D" || exit 1
if grep -q "ORCA TERMINATED NORMALLY" scan.out 2>/dev/null; then echo "$D already done"; exit 0; fi
if [ -s scan.out ] || [ -s scan_cont.out ]; then
  echo "$D partial output found (restart ${SLURM_RESTART_COUNT:-0}); continuing from the last converged step"
  (cd "$ROOT" && python3 "$HERE/restart.py" . --prepare "$D")
  if grep -q "ORCA TERMINATED NORMALLY" scan.out 2>/dev/null; then echo "$D already done"; exit 0; fi
fi
echo "$D start $(date '+%F %T') on $(hostname)"
if [ -s scan_acc.txt ]; then
  $ORCA/orca scan.inp > scan_cont.out
  rm -f scan.gbw scan*.tmp scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null
  (cd "$ROOT" && python3 "$HERE/restart.py" . --stitch "$D")
else
  $ORCA/orca scan.inp > scan.out
  rm -f scan.gbw scan*.tmp scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null
fi
echo "$D end $(date '+%F %T')"
grep -q "ORCA TERMINATED NORMALLY" scan.out || { echo "$D ORCA did not terminate normally"; exit 1; }
