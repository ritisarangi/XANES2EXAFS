#!/bin/bash
# Keeps the Zn campaign going unattended. Run it in a detached screen on a login node:
#   screen -dmS zn_autopilot bash XANES2EXAFS/aurora/autopilot.sh
# Every 10 minutes it
#   - re-queues the stopped branches of farms that ended (go.sh submit with NODES=0)
#   - keeps WANT_MAIN 256-node prod farms, WANT_MAIN_CAP 16-node capacity farms for the main pool and
#     WANT_BIG 16-node capacity farms (big pool) queued or running, with 6 h walltimes (the best
#     queue priority on Aurora)
#   - every 6 h audits and publishes finished complexes (go.sh publish)
#   - every 2 h writes aurora/STATUS.md and pushes it
# and pauses new submissions (touch $WORK/autopilot/PAUSE to pause by hand) when more than
# FAIL_MAX ORCA runs failed since the last check. New farms go to the first project in ACCOUNTS
# with an allocation that ends more than 8 h from now and has at least MIN_BALANCE node-hours
# (isaac, then ModCon); when it moves on, farms still queued on the old project are cancelled. It runs go.sh from a frozen copy of the scripts,
# so editing the clone never breaks a step in progress; restart the autopilot to pick up changes.
# Settings come from ~/.bashrc (ACCOUNT ORCA_DIR MPI_DIR WORK) and the variables below.
set -u
# ~/.bashrc may stop early in a non-interactive shell, so take the four settings from it directly
eval "$(grep -E '^export (ACCOUNT|ORCA_DIR|MPI_DIR|WORK)=' ~/.bashrc)"
export ACCOUNT ORCA_DIR MPI_DIR WORK
SRC=$(cd "$(dirname "$0")/.." && pwd)
WANT_MAIN=${WANT_MAIN:-2} WANT_BIG=${WANT_BIG:-2} WANT_MAIN_CAP=${WANT_MAIN_CAP:-1} FAIL_MAX=${FAIL_MAX:-25}
MIN_BALANCE=${MIN_BALANCE:-1500} ACCOUNTS=${ACCOUNTS:-isaac ModCon}
A=$WORK/autopilot; mkdir -p "$A"
LOG=$A/autopilot.log
SNAP=$A/repo; rm -rf "$SNAP"; mkdir -p "$SNAP"; cp -r "$SRC/aurora" "$SRC/scans" "$SRC/sites" "$SNAP/"
export RESULTS=${RESULTS:-$(dirname "$SRC")/XANES2EXAFS-results}   # the aurora-results checkout
GO="bash $SNAP/aurora/go.sh"
[ -n "${DRY:-}" ] && GO="echo DRY go.sh"      # DRY=1 ONCE=1: one cycle, log what it would do
say() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }
farms() {   # id name queue state account
  qstat -u "$USER" 2>/dev/null | awk '$4 ~ /^zn_(main|big)$/ {sub(/\..*/, "", $1); print $1, $4, $3, $10}' |
    while read -r id name q st; do echo "$id $name $q $st $(qstat -f "$id" 2>/dev/null | awk '/Account_Name/ {print $3}')"; done
}
hours() {   # 6 h, or less (at least 2 h) so the farm can still finish before a full-machine reservation
            # (maintenance); partial reservations leave nodes for our farms, so they do not count
  local now s best=6 h
  now=$(date +%s)
  s=$(pbs_rstat -f 2>/dev/null | awk '/^reserve_start/ {sub(/^reserve_start = /, ""); st=$0} /Resource_List.nodect/ && $3 >= 10000 {print st}' |
      while read -r d; do date -d "$d" +%s; done | awk -v n="$now" '$1 > n' | sort -n | head -1)
  if [ -n "$s" ]; then
    h=$(( (s - now) / 3600 - 1 ))       # whole hours left before it starts, minus 1 h to get a start slot
    [ "$h" -lt 6 ] && [ "$h" -ge 2 ] && best=$h
  fi
  echo $best
}
usable() {   # print the node-hours left on project $1 if an allocation runs > 8 h more with >= MIN_BALANCE
  sbank-list-allocations -p "$1" 2>/dev/null | awk -v p="$1" -v min="$MIN_BALANCE" -v now="$(date +%s)" '
    $6 == p && $4 ~ /^20[0-9][0-9]-/ { gsub(",", "", $9); cmd = "date -d " $4 " +%s"; cmd | getline end; close(cmd)
      if (end - now > 8 * 3600 && $9 + 0 >= min) { print int($9); exit } }'
}
failed() { grep -l 'did not terminate normally' "$WORK"/logs/scan*_*.log 2>/dev/null | xargs -r grep -L -E 'DUE TO TIME LIMIT|CANCELLED' | wc -l; }
say "autopilot started (pid $$, scripts frozen from $SRC at $(git -C "$SRC" rev-parse --short HEAD), accounts: $ACCOUNTS)"
acct_prev=
prev=$(farms | awk '{print $1":"$2}'); prevfail=$(failed); last_pub=0; last_stat=0
while :; do
  now=$(date +%s)
  cur=$(farms)
  # 1. farms that left the queue: put their stopped branches back in the pool's queue
  for x in $prev; do
    id=${x%%:*} name=${x##*:}
    echo "$cur" | grep -q "^$id " && continue
    say "farm $id ($name) ended: $(tail -1 "$WORK"/logs/$id.*.OU 2>/dev/null)"
    POOL=${name#zn_} NODES=0 $GO submit >> "$LOG" 2>&1
  done
  # 2. guards
  fail=$(failed)
  if [ $((fail - prevfail)) -gt "$FAIL_MAX" ]; then
    touch "$A/PAUSE"; say "ALERT: $((fail - prevfail)) new failed ORCA runs since the last check; submissions paused"
  fi
  prevfail=$fail
  why= acct=
  for a in $ACCOUNTS; do bal=$(usable "$a"); [ -n "$bal" ] && { acct=$a; break; }; done
  if [ -z "$acct" ]; then why="no project in '$ACCOUNTS' has a usable allocation"
  else
    export ACCOUNT=$acct
    if [ "$acct" != "$acct_prev" ]; then
      say "new farms go to project $acct ($bal node-hours left)"
      # farms still queued on another project would wait on an ending allocation: cancel them
      echo "$cur" | awk -v a="$acct" '$4 == "Q" && $5 != "" && $5 != a {print $1, $5}' | while read -r id old; do
        if [ -n "${DRY:-}" ]; then say "DRY would cancel queued farm $id on $old"
        else qdel "$id" && say "cancelled queued farm $id on $old (allocation not usable)"; fi; done
      cur=$(farms); acct_prev=$acct
    fi
  fi
  [ -e "$A/PAUSE" ] && why="paused ($A/PAUSE)"
  # 3. keep farms queued
  if [ -z "$why" ]; then
    left_main=$(( $(grep -c . "$WORK/queue/main/tasks.txt") - $(cat "$WORK/queue/main/next") ))
    left_big=$(( $(grep -c . "$WORK/queue/big/tasks.txt") - $(cat "$WORK/queue/big/next") ))
    n_main=$(echo "$cur" | awk -v a="$ACCOUNT" '$2 == "zn_main" && $3 != "capacity" && ($4 == "R" || $5 == a)' | grep -c .)
    n_big=$(echo "$cur" | awk -v a="$ACCOUNT" '$2 == "zn_big" && ($4 == "R" || $5 == a)' | grep -c .)
    n_cap=$(echo "$cur" | awk '$3 == "capacity"' | grep -c .)
    n_main_cap=$(echo "$cur" | awk -v a="$ACCOUNT" '$2 == "zn_main" && $3 == "capacity" && ($4 == "R" || $5 == a)' | grep -c .)
    # 256-node farms only while the main queue can fill them (24 slots per node)
    if [ "$n_main" -lt "$WANT_MAIN" ] && [ "$left_main" -gt 3000 ]; then
      say "submitting main farm on $ACCOUNT (queue $left_main left, $n_main main farms)"
      POOL=main QUEUE=prod NODES=256 HOURS=$(hours) $GO submit >> "$LOG" 2>&1
    fi
    # and one 16-node main farm in capacity, which starts far more often than the 256-node ones
    if [ "$n_main_cap" -lt "$WANT_MAIN_CAP" ] && [ "$left_main" -gt 0 ] && [ "$n_cap" -lt 5 ]; then
      say "submitting main capacity farm on $ACCOUNT, $(hours) h (queue $left_main left)"
      POOL=main QUEUE=capacity NODES=16 HOURS=$(hours) $GO submit >> "$LOG" 2>&1; n_cap=$((n_cap + 1))
    fi
    if [ "$n_big" -lt "$WANT_BIG" ] && [ "$left_big" -gt 0 ] && [ "$n_cap" -lt 5 ]; then
      say "submitting big farm on $ACCOUNT (queue $left_big left, $n_big big farms)"
      POOL=big QUEUE=capacity NODES=16 HOURS=$(hours) $GO submit >> "$LOG" 2>&1
    fi
  else
    say "no new farms: $why"
  fi
  # 4. publish finished complexes, write the status page
  if [ $((now - last_pub)) -ge 21600 ]; then
    say "publish: $( $GO publish 2>&1 | tail -2 | tr '\n' ' ')"; last_pub=$now
  fi
  if [ $((now - last_stat)) -ge 7200 ]; then
    bash "$SNAP/aurora/status.sh" > "$SRC/aurora/STATUS.md" 2>/dev/null
    [ -z "${DRY:-}" ] && ( cd "$SRC" && git add aurora/STATUS.md && git commit -q -m "Aurora status $(date '+%F %H:%M')" aurora/STATUS.md \
      && git push -q ) >> "$LOG" 2>&1 && say "STATUS.md pushed"
    last_stat=$now
  fi
  prev=$(farms | awk '{print $1":"$2}')
  [ -n "${ONCE:-}" ] && break
  sleep 600
done
