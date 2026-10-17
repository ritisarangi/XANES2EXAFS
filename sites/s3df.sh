# Site settings for SLAC S3DF (milano). Sourced by the submit scripts and the Slurm job scripts.
ACCOUNT=${ACCOUNT:-ssrl:smbxas}
SBATCH_SITE="--account=$ACCOUNT --partition=milano --constraint=OS_VER:9.6 --mem-per-cpu=4000M --time=72:00:00"
setup_env() {
  module purge
  module load openmpi/v4.1.7
  local MPIROOT=$(dirname $(dirname $(which mpirun)))
  ORCA=/sdf/group/ssrl/sarangi/sw/orca601/orca_6_0_1
  export PATH=$ORCA:$PATH LD_LIBRARY_PATH=$ORCA:$MPIROOT/lib:$MPIROOT/lib64:$LD_LIBRARY_PATH
}
