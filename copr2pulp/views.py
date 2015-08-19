from django.shortcuts import render
import requests

# http://copr.fedoraproject.org/api/coprs/ignatenkobrain/

copr_url = "https://copr.fedoraproject.org"

#TODO: Sorting and tagging of COPR repos to control which ones show up in the
#      repo integrator selection list. For now, use Pete Hutterer's repos for
#      demo purposes
api_path = "/api/coprs/whot/"
display_path = "/coprs/whot/"

# Create your views here.
def home(request):
    copr_info = requests.get(copr_url + api_path).json()
    # COPR API doesn't currently report repo's display URLs
    repos = copr_info["repos"]
    for repo in repos:
        repo["display_url"] = copr_url + display_path + repo["name"]
    context = {"remote_repos": repos}
    return render(request, 'copr2pulp/sourcelist.tmpl', context=context)