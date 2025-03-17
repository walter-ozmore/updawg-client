#!/bin/bash

# Pull changes from origin/master
git pull -f origin master

# Check for any changes made since the last pull
CHANGES=$(git diff --name-only HEAD@{1}..HEAD)

# If there were no changes, exit the script
if [ -z "$CHANGES" ]; then
  echo "No changes detected. Exiting."
  exit 0
fi

# Restart the updawg service if any changes were made
echo "Restarting service"
systemctl restart --reload updawg.service