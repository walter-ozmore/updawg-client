#!/bin/bash

# Exit immediately if any command fails
set -e

# Define the URL of the GitHub repository
repo_url="https://github.com/Soul327/updawg-client.git"

# Define the target directory
target_directory="/etc/updawg"


# Stop the service while we do the update
$service_name="updawg"
if systemctl list-units --full --no-pager --quiet --all | grep -Fq "$service_name"; then
  # Stop the service
  systemctl stop "$service_name"
  echo "Service '$service_name' stopped."
fi

# Install all dependencies
apt-get update
apt-get install -y git python3 python3-pip
pip3 install --no-cache-dir requests PyYAML

if [ ! -d "$target_directory" ]; then
  # Create the target directory if it doesn't exist
  mkdir -p "$target_directory"

  # Clone the repo
  echo "Cloning the repository into $target_directory..."
  git clone "$repo_url" "$target_directory"
  exit
else
  # Change directory to the existing repository
  cd "$target_directory"

  # Check if the directory is a Git repository
  if [ -d .git ]; then
    # Update the repo
    echo "Updating the existing repository in $target_directory..."
    git pull origin main
  else
    # Break
    echo "Error: $target_directory is not a Git repository."
    exit 1
  fi
fi

# Update systemctl stuff
cp /etc/updawg/install/updawg.service /etc/systemd/system/
# cp /etc/updawg/install/updawg.timer /etc/systemd/system/
systemctl daemon-reload


if [ -e "/etc/updawg/start.py" ]; then
  # Assume that this installer is only updating rather than installing
  systemctl start updawg
else
  # Create a config file
  if [ ! -e "/etc/updawg/config.yaml" ]; then
    cp /etc/updawg/example-config.yaml /etc/updawg/config.yaml
  fi

  # Create a start file
  cp /etc/updawg/example-start.py /etc/updawg/start.py

  # Echo info
  echo Find out how to configure this program here https://walter-ozmore.dev/updawg
  echo Job Done - run 'systemctl start updawg' to start the program
fi

# Copy all example files to base config files if the base configs don't exist
