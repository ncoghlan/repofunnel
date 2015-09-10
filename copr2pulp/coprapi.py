"""coprapi - Access to COPR REST API"""
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
import requests

# Client access to the remote COPR API
copr_url = "https://copr.fedoraproject.org"

#TODO: Sorting and tagging of COPR repos to control which ones show up in the
#      repo funnel selection list. For now, use Pete Hutterer's repos for
#      demo purposes
copr_api_path = "/api/coprs/whot/"
copr_display_path = "/coprs/whot/"

def iter_repos():
    # Get remote repo info from COPR
    copr_reply = requests.get(copr_url + copr_api_path)
    copr_reply.raise_for_status()
    raw_repos = copr_reply.json()["repos"]
    for repo in repos:
        # COPR API doesn't currently report repo's display URLs
        repo["display_url"] = copr_url + copr_display_path + repo["name"]
        yield repo

# Local REST API proxy for remote COPR API
COLLECTION_NAME = 'copr_repo'
def add_to_router(router, prefix):
    router.register(prefix, CoprRepoViewSet, base_name=COLLECTION_NAME)

class CoprRepoSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    instructions = serializers.CharField(read_only=True)
    additional_repos = serializers.CharField(read_only=True)
    yum_repos = serializers.DictField(read_only=True)
    display_url = serializers.URLField(read_only=True)

class CoprRepoViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(CoprRepoSerializer(iter_repos(), many=True).data)

