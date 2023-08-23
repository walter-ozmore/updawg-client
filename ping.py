import platform
import subprocess
import re

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
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
    if system_platform == "Windows":
      # Extract response time from Windows ping output
      time_match = re.search(r"time=(\d+)ms", result.stdout)
      if time_match:
        response_time = int(time_match.group(1))
      else:
        response_time = None
    else:
      # Extract response time from Linux/macOS ping output
      time_match = re.search(r"time=(\d+(\.\d+)?) ms", result.stdout)
      if time_match:
        response_time = float(time_match.group(1))
      else:
        response_time = None
    return {"online": True, "response_time": response_time}
  except subprocess.CalledProcessError:
    return {"online": False, "response_time": None}