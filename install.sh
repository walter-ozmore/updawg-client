#!/bin/bash

uninstall() {
	# === Clean up old install files if they exist === 
	SERVICE_FILE="/etc/systemd/system/updawg.service"

	# Stop the service if it exists
	if [ -f "$SERVICE_FILE" ]; then
		systemctl stop updawg
		rm "$SERVICE_FILE"  # Delete the file
	fi

	# Clean up execution path
	TARGET_DIR="/etc/updawg"
	if [ -d "$TARGET_DIR" ]; then
		find "$TARGET_DIR" -mindepth 1 ! -name 'config.yaml' ! -name 'start.py' -exec rm -rf {} +
	fi
}


download() {
	# Define the URL of the GitHub repository
	repo_url="https://github.com/Soul327/updawg-client.git"

	# Check if Git is installed
	if command -v git >/dev/null 2>&1; then
		echo "Git is already installed."
	else
		echo "Git is not installed, please install Git then run the script again"
	fi

	# Clone the repo to temp folder
	echo -n "Downloading repo..."
	git clone "$repo_url" "$TEMP_DIR" > /dev/null 2>&1
	echo " done."
}


install() {
	# === Install the files ===
	# INSTALL_FILES="/home/soul/UpDawg Client"
	INSTALL_FILES=$TEMP_DIR

	# Make our folders and copy our files
	mkdir -p "/etc/updawg"
	rsync -av --delete --exclude='start.py' --exclude='config.yaml' "$INSTALL_FILES/" "/etc/updawg" > /dev/null 2>&1

	# Copy our example files to live files
	if [ ! -f "/etc/updawg/start.py" ]; then
		cp "/etc/updawg/example-start.py" "/etc/updawg/start.py"
	fi

	if [ ! -f "/etc/updawg/config.yaml" ]; then
		cp "/etc/updawg/example-config.yaml" "/etc/updawg/config.yaml"
	fi

	# Copy our systemctl file
	ln -s "/etc/updawg/updawg.service" "/etc/systemd/system" # Runner file
	systemctl daemon-reload
	
	chmod 755 -R /etc/updawg # Set permissions
}



set -e # Exit immediately if any command fails

# Check if the script is being run with root privileges
if [[ $EUID -ne 0 ]]; then
	echo "This script must be run with sudo or as root."
	exit 1
fi

TEMP_DIR=$(mktemp -d)


echo $TEMP_DIR
download
uninstall
install