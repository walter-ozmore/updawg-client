import updawg
import time

def setDown(address):
  address["status"] = 2
  return address


# ("Index to check", "Array to check against", "Function to call on hit")
customChecks = [
  ("name", ["CoreServer", "LocalServer"], setDown)
]

while True:
  updawg.cycle()

  # Sleep if needed
  print("Sleeping", end="", flush=True)
  for x in range(10):
    print(".", end="", flush=True)
    time.sleep(5/10)
  print( "\r" + "".join("=" for _ in range(25)) + "\n" )