#!/bin/bash
# Stage 1: r2SCAN-3c CPCM(water) optimization, one array task per complex.
# Submitted by scripts/submit.sh; LIST (lists/*.txt) is passed with --export.
#SBATCH --job-name=zn_s1
#SBATCH --account=ssrl:smbxas
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=12:00:00
#SBATCH --output=logs/s1_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
ROOT=$SLURM_SUBMIT_DIR
REF=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
cd "$ROOT/stage1_r2scan/$REF" || exit 1
done_ok() { grep -q "ORCA TERMINATED NORMALLY" $REF.out 2>/dev/null && grep -q "OPTIMIZATION RUN DONE" $REF.out; }
if done_ok; then echo "$REF stage 1 already done"; exit 0; fi
$ORCA/orca $REF.inp > $REF.out
done_ok || { echo "$REF stage 1 FAILED"; exit 1; }
