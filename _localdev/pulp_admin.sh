#!/usr/bin/env bash
docker run -it --rm --link pulpapi:pulpapi pulp/admin-client bash
