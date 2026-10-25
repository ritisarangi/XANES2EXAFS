#!/bin/bash
# pm_bench.sh <REF> <config>...   config = name:cores_per_job:jobs:maxcore
# Fills one Perlmutter CPU node (2 x 64-core EPYC 7763, cores 0-127, siblings 128-255) with identical
# ORCA jobs of each layout, pinned to disjoint physical cores, and reports node throughput, as
# aurora/bench/bench.sh did on Aurora (same inputs: aurora/bench/mkinp.py, geom MaxIter 2).
set -u
T=${T:-$PSCRATCH/zn_nersc_test}; REF=$1; shift
SW=$T/sw; ORCA=$SW/orca_6_0_1_linux_x86-64_shared_openmpi416; MPI=$SW/openmpi-4.1.6
export PATH=$ORCA:$MPI/bin:$PATH LD_LIBRARY_PATH=$ORCA:$MPI/lib:${LD_LIBRARY_PATH:-} OPAL_PREFIX=$MPI
export OMPI_MCA_btl=self,vader OMPI_MCA_pml=ob1 OMPI_MCA_mtl=^ofi OMPI_MCA_hwloc_base_binding_policy=none OMPI_MCA_rmaps_base_oversubscribe=1
for v in $(env | grep -oE '^(PMI|PMIX|SLURM)_[A-Za-z0-9_]*'); do unset "$v"; done
ulimit -s unlimited
H=$(hostname -s); OUT=$T/bench/$REF; mkdir -p $OUT
{ lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core|Socket|NUMA node[0-9]'; free -g | head -2; } > $OUT/node_$H.txt
for cfg in "$@"; do
  IFS=: read name c n mc <<< "$cfg"
  D=$OUT/$name; rm -rf $D; mkdir -p $D; t0=$(date +%s); free0=$(free -g | awk '/Mem/{print $3}')
  ( peak=0; while sleep 15; do u=$(free -g | awk '/Mem/{print $3}'); [ $u -gt $peak ] && peak=$u; echo $peak > $D/peak_mem_gb; done ) & MON=$!
  for k in $(seq 0 $((n - 1))); do
    lo=$((k * c)); hi=$((lo + c - 1)); j=$D/j$k; mkdir -p $j; run=/tmp/pmb_${name}_$k; rm -rf $run; mkdir -p $run
    sed -e "s/^%pal nprocs [0-9]* end/%pal nprocs $c end/" -e "s/^%maxcore [0-9]*/%maxcore $mc/" $T/inputs/$REF.inp > $run/b.inp; cp $run/b.inp $j/
    ( cd $run && OMPI_MCA_orte_tmpdir_base=$run OMPI_MCA_btl_vader_backing_directory=$run taskset -c $lo-$hi $ORCA/orca b.inp > $j/b.out 2>&1; echo "$lo-$hi $(date +%s)" > $j/done; rm -rf $run ) &
  done
  wait $(jobs -p | grep -v "^$MON$") 2>/dev/null; t1=$(date +%s); kill $MON 2>/dev/null
  ok=$(grep -l 'TERMINATED NORMALLY\|OPTIMIZATION DID NOT CONVERGE' $D/j*/b.out 2>/dev/null | wc -l)
  cyc=$(grep -c 'GEOMETRY OPTIMIZATION CYCLE' $D/j0/b.out)
  echo "$H $REF $name cores/job=$c jobs=$n maxcore=$mc makespan=$((t1-t0))s ended=$ok/$n cycles=$cyc peakmem=$(cat $D/peak_mem_gb 2>/dev/null)GB(base $free0) node_jobs_per_hour=$(awk -v n=$n -v t=$((t1-t0)) 'BEGIN{printf "%.2f", n*3600/t}')" | tee -a $T/bench/summary.txt
done
