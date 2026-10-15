#!/bin/bash
# Runs after the pilot stage-1 array ends. If at least 6 of 7 pilot complexes converged,
# it submits the other 340 complexes (lists/rest.txt).
#SBATCH --job-name=zn_gate
#SBATCH --account=ssrl:smbxas
#SBATCH --partition=milano
#SBATCH --constraint=OS_VER:9.6
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000M
#SBATCH --time=00:15:00
#SBATCH --output=logs/gate_%j.log
cd "$SLURM_SUBMIT_DIR"
python3 scripts/status.py lists/pilot.txt
OK=$(python3 - <<'EOF'
import csv; print(sum(r["stage1"]=="converged" for r in csv.DictReader(open("status.csv"))))
EOF
)
echo "pilot stage-1 converged: $OK/7"
if [ "$OK" -ge 6 ]; then
  bash scripts/submit.sh lists/rest.txt 18
else
  echo "pilot gate failed; full set NOT submitted" | tee -a logs/submissions.txt
fi
