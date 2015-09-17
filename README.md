RepoFunnel
==========

Uses Pulp to integrate disparate RPM repos into a single unified source.

This is achieved through two main concepts:

* Tracking Feeds: remote repos that are mirrored locally in Pulp
* Merge Funnels: local Pulp repos that merge content from multiple feeds

Current focus is on aggregrating independent COPR repos, allowing users to
select their enabled COPR repos online through the repo integrator service, and
have just a single remote repo to configure on their client systems, rather
than having a proliferation of individual COPR repos enabled.

This is pre-pre-alpha software, so the above is a statement of intent, rather
than a description of current functionality :)

Future Design Goals
-------------------

RepoFunnel is being developed as part of a larger proposal to introduce a
[Software Component Pipeline]
(https://fedoraproject.org/wiki/Env_and_Stacks/Projects/SoftwareComponentPipeline)
into the Fedora project.

While the specific focus of v1.0 development is a funnel from COPR RPM repos to
local Pulp RPM repos, there are two main axes of future generalisation to be
considered:

* more upstream sources (e.g. pypi.python.org, npm.org)
* alternate downstream targets (e.g. Pinterest's pinrepo)

This is deliberately similar to the arc of Pulp's development, which focused
specifically on RPM for the v1.0 release while keeping future support for
multiple content types in mind, and than on actually supporting plugins to the
repo management system for the v2.0 release.

Communications
--------------

GitHub issue tracker: https://github.com/ncoghlan/repofunnel/issues
Mailing list: https://lists.fedoraproject.org/pipermail/env-and-stacks/

Note that RepoFunnel doesn't have its own mailing list, and instead uses the
mailing list for the
[Fedora Environments & Stacks](https://fedoraproject.org/wiki/Env_and_Stacks)
working group.


Local Development
-----------------

Source repo: https://github.com/ncoghlan/repofunnel

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

To build the container image::

    sudo _localdev/build.sh .

To run an unmodified demo instance::

    sudo setenforce 0             # Sorry Dan...
    sudo _localdev/start_pulp.sh
    sudo _localdev/demo_server.sh

To run a development instance (for the first time)::

    sudo setenforce 0             # Sorry Dan...
    sudo _localdev/start_pulp.sh
    sudo _localdev/run_dev.sh .

To restart a stopped development instance::

    sudo setenforce 0             # Sorry Dan...
    sudo _localdev/start_pulp.sh  # This will restart existing containers
    sudo docker -ai start repofunnel_dev

These are just wrappers around particular Docker invocations, read the scripts
for details (aside from the one to start a local Pulp instance, they're all
single commands)

SELinux objects to the cross-linking between the Pulp containers, so that
currently needs to be switched off in order to run up the service locally.
Pulp's architecture is sufficiently complex that fixing this will likely
require switching to Kubernetes for local development rather than using plain
Docker.

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
