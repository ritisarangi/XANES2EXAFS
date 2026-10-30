#!/bin/bash
# Keeps the unattended campaign alive on an Aurora login node. Every 5 min it checks that the agent
# (Claude Code), the autopilot, the NERSC driver and the 256-node pair watcher each run in their
# screen session, and restarts any that is missing. A restarted agent is told to re-create its
# hourly check-in and event watch, which live only inside its session.
#   screen -dmS zn_watchdog bash ~/dev/xanes2exafs/XANES2EXAFS/aurora/watchdog.sh
#   touch ~/.zn_watchdog_off      # pause it (for example to stop the agent on purpose)
# It cannot survive a reboot of the login node: after one, start it again (README, step "After a
# maintenance").
W=/lus/flare/projects/ModCon/dsokaras/zn_scans
L=$W/autopilot/watchdog.log
REPO=$HOME/dev/xanes2exafs/XANES2EXAFS
say() { echo "[$(date -u '+%F %T')] $*" >> "$L"; }
has_screen() { screen -ls | grep -q "[0-9]\.$1[[:space:]]"; }
agent_up() { pgrep -u "$USER" -x claude >/dev/null && ps -u "$USER" -o args= | grep -q '^claude .*--remote-control zn-aurora'; }
say "watchdog started (pid $$)"
while true; do
  if [ ! -e "$HOME/.zn_watchdog_off" ]; then
    if ! agent_up; then
      say "agent not running: starting it in screen zn_agent"
      screen -dmS zn_agent bash -c "cd $HOME/dev/xanes2exafs && claude --continue --remote-control zn-aurora --dangerously-skip-permissions 'The watchdog restarted this session (the previous one had stopped). Read HPC_LESSONS.md section Running a campaign with an agent and your memory, re-create the hourly Zn check-in (CronCreate, cron 17 * * * *) and its 7-day renewal reminder, re-arm the event watch, check every screen and farm, and log the restart in the Run log.'"
    fi
    has_screen zn_autopilot || { say "autopilot missing: restarting"; screen -dmS zn_autopilot env WANT_BIG=0 WANT_MAIN_CAP=2 bash "$REPO/aurora/autopilot.sh"; }
    has_screen zn_nersc || { say "NERSC driver missing: restarting"; screen -dmS zn_nersc bash -c 'cd ~/dev/iri/nersc_run && ../venv/bin/python driver.py >> driver.out 2>&1'; }
    if ! has_screen zn_bigpair && [ -s "$W/autopilot/bigpair.jobs" ]; then
      say "pair watcher missing: restarting"; screen -dmS zn_bigpair "$W/autopilot/bigpair.sh" $(cat "$W/autopilot/bigpair.jobs")
    fi
  fi
  sleep 300
done
