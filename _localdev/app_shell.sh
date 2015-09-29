#!/usr/bin/env bash
docker exec -it repofunnel_dev \
  bash -c "source /srv/repofunnel/bin/activate && /opt/repofunnel/manage.py shell"
