#!/usr/bin/env bash
docker run -it --rm --name repofunnel_dev --link pulpapi:pulpapi -p 8000:8000 \
  -v $(realpath $1):/opt/repofunnel/:Z ncoghlan/repofunnel \
  bash -c "source /srv/repofunnel/bin/activate && \
           pip3 install -r '/opt/repofunnel/requirements.txt' && \
           /opt/repofunnel/manage.py makemigrations && \
           /opt/repofunnel/manage.py migrate && \
           /opt/repofunnel/manage.py runserver 0.0.0.0:8000"
