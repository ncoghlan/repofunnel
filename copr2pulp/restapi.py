from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets
from . import pulpapi
from . import coprapi
from . import models

#TODO: Automatically translate requests exceptions to error responses
#TODO: Override the default browsable API layout with the RepoFunnel layout

#=============
# Serializers
#=============

class FeedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Feed
        read_only_fields = ('funnel_set',)

    def create(self, validated_data):
        feed_repo = models.Feed.objects.create(**validated_data)
        repo_name = "feed-" + validated_data["name"]
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        #TODO: Actually configure the repo feed
        feed_repo.save()
        return feed_repo

class FunnelSerializer(serializers.HyperlinkedModelSerializer):
    #TODO: Report the source feed URLs merged by the funnel

    class Meta:
        model = models.Funnel
        read_only_fields = ('feeds',)

    def create(self, validated_data):
        funnel = models.Funnel.objects.create(**validated_data)
        repo_name = "funnel-" + validated_data["name"]
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        funnel.save()
        # TODO: Hook up demo feed repos
        # https://copr-be.cloud.fedoraproject.org/results/whot/libevdev/epel-7-x86_64/
        # https://copr-be.cloud.fedoraproject.org/results/whot/libinput-epel7/epel-7-x86_64/
        return funnel

#==========
# ViewSets
#==========

class FeedViewSet(viewsets.ModelViewSet):
    queryset = models.Feed.objects.all()
    serializer_class = FeedSerializer

class FunnelViewSet(viewsets.ModelViewSet):
    queryset = models.Funnel.objects.all()
    serializer_class = FunnelSerializer

#=========================
# Hooking up the API URLs
#=========================
def make_urls():
    router = routers.DefaultRouter()
    router.register( "feed", FeedViewSet)
    router.register( "funnel", FunnelViewSet)
    pulpapi.add_to_router(router, "pulp")
    coprapi.add_to_router(router, "copr")
    return router.urls
