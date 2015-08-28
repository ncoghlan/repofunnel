#!/usr/bin/env bash
docker run -it --rm --name repofunnel_dev --link pulpapi:pulpapi -p 8000:8000 -v $1:/opt/repofunnel/:Z ncoghlan/repofunnel bash -c "source /srv/repofunnel/bin/activate && /opt/repofunnel/repofunnel/manage.py migrate && /opt/repofunnel/repofunnel/manage.py runserver 0.0.0.0:8000"
