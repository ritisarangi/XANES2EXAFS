# Site settings for ALCF Aurora, CPU only (PBS). Sourced by aurora/go.sh and the job scripts.
# Set before submitting (for example in ~/.bashrc):
#   export ACCOUNT=<ALCF project>
#   export ORCA_DIR=<folder holding the orca binary, ORCA 6.0.1>
#   export MPI_DIR=<OpenMPI 4.1.6 install that ORCA 6.0.1 was built against>
#   export WORK=<run folder on /lus/flare>
# Aurora charges whole nodes, so each node runs several ORCA jobs side by side (aurora/farm.pbs),
# each pinned to its own cores. Cores 0 and 52 are left to the OS, leaving 51 per socket.
# Layout options: CORES (MPI ranks per ORCA job), HT=1 (ranks on both hardware threads of
# CORES/2 physical cores), HBM=1 (prefer the socket's HBM for memory), MAXCORE (MB per rank),
# SCRATCH=tmp (default: ORCA works in node-local /tmp, scan.out still goes straight to $WORK;
# 4% faster than Lustre on one node, and keeps ORCA scratch I/O off the shared file system).
ACCOUNT=${ACCOUNT:?set ACCOUNT to the ALCF project}
QSUB_SITE="-A $ACCOUNT -l filesystems=flare -j oe"
CORES=${CORES:-16} HT=${HT:-0} HBM=${HBM:-0} MAXCORE=${MAXCORE:-3000} SCRATCH=${SCRATCH:-tmp}
# AUTO_CORES=1: when the farm starts with fewer queued branches than it has slots, give each branch
# more ranks (4, 6, 8, 12 or 16) so the slots roughly match the queue: fewer idle nodes, and each
# branch runs faster. Decided once in the job script (farm.pbs) and inherited by the node scripts.
if [ "${AUTO_CORES:-0}" = 1 ] && [ -z "${ZN_CORES_SET:-}" ] && [ -n "${PBS_NODEFILE:-}" ] && [ -f "${QDIR:-}/next" ]; then
  _nn=$(sort -u "$PBS_NODEFILE" | wc -l)
  _left=$(( $(grep -c . "$QDIR/tasks.txt") - $(cat "$QDIR/next") ))
  for _c in 4 6 8 12 16; do
    CORES=$_c
    [ $(( _nn * 2 * (51 / _c) )) -le $(( _left + _left / 10 )) ] && break
  done
  export CORES ZN_CORES_SET=1
fi

slot_list() {   # one "cpulist hbm_node" line per slot on this node
  local phys=$CORES s k lo hi cl
  [ "$HT" = 1 ] && phys=$((CORES / 2))
  for s in 0 1; do
    for k in $(seq 0 $((51 / phys - 1))); do
      lo=$((s * 52 + 1 + k * phys)); hi=$((lo + phys - 1)); cl="$lo-$hi"
      [ "$HT" = 1 ] && cl="$cl,$((lo + 104))-$((hi + 104))"
      echo "$cl $((s + 2))"
    done
  done
}
slots_per_node() { local p=$CORES; [ "$HT" = 1 ] && p=$((CORES / 2)); echo $(( 2 * (51 / p) )); }

setup_env() {
  ORCA=${ORCA_DIR:?set ORCA_DIR}
  export PATH=$ORCA:${MPI_DIR:?set MPI_DIR}/bin:$PATH LD_LIBRARY_PATH=$ORCA:$MPI_DIR/lib:$LD_LIBRARY_PATH
  export OPAL_PREFIX=$MPI_DIR      # OpenMPI may have been copied from the folder it was built in
  export OMPI_MCA_btl=self,vader OMPI_MCA_pml=ob1 OMPI_MCA_mtl=^ofi
  # each ORCA run is confined to its slot with taskset; OpenMPI must not bind on top of that
  export OMPI_MCA_hwloc_base_binding_policy=none OMPI_MCA_rmaps_base_oversubscribe=1
  # the node script is started by Cray PALS; its PMI settings must not reach ORCA's own mpirun
  local v
  for v in $(env | grep -oE '^(PMI|PMIX|PALS)_[A-Za-z0-9_]*'); do unset "$v"; done
}
