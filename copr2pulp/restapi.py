from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets
from . import pulpapi
from . import coprapi
from . import models

#TODO: Automatically translate requests exceptions to error responses
#TODO: Override the default browsable API layout with the RepoFunnel layout

class FunnelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Funnel

class FunnelViewSet(viewsets.ModelViewSet):
    queryset = models.Funnel.objects.all()
    serializer_class = FunnelSerializer

# Hooking up the API URLs
def make_urls():
    router = routers.DefaultRouter()
    router.register( "funnel", FunnelViewSet)
    pulpapi.add_to_router(router, "pulp")
    coprapi.add_to_router(router, "copr")
    return router.urls
