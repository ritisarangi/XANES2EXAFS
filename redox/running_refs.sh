#!/bin/bash
# Print the complexes whose redox task is RUNNING or PENDING now, one per line.
# Maps each Slurm array task to its line of the chunk file it was submitted with
# (logs/submissions.txt), so it does not depend on what the job has written to its log.
# Run from the project folder.
squeue -u "$USER" -n zn_redox -h -r -o "%F %K" | while read a k; do
  f=$(grep -E "job=$a( |$)" logs/submissions.txt | tail -1 | awk '{print $3}')
  [ -n "$f" ] && [ -f "$f" ] && sed -n "${k}p" "$f"
done | sort -u
