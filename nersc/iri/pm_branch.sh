#!/bin/bash
# pm_branch.sh <branch folder, e.g. scans/REF/coord_branch> <seconds ORCA may run>
# One scan branch as one Perlmutter job (shared QOS). Same ORCA build, inputs and restart.py as on
# Aurora: a branch stopped by the time limit is continued from its last geometry (RESUME_PARTIAL),
# and a finished continuation is stitched into scan.out, so the folder ends as Aurora's would.
set -u
T=/pscratch/sd/d/dsokaras/zn_nersc; R=$T/run; D=$1; LIMIT=$2
SW=/pscratch/sd/d/dsokaras/zn_nersc_test/sw; ORCA=$SW/orca_6_0_1_linux_x86-64_shared_openmpi416; MPI=$SW/openmpi-4.1.6
export PATH=$ORCA:$MPI/bin:$PATH LD_LIBRARY_PATH=$ORCA:$MPI/lib:${LD_LIBRARY_PATH:-} OPAL_PREFIX=$MPI
export OMPI_MCA_btl=self,vader OMPI_MCA_pml=ob1 OMPI_MCA_mtl=^ofi OMPI_MCA_hwloc_base_binding_policy=none OMPI_MCA_rmaps_base_oversubscribe=1
# OpenMPI found Cray XPMEM here and uses it for single copies by default; ~2% of branch runs then died
# with a segfault in vader_return_registration (the XPMEM registration cache). Linux CMA instead.
export OMPI_MCA_btl_vader_single_copy_mechanism=cma
for v in $(env | grep -oE '^(PMI|PMIX|SLURM_STEP|SLURM_SRUN)[A-Za-z0-9_]*'); do unset "$v"; done
ulimit -s unlimited
cd $R || exit 1
mkdir -p logs; log=$R/logs/$(echo $D | tr / _)_${SLURM_JOB_ID:-x}.log
ok() { [ -f "$1" ] && tail -c 4096 "$1" | grep -q "ORCA TERMINATED NORMALLY"; }
echo "$D start $(date '+%F %T') on $(hostname) job ${SLURM_JOB_ID:-x}" > $log
ok $D/scan.out && { echo "$D already finished" >> $log; exit 0; }
exec 7>>$D/.run.lock; flock -n 7 || { echo "$D locked by another job; not run" >> $log; exit 3; }
if [ -f $D/scan_cont.out ] || [ -f $D/scan.out ]; then
  RESUME_PARTIAL=1 python3 -c "import sys; sys.path.insert(0,'$T/code'); import restart; print(restart.prepare('$R','$D',False))" >> $log 2>&1 || { echo "$D prepare failed" >> $log; exit 4; }
fi
out=scan.out; [ -f $D/scan_orig.inp ] && out=scan_cont.out
# a shared job has 30 GB for 8 ranks: maxcore 2000 MB leaves headroom (ORCA can exceed maxcore, and an
# allocation failure shows as a segmentation fault); a whole-node job has the node's memory, as on Aurora.
# maxcore only sets ORCA's batching, not the results.
mc=3000; [ -z "${CPUSET:-}" ] && mc=2000
sed -i -e "s/^%pal nprocs [0-9]* end/%pal nprocs 8 end/" -e "s/^%maxcore [0-9]*/%maxcore $mc/" $D/scan.inp
# ORCA scratch: /tmp is memory on Perlmutter and counts against a shared job's memory limit, so a
# shared job (no CPUSET) keeps its scratch on $PSCRATCH; a whole-node job uses /tmp
tmpd=/tmp; [ -z "${CPUSET:-}" ] && tmpd=$T/tmp
run=$tmpd/zn_${SLURM_JOB_ID:-x}_$(echo $D | tr / _); rm -rf $run; mkdir -p $run; cp $D/scan.inp $run/
ompi=/tmp/zn_ompi_${SLURM_JOB_ID:-x}_$(echo $D | tr / _); mkdir -p $ompi    # OpenMPI session and shared memory: small, stays in /tmp
( cd $run && OMPI_MCA_orte_tmpdir_base=$ompi OMPI_MCA_btl_vader_backing_directory=$ompi timeout -s TERM $LIMIT ${CPUSET:+taskset -c $CPUSET} $ORCA/orca scan.inp > $R/$D/$out 2>&1 ); rc=$?
rm -rf $run $ompi
if ok $R/$D/$out; then
  [ $out = scan_cont.out ] && python3 $T/code/restart.py $R --stitch $D >> $log 2>&1
  echo "$D finished" >> $log
elif [ $rc = 124 ]; then echo "DUE TO TIME LIMIT" >> $log
else echo "$D ORCA did not terminate normally (rc $rc)" >> $log; fi
echo "$D end $(date '+%F %T')" >> $log
