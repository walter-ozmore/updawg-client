import git # pip install GitPython
import os
import shutil

# Moves the given file in to the repo folder
def move(name):
  source = name
  dest = os.path.join(repoFolder, name)
  if os.path.exists(source):
    shutil.copy(source, dest)
    print(f"{source} moved to {dest}.")
  else:
    print(f"{source} not found.")

def downloadRepo():
  print("Downloading repo")
  if os.path.exists(repoFolder):
    shutil.rmtree(repoFolder)

  # GitHub repository URL
  repository_url = 'https://github.com/Soul327/updawg-client.git'

  # Clone the repository
  repo = git.Repo.clone_from(repository_url, repoFolder)

  # Checkout the latest branch (e.g., 'main' or 'master')
  latest_branch = repo.heads[0]
  latest_branch.checkout()

  # Delete extra files like git ignore?

def cleanFolder():
  print("Removing older version")
  for filename in os.listdir('.'):
    # Check if the item is a file (not a subdirectory)
    if filename in protectedFiles:
      continue

    # Delete files and folders
    path = os.path.join('.', filename)
    if os.path.isfile(path):
      os.remove(path)
    else:
      shutil.rmtree(path)

def moveRepo():
  print("Installing new version")
  for filename in os.listdir(repoFolder):
    path = os.path.join(repoFolder, filename)

    # Check if the item is a file (not a subdirectory)
    if filename in protectedFiles and not os.path.exists(path):
      continue

    # Move files and folders
    if os.path.isfile(path):
      shutil.copy(path, os.path.join(".", filename))
    else:
      shutil.copytree(path, os.path.join(".", filename))

repoFolder = "./repo"
protectedFiles = ["repo", "config.yaml", "start.py"]

downloadRepo()
cleanFolder()
moveRepo()

print("Deleting repo")
shutil.rmtree(repoFolder)