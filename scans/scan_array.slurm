#!/bin/bash
# One relaxed-scan branch per array task. LIST names a chunk of a jobs file (<= 99 lines);
# each line is a job folder relative to the project folder (the submit directory).
#SBATCH --job-name=zn_scan
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=72:00:00
#SBATCH --output=logs/scan_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
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
