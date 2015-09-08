from django.shortcuts import render
from django.core.urlresolvers import reverse
from . import coprapi
from . import pulpapi

# Summary of local and remote repos
def repo_overview(request):
    # Get remote repo info from COPR
    sources = coprapi.get_repos()
    context = {"remote_repos": sources,
               "remote_repo_url": reverse("copr_repo-list"),
               "local_repo_url": reverse("pulp_repo-list")}
    return render(request, 'copr2pulp/sourcelist.html', context=context)
