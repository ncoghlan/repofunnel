from django.db import models

class Funnel(models.Model):
    name = models.CharField(max_length=30)
    # TODO: record local target repo by type and URL
    # TODO: record remote source repos by type and URL
    # TODO: Notions of repo ownership and ACLs
