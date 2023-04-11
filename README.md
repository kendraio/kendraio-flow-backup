This repository contains backups of the Flows for the Kendraio Workflow Cloud.
Until we have versioning implemented, this is a good way to keep track of changes.
It is not the intended to replace the Workflow Cloud for serving Flows.

download_flows_from_workflow_cloud.py will download the latest version of Flows from the Workflow Cloud and save them to the directory of the Flow name.

save_flow_to_workflow_cloud.py will upload a Flow to the Workflow Cloud. It requires KENDRAIO_WORKFLOW_CLOUD_AUTH_KEY to be set in the environment.


After downloading and modifying JSON of Flows, I updated each bandsintown Flow in one go:
for file in bandsintown/*; do python save_flow_to_workflow_cloud.py "$file"; done