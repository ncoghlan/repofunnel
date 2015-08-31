FROM fedora:22
MAINTAINER Nick Coghlan <ncoghlan@gmail.com>

# Install python3 and create virtual environment for the app
RUN dnf -y install python3 && \
    pyvenv "repofunnel" && \
    dnf clean all

# Install copr DNF plugin and install patternfly - remove the plugins in the end to keep image small
RUN dnf -y install dnf-plugins-core && \
    dnf -y copr enable patternfly/patternfly2 fedora-22-x86_64 && \
    dnf -y install patternfly2 && \
    dnf -y remove dnf-plugins-core && \
    dnf clean all

# Add the app sources
ADD . /srv/repofunnel/repofunnel

# Enter the virtual env, activate it, install deps and run migration
WORKDIR /srv/repofunnel
RUN source bin/activate && pip3 install -r "repofunnel/requirements.txt" && repofunnel/manage.py migrate

EXPOSE 8000
CMD source /srv/repofunnel/bin/activate && \
 /srv/repofunnel/repofunnel/manage.py runserver 0.0.0.0:8000
