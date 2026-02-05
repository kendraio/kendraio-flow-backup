import json
from pathlib import Path

import requests

FLOWS_URL = "https://app.kendra.io/flows/"

response = requests.get(FLOWS_URL, timeout=60)
response.raise_for_status()
flows = response.json()

metadata_order = [
    "id",
    "adapter",
    "org",
    "workflowId",
    "adapterName",
    "created",
    "tags",
    "updated",
    "modified",
    "title",
]
metadata_set = set(metadata_order)

for flow in flows:
    flow_name = flow.get("adapterName") or "default"
    flow_id = flow.get("id") or flow.get("workflowId")
    assert flow_id, f"Missing id/workflowId in flow: {flow!r}"

    print(f"{flow_name} {flow_id}")

    Path(flow_name).mkdir(parents=True, exist_ok=True)

    ordered_flow = {}
    for key, value in flow.items():
        if key in metadata_set:
            continue
        ordered_flow[key] = value

    for key in metadata_order:
        if key in flow and flow[key] is not None:
            ordered_flow[key] = flow[key]

    filename = Path(flow_name) / f"{flow_id}.json"
    filename.write_text(json.dumps(ordered_flow, indent=4), encoding="utf-8")
