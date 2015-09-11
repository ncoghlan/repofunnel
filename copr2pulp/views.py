from django.shortcuts import render
from django.core.urlresolvers import reverse
from . import coprapi
from . import pulpapi


# Summary of local and remote repos
def repo_overview(request):
    # Only remote repo source currently supported is COPR
    # Only local repo store currently supported is Pulp
    context = {"remote_repo_url": reverse("copr_repo-list"),
               "local_repo_url": reverse("pulp_repo-list")}
    return render(request, 'copr2pulp/sourcelist.html', context=context)

# Single page app for funnel management
def funnel_app(request):
    return render(request, 'copr2pulp/funnel_app.html')
