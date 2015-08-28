#!/usr/bin/env bash
docker run -it --rm --link pulpapi:pulpapi -p 8000:8000 ncoghlan/repofunnel

