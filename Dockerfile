# TODO: we need this to get Python 3 at least 3.4; remove when 21 becomes "the" fedora docker image
FROM fedora:21

WORKDIR /srv
RUN yum -y install python3 && pyvenv "repofunnel"

ADD . /srv/repofunnel/repofunnel
RUN cd "repofunnel" && source bin/activate && pip3 install -r "repofunnel/requirements.txt"


EXPOSE 8000
CMD source /srv/repofunnel/bin/activate && \
 /srv/repofunnel/repofunnel/manage.py runserver 0.0.0.0:8000
