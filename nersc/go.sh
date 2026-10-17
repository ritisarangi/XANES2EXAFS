#!/bin/bash
# One command for the Zn scan production run on NERSC Perlmutter.
#
#   bash XANES2EXAFS/nersc/go.sh setup  <scan_bundle.tar.gz>   unpack, check ORCA/MPI/account, run a 5-minute ORCA test
#   bash XANES2EXAFS/nersc/go.sh submit                         write scan inputs (first time) and submit the next wave
#   bash XANES2EXAFS/nersc/go.sh status                         queue, finished jobs, validated points
#   bash XANES2EXAFS/nersc/go.sh restart                        continue branches stopped by the 48 h limit
#   bash XANES2EXAFS/nersc/go.sh export                         validate and pack passing geometries into scan_results.tar.gz
#
# Needs in the environment (put them in ~/.bashrc): ACCOUNT (NERSC project), ORCA_DIR, MPI_DIR.
# Optional: WORK (run folder, default $PSCRATCH/zn_scans), WAVE (array chunks per submit, default 20),
# MAX (concurrent tasks per chunk, default 30).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(dirname "$HERE")
WORK=${WORK:-$PSCRATCH/zn_scans}
WAVE=${WAVE:-20}
export SITE=nersc
cmd=${1:-status}

need() { for v in ACCOUNT ORCA_DIR MPI_DIR; do [ -n "${!v}" ] || { echo "set $v first (see the header of this script)"; exit 1; }; done; }

case "$cmd" in
setup)
  need
  B=${2:?give the path to scan_bundle.tar.gz}
  mkdir -p "$WORK" && tar -xzf "$B" -C "$WORK"
  [ -x "$ORCA_DIR/orca" ] || { echo "no orca binary in $ORCA_DIR"; exit 1; }
  [ -x "$MPI_DIR/bin/mpirun" ] || { echo "no mpirun in $MPI_DIR/bin"; exit 1; }
  mkdir -p "$WORK/test" && cd "$WORK/test"
  printf '! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) Opt TightSCF\n%%pal nprocs 16 end\n%%maxcore 3000\n* xyz 0 1\nO 0 0 0\nH 0 0.76 0.59\nH 0 -0.76 0.59\n*\n' > test.inp
  source "$REPO/sites/nersc.sh"
  id=$(sbatch --parsable $SBATCH_SITE --time=00:20:00 --job-name=zn_test --ntasks=16 --output=test_%j.log \
       --wrap "source $REPO/sites/nersc.sh; setup_env; \$ORCA/orca test.inp > test.out; grep -q 'ORCA TERMINATED NORMALLY' test.out && echo ORCA_TEST_OK || echo ORCA_TEST_FAILED")
  echo "unpacked to $WORK; $(wc -l < "$WORK/lists/scan_full.txt") complexes in lists/scan_full.txt"
  echo "test job $id submitted; in a few minutes run:  cat $WORK/test/test_$id.log   (expect ORCA_TEST_OK)"
  ;;
submit)
  need
  cd "$WORK"
  [ -f scans/jobs_scan_full.txt ] || python3 "$REPO/scans/make_scans.py" . lists/scan_full.txt | tail -3
  mkdir -p logs scans/chunks
  [ -n "$(ls scans/chunks/jobs_scan_full_* 2>/dev/null)" ] || split -l 99 -d scans/jobs_scan_full.txt scans/chunks/jobs_scan_full_
  touch logs/submitted_chunks.txt
  source "$REPO/sites/nersc.sh"
  k=0
  for f in scans/chunks/jobs_scan_full_*; do
    grep -qx "$f" logs/submitted_chunks.txt && continue
    [ $k -ge $WAVE ] && break
    n=$(grep -c . "$f")
    id=$(sbatch --parsable $SBATCH_SITE --array=1-${n}%${MAX:-30} --export=ALL,LIST="$f",REPO="$REPO",SITE=nersc "$REPO/scans/scan_array.slurm")
    echo "$f" >> logs/submitted_chunks.txt
    echo "$(date '+%F %T') $f n=$n site=nersc account=$ACCOUNT job=$id" | tee -a logs/submissions.txt
    k=$((k+1))
  done
  left=$(( $(ls scans/chunks/jobs_scan_full_* | wc -l) - $(wc -l < logs/submitted_chunks.txt) ))
  echo "submitted $k chunks this time; $left chunks still to submit (run 'go.sh submit' again when the queue drains)"
  ;;
status)
  cd "$WORK"
  echo "queue: $(squeue -u $USER -h -t R | wc -l) running, $(squeue -u $USER -h -t PD | wc -l) pending lines"
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt 2>/dev/null | head -4
  ;;
restart)
  need
  cd "$WORK" && bash "$REPO/scans/submit_restart.sh"
  ;;
export)
  cd "$WORK"
  python3 "$REPO/scans/validate.py" . lists/scan_full.txt > /dev/null
  python3 "$REPO/scans/export_points.py" . lists/scan_full.txt
  echo "send $WORK/scan_results.tar.gz back to Riti"
  ;;
*) echo "commands: setup <bundle> | submit | status | restart | export"; exit 1 ;;
esac
