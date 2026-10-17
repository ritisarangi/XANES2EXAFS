# Site settings for ALCF Aurora, CPU only (PBS). Sourced by aurora/go.sh and the job scripts.
# Set before submitting (for example in ~/.bashrc):
#   export ACCOUNT=<ALCF project>
#   export ORCA_DIR=<folder holding the orca binary, ORCA 6.0.1>
#   export MPI_DIR=<OpenMPI 4.1.6 install that ORCA 6.0.1 was built against>
#   export WORK=<run folder on /lus/flare>
# Aurora charges whole nodes, so each node runs 6 ORCA jobs of 16 cores side by side
# (aurora/farm.pbs). Cores 0 and 52 are left to the OS; 8 more stay free.
ACCOUNT=${ACCOUNT:?set ACCOUNT to the ALCF project}
QSUB_SITE="-A $ACCOUNT -l filesystems=home:flare -j oe"
SLOTS=${SLOTS:-"1-16 17-32 33-48 53-68 69-84 85-100"}
setup_env() {
  ORCA=${ORCA_DIR:?set ORCA_DIR}
  export PATH=$ORCA:${MPI_DIR:?set MPI_DIR}/bin:$PATH LD_LIBRARY_PATH=$ORCA:$MPI_DIR/lib:$LD_LIBRARY_PATH
  export OMPI_MCA_btl=self,vader OMPI_MCA_pml=ob1 OMPI_MCA_mtl=^ofi
  # each ORCA run is confined to its slot with taskset; OpenMPI must not bind on top of that
  export OMPI_MCA_hwloc_base_binding_policy=none OMPI_MCA_rmaps_base_oversubscribe=1
  # the node script is started by Cray PALS; its PMI settings must not reach ORCA's own mpirun
  local v
  for v in $(env | grep -oE '^(PMI|PMIX|PALS)_[A-Za-z0-9_]*'); do unset "$v"; done
}
