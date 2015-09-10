RepoFunnel
==========

Uses Pulp to integrate disparate RPM repos into a single unified source.

Current focus is on aggregrating independent COPR repos, allowing users to
select their enabled COPR repos online through the repo integrator service, and
have just a single remote repo to configure on their client systems, rather
than having a proliferation of individual COPR repos enabled.

This is pre-pre-alpha software, so the above is a statement of intent, rather
than a description of current functionality :)

Future Design Goals
-------------------

While the specific focus of v1.0 development is a funnel from COPR RPM repos to
Pulp RPM repos, there are two main axes of future generalisation to be
considered:

* more upstream sources (e.g. pypi.python.org, npm.org)
* alternate downstream targets (e.g. Pinterest's pinrepo)

This is deliberately similar to the arc of Pulp's development, which focused
specifically on RPM for the v1.0 release while keeping future support for
multiple content types in mind, and than on actually supporting plugins to the
repo management system for the v2.0 release.

Local Development
-----------------

Helper scripts for local development are in `_localdev`.

* `build.sh`: Builds the ncoghlan/repofunnel Docker image locally
* `start_pulp.sh`: Runs up a local containerised Pulp instance
* `pulp_admin.sh`: Starts a container to run the pulp-admin client against the
  local Pulp instance
* `demo_server.sh`: Runs the ncoghlan/repofunnel image against the local Pulp
  instance
* `run_dev.sh`: Runs the ncoghlan/repofunnel image, but runs the RepoFunnel web
  service itself from the source checkout on the host, rather than the version
  built into the container

To run an unmodified demo instance::

    sudo _localdev/start_pulp.sh
    sudo _localdev/demo_server.sh

To run a development instance::

    sudo _localdev/start_pulp.sh
    sudo _localdev/run_dev.sh $(pwd)/..

These are just wrappers around particular Docker invocations, read the scripts
for details (aside from the one to start a local Pulp instance, they're all
single commands)

SELinux objects to the cross-linking between the Pulp containers, so that
currently needs to be switched off in order to run up the service locally.

Tech stack
----------

This is a Django app, to align with the tech stack used by pulpproject.org

REST API design is taken from jsonapi.org, provided via Django REST Framework

Development relies on Docker containers (for both Pulp and RepoFunnel itself)

The copr2pulp Django app handles the aspects specific to retrieving repo details
from COPR and mapping them to local repos stored in Pulp (making both remote
data sources and local data stores pluggable is a desirable future enhancement,
but not a near term priority)

Front end styling relies on patternfly.org
