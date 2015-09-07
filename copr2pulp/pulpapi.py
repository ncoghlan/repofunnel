"""pulpapi - Access to Pulp REST API"""
import requests

#TODO: Configurable Pulp connectivity. For now, assume a local container
# service link called "pulpapi", and don't verify the HTTPS connection
pulp_url = "https://pulpapi/pulp"
pulp_api_path = "/api/v2/repositories/"

def get_repos():
    pulp_info = requests.get(pulp_url + pulp_api_path,
                             auth=('admin', 'admin'),
                             verify=False)
    if pulp_info.text == "not found":
        repos = []
    else:
        repos = pulp_info.json()
    return repos
