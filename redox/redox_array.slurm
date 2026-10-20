#!/bin/bash
# One complex per array task: optimisation + analytic Hessian at the charge moved toward neutral.
# A neutral complex whose +1 run does not finish is rerun at -1 in the same task.
# Runs on the preemptable QOS: a requeued task resumes each optimisation from its last
# geometry (redox/resume.py) and skips a primary run already marked as failed.
# MODE=reverse (set by submit_redox.sh) runs only redox/reverse/<REF>, the opposite charge step.
#SBATCH --job-name=zn_redox
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=72:00:00
#SBATCH --open-mode=append
#SBATCH --output=logs/redox_%A_%a.log
module purge
module load openmpi/v4.1.7
MPIROOT=$(dirname $(dirname $(which mpirun)))
ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
ROOT=$SLURM_SUBMIT_DIR
HERE=${REPO:?}/redox
trap 'echo "stopped by Slurm $(date "+%F %T")"; exit 143' TERM
REF=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$ROOT/$LIST")
done_ok() { grep -q "ORCA TERMINATED NORMALLY" "$1/$REF.out" 2>/dev/null && grep -q "VIBRATIONAL FREQUENCIES" "$1/$REF.out"; }
run() {
  cd "$ROOT/redox/$1/$REF" || return 1
  done_ok . && { echo "$REF $1 already done"; return 0; }
  [ -f FAILED ] && { echo "$REF $1 failed in an earlier attempt"; return 1; }
  python3 "$HERE/resume.py" "$REF"
  echo "$REF $1 start $(date '+%F %T') on $(hostname)"
  $ORCA/orca $REF.inp > $REF.out
  rm -f $REF.gbw $REF*.tmp* $REF.densities* ${REF}_trj.xyz $REF.engrad $REF.opt 2>/dev/null
  echo "$REF $1 end $(date '+%F %T')"
  done_ok . || { touch FAILED; return 1; }
}
if [ "${MODE:-}" = reverse ]; then run reverse && exit 0; echo "$REF reverse FAILED"; exit 1; fi
if run primary; then exit 0; fi
if [ -d "$ROOT/redox/fallback/$REF" ]; then
  echo "$REF primary did not finish; running the -1 fallback"
  run fallback && exit 0
fi
echo "$REF FAILED"; exit 1
