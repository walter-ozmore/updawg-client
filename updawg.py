import requests
import json
import time
import os
import platform
import subprocess
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

def cycle(customChecks=None, clientCode=None, userId=None):
  if clientCode == None:
    return
  if userId == None:
    return

  # Grab data from the server
  print("Fetching data from server", flush=True)
  data = post("fetch", clientCode=clientCode, userId=userId)
  if data == None:
    print("Failed to get data from the server")
    return
  
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
        address = defaultAction(address)

      
      # Notify the user of the status in the console
      if address["status"] in range(200, 300): print(bcolors.OKGREEN, end="")
      if address["status"] in range(300, 400): print(bcolors.WARNING, end="")
      if address["status"] in range(400, 500): print(bcolors.FAIL   , end="")
      if address["status"] in range(500, 600): print(bcolors.FAIL   , end="")
      print(address["status"], bcolors.ENDC)

  # Return the updated list to the server
  print("\nSending update data to server", end="", flush=True)
  # data = post("update", data, clientCode=clientCode, userId=userId)
  clearLine()

  if data["code"] != 0:
    print("SERVER: " + data["message"])

def defaultAction(address):
  # Get the address' status by pinging it
  address["lastUpdate"] = int(time.time())
  numOfRetries = 1
  while numOfRetries > 0:
    numOfRetries -= 1
    response = ping(address["pingingAddress"])
    if response["online"]:
      break
  address["status"] = 200 if response["online"] else 400
  return address


def notifyUsers():
  global lastEmailSentTime

  if time.time() - lastEmailSentTime < 60*15:
    return
  lastEmailSentTime = time.time()

  import smtplib
  from email.mime.text import MIMEText
  from email.mime.multipart import MIMEMultipart
  from email.mime.application import MIMEApplication

  userEmails = ["soulsilver27@hotmail.com", "walter@cooperpropane.com"]

  subject = "UpDawg - Alert"
  # HTML content for the email
  rows = ""
  for address in addressEmails:
    rows += "<tr><td>"+address["name"]+"</td><td>"+str(address["status"])+"</td></tr>"

  html_content = """
    <html>
    <head>
      <style>
        th {
          text-align: left;
        }
      </style>
    </head>
    <body>
      <center><h1>UpDawg Alert</h1></center>
      <table style="width: 100%">
        <tr>
          <th>Name</th>
          <th>Status</th>
        </tr>
      """+rows+"""
      </table>
    </body>
    </html>
  """
  # List servers down

  print("Sending emails")
  for receiver_email in userEmails:
    # Email configuration
    # receiver_email = "soulsilver27@hotmail.com"
    sender_email, password = config["email"]["email"], config["email"]["password"]
    server, port = config["email"]["server"], config["email"]["port"]

    # Create the email content
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to the SMTP server and send the email
    try:
      server = smtplib.SMTP(server, port)
      server.starttls()
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, msg.as_string())
      server.quit()
      print("Email sent successfully!")
    except Exception as e:
      print("Error sending email:", str(e))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
url = "https://everyoneandeverything.org/updawg-v2/ajax/client"
userId = -1
lastEmailSentTime = 0