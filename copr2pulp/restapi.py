from rest_framework.response import Response
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
    _pulp_prefix = "feed-"

    class Meta:
        model = models.Feed
        fields = ("id", "name", "url", "feed_url")

    def create(self, validated_data):
        feed_repo = models.Feed.objects.create(**validated_data)
        repo_name = self._pulp_prefix + validated_data["name"]
        # Create a new feed repository in Pulp
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        # Configure the remote content feed
        add_importer = pulpapi.set_feed(repo_name,
                                        validated_data["feed_url"])
        pulpapi.wait_for_task(add_importer["spawned_tasks"][0]["task_id"])
        pulp_importer = pulpapi.get_feed(repo_name)
        # Start the initial content sync
        pulp_sync = pulpapi.start_sync(repo_name)
        # Save the new tracking feed to the database
        feed_repo.pulp_repo = repo_name
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
    _pulp_prefix = "funnel-"
    feeds = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = models.Funnel
        fields = ("id", "name", "url", "feeds", "funnel_url")
        read_only_fields = ("funnel_url",)

    def create(self, validated_data):
        funnel = models.Funnel.objects.create(**validated_data)
        repo_name = self._pulp_prefix + validated_data["name"]
        # Create a new funnel RPM repository in Pulp
        pulp_repo = pulpapi.create_repo(repo_name, repo_name)
        add_importer = pulpapi.set_feed(repo_name)
        pulpapi.wait_for_task(add_importer["spawned_tasks"][0]["task_id"])
        pulp_importer = pulpapi.get_feed(repo_name)
        # Configure the funnel for publishing
        pulp_distributor, funnel_url = pulpapi.set_target(repo_name)
        funnel.funnel_url = funnel_url
        # Merge content into the funnel from the feed repositories
        #TODO: Specify which feeds to link. For now, always link all of them
        feeds = models.Feed.objects.all()
        pulp_merges = {}
        for feed in feeds.all():
            #TODO: Support filtering merged content
            source_id = feed.pulp_repo
            pulp_merges[source_id] = pulpapi.start_merge(source_id, repo_name)
            #TODO: Configure event listeners for feed repo updates
        # Start the initial repo publication
        pulp_publish = pulpapi.start_publish(repo_name)
        # Save the new merge funnel to the database
        funnel.feeds = feeds
        funnel.pulp_repo = repo_name
        funnel.save()
        # Show the Pulp details in the creation response
        self.fields["_debug_info"] = serializers.DictField(read_only=True)
        funnel._debug_info = {
            "pulp_repo_creation": pulp_repo,
            "pulp_importer": pulp_importer,
            "pulp_initial_merges": pulp_merges,
            "pulp_distributor": pulp_distributor,
            "pulp_publish": pulp_publish,
        }
        return funnel

#==========
# ViewSets
#==========

class _DestroyPulpRepoMixin:
    def destroy(self, request, *, pk):
        instance = self._model_manager.get(pk=pk)
        repo_name = instance.name
        pulp_repo_id = instance.pulp_repo
        if pulp_repo_id is None:
            pulp_repo_id = self.serializer_class._pulp_prefix + repo_name
        pulp_delete = pulpapi.delete_repo(pulp_repo_id)
        super().destroy(request, pk=pk)
        details = {
            "id": pk,
            "name": repo_name,
            "_debug_info": {"pulp_repo_deletion": pulp_delete}
        }
        return Response(details)

class FeedViewSet(_DestroyPulpRepoMixin, viewsets.ModelViewSet):
    _model_manager = models.Feed.objects
    queryset = _model_manager.all()
    serializer_class = FeedSerializer

class FunnelViewSet(_DestroyPulpRepoMixin, viewsets.ModelViewSet):
    _model_manager = models.Funnel.objects
    queryset = _model_manager.all()
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
