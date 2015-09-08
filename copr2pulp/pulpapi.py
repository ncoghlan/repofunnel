"""pulpapi - Access to Pulp REST API"""
import requests

#TODO: Configurable Pulp connectivity. For now, assume a local container
# service link called "pulpapi", and don't verify the HTTPS connection
pulp_url = "https://pulpapi/pulp"
pulp_api_path = "/api/v2/repositories/"

def _convert_repo(repo):
    return {"repo_id":repo["id"],
            "display_name":repo["display_name"],
            "details": repo,
            }

def iter_repos():
    pulp_info = requests.get(pulp_url + pulp_api_path,
                             auth=('admin', 'admin'),
                             verify=False)
    if pulp_info.text == "not found":
        raw_repos = []
    else:
        raw_repos = pulp_info.json()
    for repo in raw_repos:
        yield _convert_repo(repo)

def create_repo(repo_id, display_name):
    details = {"id":repo_id, "display_name":display_name}
    pulp_reply = requests.post(pulp_url + pulp_api_path,
                               auth=('admin', 'admin'),
                               json=details,
                               verify=False)
    pulp_reply.raise_for_status()
    return _convert_repo(pulp_reply.json())
