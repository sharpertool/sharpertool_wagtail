#!/usr/bin/env bash

# Use an environment variable which works locally, but then on CircleCI use the global, default environment.
profilename=${AWS_PROFILE:-''}
if [[ ! -z "${profilename}" ]]
then
    export profile="--profile ${profilename}"
else
    export profile=''
fi

export sgname=${CIRCLECI_SG:-sg-8e3fa8f6}

