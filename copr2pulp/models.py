from django.db import models

class Feed(models.Model):
    # TODO: support multiple repo types
    # TODO?: Garbage collection of no longer referenced feed repos
    name = models.CharField(max_length=30, unique=True)
    pulp_repo = models.CharField(max_length=35, null=True)
    feed_url = models.URLField(unique=True)
    # + funnel_set from related field in Funnel

class Funnel(models.Model):
    # TODO: Notions of funnel ownership and ACLs
    name = models.CharField(max_length=30, unique=True)
    pulp_repo = models.CharField(max_length=40, null=True)
    funnel_url = models.URLField(unique=True, null=True)
    feeds = models.ManyToManyField(Feed)
