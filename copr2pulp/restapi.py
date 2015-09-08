from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import routers
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from . import pulpapi
from . import coprapi

# Local Pulp repos
class PulpRepoSerializer(serializers.Serializer):
    repo_id = serializers.CharField()
    display_name = serializers.CharField()
    details = serializers.DictField(read_only=True)

    def create(self, validated_data):
        repo = pulpapi.create_repo(**validated_data)
        return repo

class PulpRepoViewSet(viewsets.ViewSet):
    serializer_class = PulpRepoSerializer

    def list(self, request):
        repos = pulpapi.iter_repos()
        return Response(self.serializer_class(repos, many=True).data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        repo = serializer.save()
        return Response(self.serializer_class(repo).data,
                        status=status.HTTP_201_CREATED)


# Upstream COPR repos
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

# Hooking up the API URLs
def make_urls():
    router = routers.DefaultRouter()
    router.register("pulp", PulpRepoViewSet, base_name="pulp_repo")
    router.register("copr", CoprRepoViewSet, base_name="copr_repo")
    return router.urls