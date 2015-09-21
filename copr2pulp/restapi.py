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
    #TODO: Delete the Pulp repo when deleting the tracking feed
    #TODO: Support recreating the Pulp repo from the RepoFunnel state

    class Meta:
        model = models.Feed
        fields = ("id", "name", "url", "feed_url")

    def create(self, validated_data):
        feed_repo = models.Feed.objects.create(**validated_data)
        repo_name = "feed-" + validated_data["name"]
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        add_importer = pulpapi.set_feed(repo_name,
                                        validated_data["feed_url"])
        pulpapi.wait_for_task(add_importer["spawned_tasks"][0]["task_id"])
        pulp_importer = pulpapi.get_feed(repo_name)
        pulp_sync = pulpapi.start_sync(repo_name)
        #TODO: Store the pulp repo URL on the Feed instance
        feed_repo.save()
        # Show the Pulp details in the creation response
        self.fields["_debug_info"] = serializers.DictField(read_only=True)
        feed_repo._debug_info = {
            "pulp_repo_creation": pulp_repo,
            "pulp_importer": pulp_importer,
            "pulp_initial_sync": pulp_sync
        }
        return feed_repo

class FunnelSerializer(serializers.HyperlinkedModelSerializer):
    #TODO: Delete the Pulp repo when deleting the merge funnel
    feeds = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = models.Funnel
        fields = ("id", "name", "url", "feeds")

    def create(self, validated_data):
        funnel = models.Funnel.objects.create(**validated_data)
        repo_name = "funnel-" + validated_data["name"]
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        #TODO: Store the pulp repo URL on the Funnel instance
        funnel.save()
        #TODO: Specify which feeds to link. For now, always link all of them
        funnel.feeds = models.Feed.objects.all()
        #TODO: Configure content sync from the feed repo to the merge repo
        #TODO: Configure event listeners for feed repo updates
        funnel.save()
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
