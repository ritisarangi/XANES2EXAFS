#!/bin/bash
# Watcher for preemptable runs. S3DF cancels preempted jobs on the preemptable QOS instead of
# requeueing them, so this small job resubmits whatever stopped, then schedules itself again.
# Start once from the project folder:
#   sbatch --account=ssrl:smbxas --export=ALL,REPO=$(cd ../XANES2EXAFS && pwd) ../XANES2EXAFS/redox/watcher.slurm
# Stops itself when every reverse complex is finished or marked FAILED.
# To stop it early:  scancel -n zn_watch
#SBATCH --job-name=zn_watch
#SBATCH --partition=milano
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
#SBATCH --open-mode=append
#SBATCH --output=logs/watcher.log
cd "$SLURM_SUBMIT_DIR" || exit 1
EVERY=${EVERY:-30}
echo "== $(date '+%F %T') watcher run"
bash "${REPO:?}/redox/resubmit_reverse.sh"
total=$(cat lists/reverse_*.txt | sort -u | grep -c .)
fin=0
for r in $(cat lists/reverse_*.txt | sort -u); do
  d=redox/reverse/$r
  { grep -q "VIBRATIONAL FREQUENCIES" "$d/$r.out" 2>/dev/null && grep -q "ORCA TERMINATED NORMALLY" "$d/$r.out"; } && fin=$((fin+1)) && continue
  [ -f "$d/FAILED" ] && fin=$((fin+1))
done
echo "finished or FAILED: $fin of $total"
if [ "$fin" -ge "$total" ]; then echo "all reverse runs settled; watcher stops"; exit 0; fi
if squeue -u "$USER" -n zn_watch -h -t PENDING | grep -q .; then echo "another watcher already queued"; exit 0; fi
sbatch --account="$SLURM_JOB_ACCOUNT" --begin=now+${EVERY}minutes --export=ALL,REPO="$REPO",EVERY="$EVERY" "$REPO/redox/watcher.slurm"
