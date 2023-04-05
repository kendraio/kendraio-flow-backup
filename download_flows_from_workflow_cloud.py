import os
import json
import requests

try:
    response = requests.get("https://app.kendra.io/api/")
    flows = response.json()

    for flow in flows:
        flow_name = flow['adapterName']
        flow_id = flow['workflowId']
        print(f"{flow_name} {flow_id}")

        try:
            # Create a directory for the flow_name if it doesn't exist
            if not os.path.exists(flow_name):
                os.makedirs(flow_name)

            # Save the JSON file in the flow_name directory with flow_id as the filename
            filename = f"{flow_name}/{flow_id}.json"
            with open(filename, 'w') as file:
                file.write(json.dumps(flow, indent=4))
        except Exception as e:
            print(f"Error downloading flow '{flow_name} {flow_id}': {e}")

except Exception as e:
    print(f"Error getting list of flows: {e}")
