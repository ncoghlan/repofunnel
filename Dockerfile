FROM fedora
MAINTAINER Nick Coghlan <ncoghlan@gmail.com>

WORKDIR /srv
RUN dnf -y install python3 && pyvenv "repofunnel" && dnf clean all

ADD . /srv/repofunnel/repofunnel
RUN cd "repofunnel" && source bin/activate && pip3 install -r "repofunnel/requirements.txt" && repofunnel/manage.py migrate


EXPOSE 8000
CMD source /srv/repofunnel/bin/activate && \
 /srv/repofunnel/repofunnel/manage.py runserver 0.0.0.0:8000
