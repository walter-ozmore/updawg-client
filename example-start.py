import updawg
import yaml

def setDown(address):
  address["status"] = 400
  return address

def load_config(file_path):
  with open(file_path, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)
  return config

config = load_config('config.yaml')
updawg.userId = config["user-id"]
updawg.clientCode = config["client-code"]
# updawg.customChecks = [
#   ("name", ["FGCore1", "Other Test Server B"], setDown)
# ]

updawg.start()