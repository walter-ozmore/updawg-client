import updawg
import yaml

def setDown(address):
	"""
	Example function show what you can do with an address
	"""
	address["status"] = 400
	return address


# Load config
def load_config(file_path):
	"""
	Loads info such as the client-code or user-id
	"""
	with open(file_path, 'r') as yaml_file:
		config = yaml.safe_load(yaml_file)
	return config

config = load_config('config.yaml')

updawg.clientCode = config["client-code"]
if "url" in config: updawg.url = config["url"] # Set custom url (optional)

# Create array for custom checks
# (checkType, checkFilters, func)
updawg.customChecks = [
	("name", ["FGCore1", "Other Test Server B"], setDown)
]

updawg.start()