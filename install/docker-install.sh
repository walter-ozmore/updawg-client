#!/bin/bash

# Define the URL of the GitHub repository
repo_url="https://github.com/Soul327/updawg-client.git"

# Define the target directory
target_directory="/etc/updawg"

# Make our install directory
mkdir -p "$target_directory"

# Clone fresh github
git clone "$repo_url" "$target_directory"