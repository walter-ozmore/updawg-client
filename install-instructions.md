sudo apt-get update
sudo apt-get install git

cd /etc
sudo git clone https://github.com/Soul327/updawg-client.git updawg

<!-- Make copies of the starter files -->
sudo cp example-start.py start.py
sudo cp example-config.yaml config.yaml