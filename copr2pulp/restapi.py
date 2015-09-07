from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets
from . import pulpapi
from . import coprapi

class PulpRepoSerializer(serializers.Serializer):
    details = serializers.DictField(read_only=True)

class PulpRepoViewSet(viewsets.ViewSet):
    def list(self, request):
        repos = [{"details": repo} for repo in pulpapi.get_repos()]
        return Response(PulpRepoSerializer(repos, many=True).data)

class CoprRepoSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    instructions = serializers.CharField(read_only=True)
    additional_repos = serializers.CharField(read_only=True)
    yum_repos = serializers.DictField(read_only=True)
    display_url = serializers.URLField(read_only=True)

class CoprRepoViewSet(viewsets.ViewSet):
    def list(self, request):
        repos = coprapi.get_repos()
        return Response(CoprRepoSerializer(repos, many=True).data)

def make_urls():
    router = routers.DefaultRouter()
    router.register("pulp", PulpRepoViewSet, base_name="pulp_repo")
    router.register("copr", CoprRepoViewSet, base_name="copr_repo")
    return router.urls