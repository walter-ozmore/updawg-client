import requests
import json
import time
from ping import ping

'''
  Response status codes are based on HTTP status codes
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses

  100-199: Informational 
  200-299: Successful
  300-399: Warnings
  400-499: Address Errors
  500-599: UpDawg Client Errors
'''

# Colors for command line
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def clearLine():
  print("\r" + ("".join(" " for _ in range(30))) + "\r", end="", flush=True)


def fetchData(local=False):
  if local:
    with open('data.json', 'r') as dataFile:
      # Reading from json file
      data = json.load(dataFile)
    return data

  return post("fetch")


def updateData(data, local=False):
  if local:
    with open("data.json", "w") as dataFile:
      json.dump(data, dataFile)
    return
  post("update", data)


def post(function, jsonObj={}, clientCode=None, userId=None):
  if clientCode == None or userId == None:
    return
  
  jsonString = json.dumps(jsonObj)

  # Data to be sent in the request body
  args = {
    "userId"    : userId,
    "clientCode": clientCode,
    "function"  : function,
    "json"      : jsonString
  }

  # Send POST request
  try:
    response = requests.post(url, data=args, headers=headers)
  except:
    return

  # Ignore errors
  if response.status_code != 200:
    print('Request failed with status code:', response.status_code)
    return

  # Try and decode the json
  try:
    data = json.loads(response.text)
  except:
    print("Failed to decode message: " + response.text)
    return
  return data


def pingCheck(address):
  # Get the address' status by pinging it
  address["lastUpdate"] = int(time.time())
  numOfRetries = 4
  while numOfRetries > 0:
    numOfRetries -= 1
    response = ping(address["pingingAddress"])
    if response["online"]:
      break
  address["status"] = 200 if response["online"] else 400
  return address

def checkAddress(currentTime):
  # TODO: Make this in to an algorithm that can be selected by a user
  # Get the oldest address that has been updated
  oldestAddress = None
  oldestTimestamp = None
  currentTimestamp = time.time()

  # Get the oldest address that has been updated
  for collectionID in data["collections"]:
    addresses = data["collections"][collectionID]["addresses"]
    for address in addresses:
      timestamp = float(address["lastUpdate"])
      interval = float(address["pingInterval"])

      if interval == None or interval < 0:
        interval = 30


      if currentTimestamp - timestamp < interval:
        continue
      
      if oldestTimestamp is None or timestamp < oldestTimestamp:
        oldestTimestamp = timestamp
        oldestAddress = address
        # print(address) # For testing

  # If there is no oldestAddress then there is nothing to update
  if oldestAddress == None:
    return

  # Changing the name of oldestAddress so it looks better, also im lazy
  address = oldestAddress

  # Draw address
  string = "%-20s" % (address["name"] if address["name"] != None and len(address["name"]) > 0 else address["pingingAddress"])
  print(string, end="", flush=True)
  
  # Check on the address
  hasChecked = False
  for customCheck in customChecks:
    if address[customCheck[0]] in customCheck[1]:
      address = customCheck[2](address)
      hasChecked = True
      break
  
  if hasChecked == False:
    address = pingCheck(address)
  
  # Set the last update time
  address["lastUpdate"] = str(time.time())

  # Draw the updated status && Notify the user of the status in the console
  if address["status"] in range(200, 300): print(bcolors.OKGREEN, end="")
  if address["status"] in range(300, 400): print(bcolors.WARNING, end="")
  if address["status"] in range(400, 500): print(bcolors.FAIL   , end="")
  if address["status"] in range(500, 600): print(bcolors.FAIL   , end="")
  print(address["status"], bcolors.ENDC)
    
def start():
  global data

  updateInterval = 30
  lastUpdate = time.time()

  # Load in all our data
  data = post("fetch", clientCode=clientCode, userId=userId)
  if data == None:
    print("UPDATE: Failed to get data from the server")
    return

  # Thread:
  while True:
    currentTime = int(time.time())

    # Check to see if we should update the server
    if currentTime - lastUpdate >= updateInterval:
      print("Updating with the server...")
      post("update", data, clientCode=clientCode, userId=userId)
      while True:
        data = post("fetch", clientCode=clientCode, userId=userId)
        if data != None:
          break
      lastUpdate = int(time.time())
      continue

    # Check for an address that hasnt been updated in a while
    checkAddress(currentTime)

    # Sleep for a little bit to prevent hoging the system resources
    time.sleep( .1 )

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
# url = "https://everyoneandeverything.org/updawg-v2/ajax/client"
url = "http://127.0.0.1/updawg/ajax/client"
userId = -1
clientCode = ""
data = None
customChecks = []