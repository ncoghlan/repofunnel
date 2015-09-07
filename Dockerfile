FROM fedora:22
MAINTAINER Nick Coghlan <ncoghlan@gmail.com>

# TODO: Migrate over to S2I's separate builder image model
#       That should also avoid caching built wheel's inside the image

# Ensure Python 3 and pip for Python 3 are installed
RUN dnf -y install python3 python3-pip && \
    dnf clean all

# Install copr DNF plugin and install patternfly - remove the plugins in the end to keep image small
RUN dnf -y install dnf-plugins-core && \
    dnf -y copr enable patternfly/patternfly2 fedora-22-x86_64 && \
    dnf -y install patternfly2 && \
    dnf -y remove dnf-plugins-core && \
    dnf clean all

# Add the app sources
ADD . /srv/repofunnel/repofunnel

# Create the virtual env, activate it, install deps and run migration
WORKDIR /srv
RUN pyvenv "repofunnel" && \
    cd repofunnel && \
    source bin/activate && \
    pip3 install -r "repofunnel/requirements.txt" && \
    repofunnel/manage.py migrate

EXPOSE 8000
CMD source /srv/repofunnel/bin/activate && \
    /srv/repofunnel/repofunnel/manage.py runserver 0.0.0.0:8000
