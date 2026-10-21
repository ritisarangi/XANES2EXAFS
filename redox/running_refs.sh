#!/bin/bash
# Print the complexes whose zn_redox task is RUNNING or PENDING now, one per line.
# Running tasks: the complex named on the last "start" line of the task's own log.
# Pending tasks: the line of the chunk file the array was submitted with (logs/submissions.txt);
# chunk files carry a timestamp, so later submissions never overwrite them.
# Run from the project folder.
squeue -u "$USER" -n zn_redox -h -r -o "%F %K %t" | while read a k st; do
  lg="logs/redox_${a}_${k}.log"
  if [ "$st" != PD ] && [ -f "$lg" ]; then
    r=$(grep -oE "^[A-Z0-9]+ (primary|fallback|reverse) start" "$lg" | tail -1 | cut -d' ' -f1)
    [ -n "$r" ] && { echo "$r"; continue; }
  fi
  f=$(grep -E "job=$a( |$)" logs/submissions.txt | tail -1 | awk '{print $3}')
  [ -n "$f" ] && [ -f "$f" ] && sed -n "${k}p" "$f"
done | sort -u
