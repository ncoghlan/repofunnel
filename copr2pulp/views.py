from django.shortcuts import render
from . import coprapi
from . import pulpapi

# Summary of local and remote repos
def repo_overview(request):
    # Get remote repo info from COPR
    sources = coprapi.get_repos()
    # Get local repo info from Pulp
    targets = pulpapi.get_repos()
    # Display them both
    context = {"remote_repos": sources, "local_repos": targets}
    return render(request, 'copr2pulp/sourcelist.html', context=context)