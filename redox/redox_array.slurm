#!/bin/bash
# One complex per array task: optimisation + analytic Hessian at the charge moved toward neutral.
# A neutral complex whose +1 run does not finish is rerun at -1 in the same task.
#SBATCH --job-name=zn_redox
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=72:00:00
#SBATCH --output=logs/redox_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
ROOT=$SLURM_SUBMIT_DIR
REF=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
done_ok() { grep -q "ORCA TERMINATED NORMALLY" "$1/$REF.out" 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" "$1/$REF.out"; }
run() {
  cd "$ROOT/redox/$1/$REF" || return 1
  done_ok . && { echo "$REF $1 already done"; return 0; }
  echo "$REF $1 start $(date '+%F %T') on $(hostname)"
  $ORCA/orca $REF.inp > $REF.out
  rm -f $REF.gbw $REF*.tmp* $REF.densities* ${REF}_trj.xyz $REF.engrad $REF.opt 2>/dev/null
  echo "$REF $1 end $(date '+%F %T')"
  done_ok .
}
if run primary; then exit 0; fi
if [ -d "$ROOT/redox/fallback/$REF" ]; then
  echo "$REF primary did not finish; running the -1 fallback"
  run fallback && exit 0
fi
echo "$REF FAILED"; exit 1
