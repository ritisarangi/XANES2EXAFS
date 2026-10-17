#!/bin/bash
# bench.sh <outdir> <REF> <config>...   config = name:cores_per_job:jobs:ht(0/1):hbm(0/1):maxcore:scratch(lustre|tmp)
# Fills one node with identical ORCA jobs in each layout and reports node throughput.
set -u
OUT=$1 REF=$2; shift 2
REPO=$(cd "$(dirname "$0")/../.." && pwd)
source $REPO/sites/aurora.sh; setup_env; ulimit -s unlimited
H=$(hostname -s)
mkdir -p $OUT
{ echo "== $H"; lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core|Socket|NUMA node[0-9]'; numactl -H | grep -E 'size|cpus'; free -g | head -2
  echo "cpuset: $(taskset -pc $$)"; echo "siblings of cpu1: $(cat /sys/devices/system/cpu/cpu1/topology/thread_siblings_list)"
  df -h /tmp /dev/shm | tail -2; } > $OUT/node_$H.txt 2>&1
sib() { cat /sys/devices/system/cpu/cpu$1/topology/thread_siblings_list | tr ',' '\n' | grep -v "^$1$" | head -1; }
hbm_of() {  # CPU-less NUMA node nearest to socket NUMA node $1
  local best= bd=999 n d
  for n in /sys/devices/system/node/node*; do n=${n##*node}; [ -z "$(cat /sys/devices/system/node/node$n/cpulist)" ] || continue
    d=$(awk -v k=$((n+1)) '{print $k}' /sys/devices/system/node/node$1/distance); [ $d -lt $bd ] && bd=$d best=$n; done; echo $best; }
for cfg in "$@"; do
  IFS=: read name c n ht hbm mc scr <<< "$cfg"
  phys=$c; [ $ht = 1 ] && phys=$((c / 2))
  per=$((n / 2)); free0=$(free -g | awk '/Mem/{print $3}')
  D=$OUT/$name; rm -rf $D; mkdir -p $D; t0=$(date +%s)
  ( peak=0; while sleep 15; do u=$(free -g | awk '/Mem/{print $3}'); [ $u -gt $peak ] && peak=$u; echo $peak > $D/peak_mem_gb; done ) & MON=$!
  for s in 0 1; do base=$((s * 52 + 1)); hb=$(hbm_of $s)
    for k in $(seq 0 $((per - 1))); do
      lo=$((base + k * phys)); hi=$((lo + phys - 1)); cl="$lo-$hi"
      [ $ht = 1 ] && cl="$cl,$(sib $lo)-$(sib $hi)"
      j=$D/j${s}_$k; mkdir -p $j; python3 $(dirname $0)/mkinp.py $REPO $REF $c $mc ${MAXITER:-2} > $j/b.inp
      run=$j; [ $scr = tmp ] && { run=/tmp/zb_${name}_${s}_$k; rm -rf $run; mkdir -p $run; cp $j/b.inp $run/; }
      pol=""; [ $hbm = 1 ] && pol="numactl --preferred=$hb"
      ( cd $run && taskset -c $cl $pol $ORCA/orca b.inp > $j/b.out 2>&1; echo "$cl $(date +%s)" > $j/done
        [ $scr = tmp ] && { du -sh $run > $j/scratch_size; rm -rf $run; } ) &
    done
  done
  wait $(jobs -p | grep -v "^$MON$") 2>/dev/null
  t1=$(date +%s); kill $MON
  ok=$(grep -l 'TERMINATED NORMALLY\|OPTIMIZATION DID NOT CONVERGE\|geometry optimization did not converge' $D/j*/b.out 2>/dev/null | wc -l)
  cyc=$(grep -c 'GEOMETRY OPTIMIZATION CYCLE' $D/j0_0/b.out)
  echo "$H $name cores/job=$c jobs=$n ht=$ht hbm=$hbm maxcore=$mc scratch=$scr makespan=$((t1-t0))s ended=$ok/$n cycles=$cyc peakmem=$(cat $D/peak_mem_gb 2>/dev/null)GB(base ${free0}) node_jobs_per_hour=$(awk -v n=$n -v t=$((t1-t0)) 'BEGIN{printf "%.2f", n*3600/t}')" | tee -a $OUT/summary.txt
done
