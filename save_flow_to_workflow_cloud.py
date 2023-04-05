import os
import sys
import json
import requests

API_AUTH_KEY = os.getenv("KENDRAIO_WORKFLOW_CLOUD_AUTH_KEY")

def convert_get_to_post(get_response):
    """The format that is required by the POST
    endpoint is a bit different from what the
    GET endpoint provides, so we convert it a bit.
    """
    post_data = {
        "title": get_response["title"],
        "blocks": get_response["blocks"],
        "id": get_response["id"],
        "adapterName": get_response["adapterName"],
        "tags": get_response.get("tags", []),
    }
    return post_data

def update_flow(flow_name, flow_id, file_path):
    API_DOCUMENT_URL = f"https://app.kendra.io/api/{flow_name}/{flow_id}"
    print(f"Updating {API_DOCUMENT_URL}")
    with open(file_path, "r") as file:
        data = file.read()
    payload = json.loads(data)
    payload = convert_get_to_post(payload)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "authorization": "Bearer " + API_AUTH_KEY,
    }
    response = requests.request(
        "POST", API_DOCUMENT_URL, json=convert_get_to_post(payload), headers=headers
    )

    return response

if not API_AUTH_KEY:
    print('Set KENDRAIO_WORKFLOW_CLOUD_AUTH_KEY environment variable')
    sys.exit(1)


if len(sys.argv) == 2:
    # Get the file path from the command line
    file_path = sys.argv[1]

    # Extract flow_name and flow_id from the file path
    flow_name, flow_id_json = os.path.split(file_path)
    flow_id, _ = os.path.splitext(flow_id_json)

    response = update_flow(flow_name, flow_id, file_path)

    if 200 <= response.status_code < 300:
        # Success
        print("Success")
        sys.exit(0)
    elif 400 <= response.status_code < 500:
        # Client error
        print(f"Error: {response.status_code} {response.text}")
        sys.exit(1)
    elif 500 <= response.status_code < 600:
        # Server error7
        print(f"Error: {response.status_code} {response.text}")
        sys.exit(2)

else:
    print("Usage: python save_flow_to_workflow_cloud.py <file_path>")
    print("E.g: python save_flow_to_workflow_cloud.py bandsintown/selectArtist.json")
    sys.exit(2)
