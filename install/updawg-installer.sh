#!/bin/bash

# Define the URL of the GitHub repository
repo_url="https://github.com/Soul327/updawg-client.git"

# Define the target directory
target_directory="/etc/updawg"

# Check if Git is installed
if command -v git >/dev/null 2>&1; then
    echo "Git is already installed."
else
    # Install Git if not installed
    echo "Git is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y git
fi

# Create the target directory if it doesn't exist
if [ ! -d "$target_directory" ]; then
    sudo mkdir -p "$target_directory"
    echo "Cloning the repository into $target_directory..."
    git clone "$repo_url" "$target_directory"
else
    # Change directory to the existing repository
    cd "$target_directory"

    # Check if the directory is a Git repository
    if [ -d .git ]; then
        echo "Updating the existing repository in $target_directory..."
        git pull origin master
    else
        echo "Error: $target_directory is not a Git repository."
        exit 1
    fi
fi

# Copy all example files to base config files
if [ ! -e "/etc/updawg/config.yaml" ]; then
    sudo cp /etc/updawg/example-config.yaml /etc/updawg/config.yaml
if [ ! -e "/etc/updawg/start.py" ]; then
    sudo cp /etc/updawg/example-start.py /etc/updawg/start.py

# Update systemctl stuff
sudo cp /etc/updawg/install/updawg.service /etc/systemd/system/
sudo systemctl daemon-reload

# Echo info 
echo Job Done - run 'sudo systemctl start updawg' to start the program