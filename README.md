Repo Integrator
===============

Uses Pulp to integrate disparate RPM repos into a single unified source.

Current focus is on aggregrating independent COPR repos, allowing users to select their enabled COPR repos online through the repo integrator service, and have just a single remote repo to configure on their client systems, rather than having a proliferation of individual COPR repos enabled.

This is pre-pre-alpha software, so the above is a statement of intent, rather than a description of current functionality :)


Tech stack
----------

This is a Django app, to align with the tech stack used by pulpproject.org

The copr2pulp Django app handles the aspects actually specific to this project.

`repo_integrator/Dockerfile` shows how to run a devel server as a container,
or locally in a virtual environment.