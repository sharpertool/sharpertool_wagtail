#!/bin/sh

mypath=$(dirname $0)

pushd django_root
coverage run --rcfile='${mypath}/../.coveragerc' manage.py test --keepdb
coverage html
popd

