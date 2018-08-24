#!/bin/bash
# Checks if badgebot is active and re-activates if not

running=$(ps -eaf | grep badge)
if [[ $running != *"badgebot.py"* ]]; then
  python3 ~/badgebot/badgebot.py >> ~/badgebot/log 2>&1
fi
