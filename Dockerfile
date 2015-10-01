FROM fedora:22
MAINTAINER Nick Coghlan <ncoghlan@gmail.com>

# TODO: Migrate over to S2I's separate builder image model (once that exists)
#       That should also avoid caching built wheel's inside the image

# Install Python 3 and pip for Python 3 to handle the back end REST service
# Also install Node.js, npm & Bower to manage the front end web UI
RUN dnf -y install python3 python3-pip nodejs npm git && \
    dnf clean all
RUN npm install -g bower

# Add the app sources
ADD . /srv/repofunnel

# Create the virtual env, activate it, install deps and ensure migrations exist
WORKDIR /srv
RUN pyvenv repofunnel && \
    cd repofunnel && \
    source bin/activate && \
    pip3 install -r requirements.txt && \
    bower --allow-root install patternfly angular-patternfly && \
    ./manage.py makemigrations

# Always run migrations before starting server
EXPOSE 8000
CMD source /srv/repofunnel/bin/activate && \
    /srv/repofunnel/manage.py migrate && \
    /srv/repofunnel/manage.py runserver 0.0.0.0:8000
