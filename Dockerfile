# TODO: we need this to get Python 3 at least 3.4; remove when 21 becomes "the" fedora docker image
FROM fedora:21

WORKDIR /srv
RUN yum -y install python3 && pyvenv "repo_integrator"

ADD . /srv/repo_integrator/repo_integrator
RUN cd "repo_integrator" && source bin/activate && pip3 install -r "repo_integrator/requirements.txt"


EXPOSE 8000
CMD source /srv/repo_integrator/bin/activate && \
 /srv/repo_integrator/repo_integrator/manage.py runserver 0.0.0.0:8000
