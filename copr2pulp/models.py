from django.db import models

class Feed(models.Model):
    # TODO: support multiple repo types
    # TODO: Garbage collection of no longer referenced feed repos
    name = models.CharField(max_length=30)
    pulp_repo = models.CharField(max_length=35, null=True)
    feed_url = models.URLField()
    # + funnel_set from related field in Funnel

class Funnel(models.Model):
    # TODO: Notions of funnel ownership and ACLs
    name = models.CharField(max_length=30)
    pulp_repo = models.CharField(max_length=40, null=True)
    feeds = models.ManyToManyField(Feed)
