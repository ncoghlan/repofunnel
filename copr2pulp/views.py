from django.shortcuts import render
import requests

# http://copr.fedoraproject.org/api/coprs/ignatenkobrain/

copr_url = "https://copr.fedoraproject.org"

#TODO: Sorting and tagging of COPR repos to control which ones show up in the
#      repo integrator selection list. For now, use Pete Hutterer's repos for
#      demo purposes
copr_api_path = "/api/coprs/whot/"
copr_display_path = "/coprs/whot/"

#TODO: Configurable Pulp connectivity. For now, assume a local container
# service link called "pulpapi", and don't verify the HTTPS connection
pulp_url = "https://pulpapi/pulp"
pulp_api_path = "/api/v2/repositories/"

# Create your views here.
def home(request):
    # Get remote repo info from COPR
    copr_info = requests.get(copr_url + copr_api_path).json()
    # COPR API doesn't currently report repo's display URLs
    sources = copr_info["repos"]
    for repo in sources:
        repo["display_url"] = copr_url + copr_display_path + repo["name"]
    # Get local repo info from Pulp
    pulp_info = requests.get(pulp_url + pulp_api_path,
                             auth=('admin', 'admin'),
                             verify=False)
    if pulp_info.text == "not found":
        targets = []
    else:
        targets = pulp_info.json()
    # Display them both
    context = {"remote_repos": sources, "local_repos": targets}
    return render(request, 'copr2pulp/sourcelist.html', context=context)