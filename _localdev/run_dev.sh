#!/usr/bin/env bash
docker run -it --rm --name repofunnel_dev --link pulpapi:pulpapi -p 8000:8000 \
  -e "DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')" \
  -v $(realpath $1):/opt/repofunnel/:Z ncoghlan/repofunnel \
  bash -c "source /srv/repofunnel/bin/activate && \
           pip3 install -r '/opt/repofunnel/requirements.txt' && \
           /opt/repofunnel/manage.py makemigrations && \
           /opt/repofunnel/manage.py migrate && \
           /opt/repofunnel/manage.py runserver_plus 0.0.0.0:8000"
