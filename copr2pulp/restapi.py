from rest_framework import routers
from . import pulpapi
from . import coprapi

#TODO: Automatically translate requests exceptions to error responses
#TODO: Override the default browsable API layout with the service layout

# Hooking up the API URLs
def make_urls():
    router = routers.DefaultRouter()
    pulpapi.add_to_router(router, "pulp")
    coprapi.add_to_router(router, "copr")
    return router.urls
