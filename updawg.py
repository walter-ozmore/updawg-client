import requests
import json
import time
from pythonping import ping

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

def cycle():
  global clientCode

  # Grab data from the server
  print("Fetching data from server")
  data = post("fetch")
  print("SERVER: " + data["message"] + "\n")

  # ClientCode is invalid, exit program
  if(data["code"] == 1):
    exit()

  # Update client code
  clientCode = data["clientCode"]

  # Loop though and ping all addresses then store them in a list for return
  for collection in data['collections'].items():
    # Ping the addresses
    for address in collection[1]["addresses"]:
      print(address["pingingAddress"], end=" ")
      address["lastUpdate"] = int(time.time())

      try:
        response = ping(address["pingingAddress"], count=1, timeout=1)
      except:
        address["status"] = 2
        continue

      address["status"] = 1 if response.success() else 2

      print( response.success() )

  # Return the updated list to the server
  print("\nSending update data to server")
  # print(data)
  data = post("update", data)
  print("SERVER: " + data["message"])


def saveClientCode():
  with open("client-code.txt", "w") as file:
    file.write(clientCode)

def loadClientCode():
  with open("client-code.txt", "r") as file:
    clientCode = file.read()
  return clientCode

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
url = "https://www.everyoneandeverything.org/updawg-v2/ajax/client"
clientCode = loadClientCode()
userId = 8

while True:
  cycle()
  time.sleep(20)
saveClientCode()