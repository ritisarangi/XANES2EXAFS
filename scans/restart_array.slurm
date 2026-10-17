#!/bin/bash
# Continue one stopped scan branch per array task (inputs from scans/restart.py), then stitch.
#SBATCH --job-name=zn_scanr
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --output=logs/scanr_%A_%a.log
source "${REPO:?}/sites/${SITE:-s3df}.sh"
setup_env
ROOT=$SLURM_SUBMIT_DIR
HERE=$REPO/scans
D=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
cd "$ROOT/$D" || exit 1
if grep -q "ORCA TERMINATED NORMALLY" scan.out 2>/dev/null; then echo "$D already done"; exit 0; fi
echo "$D start $(date '+%F %T') on $(hostname)"
$ORCA/orca scan.inp > scan_cont.out
rm -f scan.gbw scan*.tmp scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null
cd "$ROOT" && python3 "$HERE/restart.py" . --stitch "$D"
echo "$D end $(date '+%F %T')"
grep -q "ORCA TERMINATED NORMALLY" "$D/scan.out" || exit 1
