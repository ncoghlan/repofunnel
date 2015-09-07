#!/usr/bin/env bash

LINKS="--link pulp_qpid:qpid --link pulp_db:db"

# try to start an existing one, and only run a new one if that fails
if docker start pulp_db 2> /dev/null
then
    echo pulp_db already exists
else
    echo running pulp_db
    docker run -d --name pulp_db -p 27017:27017 pulp/mongodb
fi

# try to start an existing one, and only run a new one if that fails
if docker start pulp_qpid 2> /dev/null
then
    echo pulp_qpid already exists
else
    echo running pulp_qpid
    docker run -d --name pulp_qpid -p 5672:5672 pulp/qpid
fi

# We create a data container to hold all of Pulp's working directories
MOUNTS="--volumes-from pulp_data -v /dev/log:/dev/log"
if docker start pulp_data 2> /dev/null
then
    echo Shared volumes for Pulp already created
else
    echo Launching Pulp data container
    # First we create a plain CentOS data container to own the volumes
    docker run -it $LINKS --name pulp_data \
                -v /var/log/httpd-pulpapi \
                -v /var/log/httpd-crane \
                -v /etc/pulp \
                -v /etc/pki/pulp \
                -v /var/lib/pulp \
                centos:7 echo "Created Pulp data container"
    # Then we run setup in the Pulp base container to initialise them
    docker run -it --rm $LINKS $MOUNTS --hostname pulpapi \
           pulp/base bash -c /setup.sh
fi

#TODO: Move these to a proper helper script...
PULP_DATA_VOLUMES=$(docker inspect pulp_data | python3 -c 'import json, sys, os.path; data = [os.path.dirname(vol["Source"]) for vol in json.loads(sys.stdin.read())[0]["Mounts"]];print(" ".join(data))')
for vol in $PULP_DATA_VOLUMES; do
    echo Setting context on $vol
    chcon -Rt svirt_sandbox_file_t $vol
done
PULPAPI_LOG=$(docker inspect pulp_data | python3 -c 'import json, sys; data = [vol["Source"] for vol in json.loads(sys.stdin.read())[0]["Mounts"] if vol["Destination"] == "/var/log/httpd-pulpapi"];print(data[0])')
CRANE_LOG=$(docker inspect pulp_data | python3 -c 'import json, sys; data = [vol["Source"] for vol in json.loads(sys.stdin.read())[0]["Mounts"] if vol["Destination"] == "/var/log/httpd-crane"];print(data[0])')

if docker start pulp_beat 2> /dev/null
then
    echo pulp_beat already exists
else
    echo running pulp_beat
    docker run $MOUNTS $LINKS -d --name pulp_beat pulp/worker beat
fi
if docker start pulp_resource_manager 2> /dev/null
then
    echo pulp_resource_manager already exists
else
    echo running pulp_resource_manager
    docker run $MOUNTS $LINKS -d --name pulp_resource_manager pulp/worker resource_manager
fi
if docker start pulp_worker1 2> /dev/null
then
    echo pulp_worker1 already exists
else
    echo running pulp_worker1
    docker run $MOUNTS $LINKS -d --name pulp_worker1 pulp/worker worker 1
fi
if docker start pulp_worker2 2> /dev/null
then
    echo pulp_worker2 already exists
else
    echo running pulp_worker2
    docker run $MOUNTS $LINKS -d --name pulp_worker2 pulp/worker worker 2
fi

# /var/lib/pulp is initially owned by root when mounted from a data container
if docker start pulpapi 2> /dev/null
then
    echo pulpapi already exists
else
    echo running pulpapi
    docker run $MOUNTS -v $PULPAPI_LOG:/var/log/httpd:Z $LINKS -d \
           --name pulpapi --hostname pulpapi -p 443:443 -p 80:80 \
           pulp/apache bash -c 'chown apache /var/lib/pulp && /run.sh'
fi
if docker start crane 2> /dev/null
then
    echo crane already exists
else
    echo running crane
    docker run $MOUNTS -v $CRANE_LOG:/var/log/httpd:Z -d \
           --name crane -p 5000:80 \
           pulp/crane-allinone bash -c 'chown apache /var/lib/pulp && /usr/sbin/httpd -D FOREGROUND'
fi

#docker run $MOUNTS -v $PULPAPI_LOG:/var/log/httpd:Z $LINKS -d pulp/apache bash
