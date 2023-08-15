import requests
import json
import time
import os
import platform
import subprocess

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


def post(function, jsonObj={}):
  jsonString = json.dumps(jsonObj)

  # Data to be sent in the request body
  args = {
    "userId"    : userId,
    "clientCode": clientCode,
    "function"  : function,
    "json"      : jsonString
  }

  # Send POST request
  response = requests.post(url, data=args, headers=headers)

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

def cycle(customChecks=None):
  global clientCode

  if clientCode == None:
    clientCode = loadClientCode()

  # Grab data from the server
  print("Fetching data from server", end="", flush=True)
  data = post("fetch")
  
  # Check for errors, when there is an error print it out
  # ClientCode is invalid, exit program
  if(data["code"] == 1):
    print("\rERROR: " + data["message"] + "\n")
    exit()
  # Clear the line
  clearLine()

  # Update client code
  clientCode = data["clientCode"]

  # Loop though and ping all addresses then store them in a list for return
  for collection in data['collections'].items():
    # Ping the addresses
    for address in collection[1]["addresses"]:
      # Notify the user which address is being worked on
      string = "%-20s" % (address["name"] if address["name"] != None and len(address["name"]) > 0 else address["pingingAddress"])
      print(string, end="", flush=True)

      # Get custom function
      customFunction = None
      if(customChecks != None):
        for check in customChecks:
          if(address[check[0]] in check[1]):
            customFunction = check[2]
            break
      

      if customFunction != None:
        address = customFunction(address)
      else:
        # Get the address' status by pinging it
        address["lastUpdate"] = int(time.time())
        address["status"] = 200 if ping(address["pingingAddress"]) else 400

      
      # Notify the user of the status in the console
      if address["status"] in range(200, 300): print(bcolors.OKGREEN, end="")
      if address["status"] in range(300, 400): print(bcolors.WARNING, end="")
      if address["status"] in range(400, 500): print(bcolors.FAIL   , end="")
      if address["status"] in range(500, 600): print(bcolors.FAIL   , end="")
      print(address["status"], bcolors.ENDC)

  # Return the updated list to the server
  print("\nSending update data to server", end="", flush=True)
  data = post("update", data)
  clearLine()

  if data["code"] != 0:
    print("SERVER: " + data["message"])


def saveClientCode():
  with open("client-code.txt", "w") as file:
    file.write(clientCode)

def loadClientCode():
  if os.path.exists("client-code.txt") == False:
    print("ERROR: " + os.getcwd() + "/client-code.txt was not found!")
    exit()
  
  with open("client-code.txt", "r") as file:
    clientCode = file.read()
  return clientCode

def ping(server_address):
  system_platform = platform.system()

  if system_platform == "Windows":
    # On Windows, use the 'ping' command
    command = ["ping", "-n", "1", server_address]
  elif system_platform == "Linux" or system_platform == "Darwin":
    # On Linux and macOS, use the 'ping' command
    command = ["ping", "-c", "1", server_address]
  else:
    raise NotImplementedError("Unsupported platform: " + system_platform)

  try:
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return True  # Server responded to ping
  except subprocess.CalledProcessError:
    return False  # Server did not respond to ping

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
url = "https://www.everyoneandeverything.org/updawg-v2/ajax/client"
userId = 8
clientCode = None