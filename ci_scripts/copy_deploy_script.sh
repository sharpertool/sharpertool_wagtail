#!/bin/bash

SRC_SCRIPT={SRC_SCRIPT:-site_deploy_zip.sh}
num_tries=10
retries=${num_tries}
false
stat=$?
while [[ ${stat} -ne 0 && ${retries} -gt 0 ]]
do
    echo "Copy deploy script to remote host"
    scp -o ConnectTimeout=5 ./ci_scripts/${SRC_SCRIPT} deploy_host:${BASE_DIR}/site_deploy_zip.sh
    stat=$?

    ((retries -= 1))
    if [[ ${retries} -gt 0 ]];then
        echo "I have ${retries} retries left"
    fi
done

if [[ ${stat} -ne 0 ]];then
    echo "The operation failed after ${num_tries} retries"
fi
# If the first scp failed, this will fail, otherwise it should pass
scp -o ConnectTimeout=5 ./ci_scripts/deploy_exclude.lst deploy_host:${BASE_DIR}

