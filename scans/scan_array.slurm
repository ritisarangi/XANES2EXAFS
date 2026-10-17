#!/bin/bash
# One relaxed-scan branch per array task. LIST names a chunk of a jobs file (<= 99 lines);
# each line is a job folder relative to the project folder (the submit directory).
#SBATCH --job-name=zn_scan
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --output=logs/scan_%A_%a.log
source "${REPO:?}/sites/${SITE:-s3df}.sh"
setup_env
ROOT=$SLURM_SUBMIT_DIR
D=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
cd "$ROOT/$D" || exit 1
if grep -q "ORCA TERMINATED NORMALLY" scan.out 2>/dev/null; then echo "$D already done"; exit 0; fi
echo "$D start $(date '+%F %T') on $(hostname)"
$ORCA/orca scan.inp > scan.out
# keep the output, per-step geometries and scan tables; drop wavefunction and scratch files
rm -f scan.gbw scan*.tmp scan.densities* scan.*.gbw scan_*.tmp* 2>/dev/null
echo "$D end $(date '+%F %T')"
grep -q "ORCA TERMINATED NORMALLY" scan.out || { echo "$D ORCA did not terminate normally"; exit 1; }
