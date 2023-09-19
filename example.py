import updawg
import time
import yaml

def load_config(file_path):
  with open(file_path, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)
  return config

def addToEmailList(address):
  address = updawg.defaultAction(address)
  if address["status"] != 200:
    addressEmails.append(address)
  return address


config = load_config('config.yaml')
# ("Index to check", "Array to check against", "Function to call on hit")
customChecks = [
  ("name", ["RCC Connection", "Test Address - Will Fail"], addToEmailList)
]

while True:
  addressEmails = []

  updawg.cycle(customChecks=customChecks, clientCode=config["client-code"], userId=config["user-id"])

  notifyUsers()

  # Sleep if needed
  print("Sleeping", end="", flush=True)
  sleepTime, ticks = 30, 5
  for x in range(ticks):
    print(".", end="", flush=True)
    time.sleep(sleepTime/ticks)

  print( "\r" + "".join("=" for _ in range(25)) + "\n" )