#!/bin/bash
# Stage 2: B3LYP-D3(BJ) CPCM(water) TightOpt + analytic Freq from the stage-1 geometry.
# def2-TZVP on Zn and first-shell donors, def2-SVP elsewhere. Starts only after the
# matching stage-1 task finishes (aftercorr dependency set in scripts/submit.sh).
#SBATCH --job-name=zn_s2
#SBATCH --account=ssrl:smbxas
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=72:00:00
#SBATCH --output=logs/s2_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
ROOT=$SLURM_SUBMIT_DIR
REF=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
cd "$ROOT/stage2_b3lyp/$REF" || exit 1
done_ok() { grep -q "ORCA TERMINATED NORMALLY" $REF.out 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" $REF.out; }
if done_ok; then echo "$REF stage 2 already done"; exit 0; fi
python3 "$ROOT/scripts/make_stage2_inp.py" "$ROOT" "$REF" || { echo "$REF no stage-1 geometry"; exit 1; }
$ORCA/orca $REF.inp > $REF.out
done_ok || { echo "$REF stage 2 FAILED"; exit 1; }
