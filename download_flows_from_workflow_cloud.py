import requests
import json
import os

API = 'https://app.kendra.io/api'
flows = requests.get(API).json()

for flow in flows:
    flow_name = flow['adapterName']
    flow_id = flow['id']
    print(f"{flow_name} {flow_id}")

    try:
        response = requests.get(f"{API}/{flow_name}/{flow_id}")
        code = json.dumps(response.json(), indent=4)

        # Create a directory for the flow_name if it doesn't exist
        if not os.path.exists(flow_name):
            os.makedirs(flow_name)

        # Save the JSON file in the flow_name directory with flow_id as the filename
        filename = f"{flow_name}/{flow_id}.json"
        with open(filename, 'w') as file:
            file.write(code)
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error parsing JSON for flow '{flow_name} {flow_id}': {e}")
