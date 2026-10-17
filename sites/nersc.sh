# Site settings for NERSC Perlmutter CPU nodes. Sourced by the submit scripts and the Slurm job scripts.
# Set before submitting (for example in ~/.bashrc):
#   export ACCOUNT=<NERSC project, e.g. m1234>
#   export ORCA_DIR=<folder holding the orca binary, ORCA 6.0.1>
#   export MPI_DIR=<OpenMPI 4.1.x install that ORCA 6.0.1 was built against>
# The shared QOS charges only the cores used. Perlmutter counts hardware threads as CPUs,
# so 16 MPI ranks on 16 physical cores need --cpus-per-task=2.
ACCOUNT=${ACCOUNT:?set ACCOUNT to the NERSC project}
SBATCH_SITE="--account=$ACCOUNT --constraint=cpu --qos=shared --cpus-per-task=2 --mem=60G --time=48:00:00"
setup_env() {
  ORCA=${ORCA_DIR:?set ORCA_DIR}
  export PATH=$ORCA:${MPI_DIR:?set MPI_DIR}/bin:$PATH LD_LIBRARY_PATH=$ORCA:$MPI_DIR/lib:$LD_LIBRARY_PATH
  export OMPI_MCA_btl=self,vader
}
