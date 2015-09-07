"""coprapi - Access to COPR REST API"""

import requests

# http://copr.fedoraproject.org/api/coprs/ignatenkobrain/

copr_url = "https://copr.fedoraproject.org"

#TODO: Sorting and tagging of COPR repos to control which ones show up in the
#      repo integrator selection list. For now, use Pete Hutterer's repos for
#      demo purposes
copr_api_path = "/api/coprs/whot/"
copr_display_path = "/coprs/whot/"

def get_repos():
    # Get remote repo info from COPR
    copr_info = requests.get(copr_url + copr_api_path).json()
    # COPR API doesn't currently report repo's display URLs
    repos = copr_info["repos"]
    for repo in repos:
        repo["display_url"] = copr_url + copr_display_path + repo["name"]
    return repos
