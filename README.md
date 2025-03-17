# Install instructions
## Native (Linux)
REQUIRES: `systemd` `unzip` `wget` `git`

```bash
wget https://github.com/walter-ozmore/updawg-client/archive/refs/heads/main.zip -O updawg-client.zip
unzip updawg-client.zip
cd updawg-client-main
sudo ./install.sh
```

# Post Install
Add your client key under the config file `/etc/updawg/config.yaml`
Run `systemctl start updawg`

Currently the system will not auto update please run the `check-update.sh` script
to update