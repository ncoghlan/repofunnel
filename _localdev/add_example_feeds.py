#!/usr/bin/python3
import requests

example_feeds = [
    {
        "name": "SCL-PostgreSQL94-EPEL-7-x86_64",
        "feed_url": "https://copr-be.cloud.fedoraproject.org/results/rhscl/rh-postgresql94/epel-7-x86_64/"
    },
    {
        "name": "SCL-Python34-EPEL-7-x86_64",
        "feed_url": "https://copr-be.cloud.fedoraproject.org/results/rhscl/rh-python34-el7/epel-7-x86_64/"
    },
    {
        "name": "PyPA-EPEL-7-x86_64",
        "feed_url": "https://copr-be.cloud.fedoraproject.org/results/pypa/pypa/epel-7-x86_64/"
    },
]

repofunnel_feeds_url = "http://localhost:8000/api/feed/"

for feed_settings in example_feeds:
    print(feed_settings)
    config = {
        "data": {
            "type": "feeds",
            "attributes": feed_settings
        }
    }

    reply = requests.post(repofunnel_feeds_url, json=config)
    reply.raise_for_status()
