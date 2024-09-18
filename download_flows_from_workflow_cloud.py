import requests
import json
import os
from collections import OrderedDict

API = 'https://app.kendra.io/flows/'

def create_flow_dict(flow):
    # Create an OrderedDict for the encoded data (mimicking the server's _encoded field)
    encoded_data = OrderedDict()
    for key, value in flow.items():
        if key not in ['workflowId', 'adapterName', 'created', 'tags', 'updated', 'modified', 'title']:
            encoded_data[key] = value

    # Create an OrderedDict for the additional fields (mimicking the server's behavior)
    additional_data = OrderedDict([
        ('workflowId', flow.get('id')),
        ('adapterName', flow.get('adapterName')),
        ('created', flow.get('created')),
        *([('tags', flow.get('tags'))] if 'tags' in flow else []),
        #('tags', flow.get('tags', [])),  # Use empty list as default
        ('updated', flow.get('updated')),
        ('modified', flow.get('updated')),  # Set modified to match updated
        ('title', flow.get('title'))
    ])

    # Merge the dictionaries in the correct order
    result = OrderedDict()
    result.update(encoded_data)
    result.update(additional_data)

    return result

def backup_flows():
    try:
        # Make a single API call to get all flows with full data
        response = requests.get(API)
        flows = response.json()

        for flow in flows:
            flow_name = flow.get('adapterName', 'Unknown')
            flow_id = flow.get('id', 'Unknown')
            print(f"Processing: {flow_name} {flow_id}")

            try:
                # Create a directory for the flow_name if it doesn't exist
                if not os.path.exists(flow_name):
                    os.makedirs(flow_name)

                # Create the formatted flow dictionary
                formatted_flow = create_flow_dict(flow)

                # Save the JSON file in the flow_name directory with flow_id as the filename
                filename = f"{flow_name}/{flow_id}.json"
                with open(filename, 'w') as file:
                    json.dump(formatted_flow, file, indent=4)

            except IOError as e:
                print(f"Error writing file for flow '{flow_name} {flow_id}': {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from API response: {e}")

if __name__ == "__main__":
    backup_flows()