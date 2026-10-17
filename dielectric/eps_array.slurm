#!/bin/bash
# One optimisation + analytic Hessian per array task at a non-water CPCM dielectric.
# LIST names a chunk of a jobs file (<= 99 lines); each line is dielectric/eps<E>/<REF>.
#SBATCH --job-name=zn_eps
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=72:00:00
#SBATCH --output=logs/eps_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
ROOT=$SLURM_SUBMIT_DIR
D=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
REF=$(basename "$D")
cd "$ROOT/$D" || exit 1
done_ok() { grep -q "ORCA TERMINATED NORMALLY" $REF.out 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" $REF.out; }
if done_ok; then echo "$D already done"; exit 0; fi
echo "$D start $(date '+%F %T') on $(hostname)"
$ORCA/orca $REF.inp > $REF.out
# keep .out, .xyz and .hess; drop wavefunction, trajectory and scratch files
rm -f $REF.gbw $REF*.tmp* $REF.densities* ${REF}_trj.xyz $REF.engrad $REF.opt 2>/dev/null
echo "$D end $(date '+%F %T')"
done_ok || { echo "$D FAILED"; exit 1; }
