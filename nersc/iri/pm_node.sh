#!/bin/bash
# pm_node.sh <seconds ORCA may run> <branch> ...   up to 16 branches on one Perlmutter CPU node,
# each pm_branch.sh pinned to its own 8 physical cores (0-127), as the Aurora farms do.
set -u
LIMIT=$1; shift; i=0
for D in "$@"; do
  CPUSET=$((i * 8))-$((i * 8 + 7)) bash /pscratch/sd/d/dsokaras/zn_nersc/code/pm_branch.sh "$D" "$LIMIT" &
  i=$((i + 1))
done
wait
