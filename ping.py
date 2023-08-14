import platform
import subprocess

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