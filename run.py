import requests
import yaml
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

# Fetching values from .env
url = os.getenv('URL')
output_yaml = os.getenv('OUTPUT_YAML')

# Fetching JSON data from URL
response = requests.get(url)
json_data = response.json()

# Transforming the structure for YAML formatting
yaml_data = {"regions": {}}

for region_id, details in json_data["Regions"].items():
    region_details = {
        "regionid": details["RegionID"],
        "regioncode": details["RegionCode"],
        "regionname": details["RegionName"],
        "nodes": []
    }
    
    for node in details.get("Nodes", []):
        node_details = {
            "name": node.get("Name"),
            "regionid": node.get("RegionID"),
            "hostname": node.get("HostName"),
            "ipv4": node.get("IPv4"),
            "ipv6": node.get("IPv6"),
            "stunport": 0,
            "stunonly": node.get("STUNOnly", False),
            "derpport": 0
        }
        region_details["nodes"].append(node_details)
    
    yaml_data["regions"][region_id] = region_details

# Saving the YAML data to the specified file
with open(output_yaml, 'w') as outfile:
    yaml.dump(yaml_data, outfile, default_flow_style=False)

print(f"YAML data has been saved to '{output_yaml}'.")
