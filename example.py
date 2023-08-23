import updawg
import time
import yaml

def setDown(address):
  address["status"] = 2
  return address

def load_config(file_path):
    with open(file_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

config = load_config('config.yaml')


# ("Index to check", "Array to check against", "Function to call on hit")
customChecks = [
  ("name", ["CoreServer", "LocalServer"], setDown)
]

while True:
  updawg.cycle(clientCode=config["client-code"])

  # Sleep if needed
  print("Sleeping", end="", flush=True)

  sleepTime, ticks = 30, 5
  for x in range(ticks):
    print(".", end="", flush=True)
    time.sleep(sleepTime/ticks)
  
  print( "\r" + "".join("=" for _ in range(25)) + "\n" )