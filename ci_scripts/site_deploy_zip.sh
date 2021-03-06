#!/bin/bash

zipfile=$1
VERSION=$2
APPPATH=${APPPATH:-/home/django/sharpertool}
zipdir=${APPPATH}/zipdir
deploydir=${APPPATH}/deploy
excludefile=${APPPATH}/deplay_exclude.lst

echo "unzip ${zipfile} to ${zipdir}"
rm -rf ${zipdir}
mkdir -p ${zipdir}
mkdir -p ${deploydir}
pushd ${zipdir}
unzip -uoq ${deploydir}/${zipfile}
popd

cd ${APPPATH}

echo "use rsync to synchronize the two paths"
if [[ -e ${excludefile} ]]
then
    rsync -av --delete --exclude-from ${excludefile} ${zipdir}/ .
else
    echo "Cannot use rsync if the excludefile does not exist!"
    exit 2
fi

# Put site into maintenance mode
touch ${APPPATH}/maintenance.on

echo "Update requirements"
.venv3/bin/pip install --upgrade pip
.venv3/bin/pip install --upgrade -r requirements/prod.txt

echo -e "\n Collecting updated statics.."
./manage collectstatic --noinput

# Show any pending migrations
./manage showmigrations | grep "\[ \]\|^[a-z]" | grep "[ ]" -B 1

# Run migrations
./manage migrate --noinput

echo "Updating APP_VERSION to match production version"
cat << EOF >| .versions.env
# Versions for app monitoring
APP_VERSION=${VERSION}
DJANGO_SENTRY_RELEASE=${VERSION}
SERVER_VERSION=${VERSION}

EOF

# Update app directory user and group values
sudo chown -R django:www-data ${APPPATH}

echo -e "\n Reloading uWSGI web service.."

# Reload with reload.me
touch reload.me

rm -f ${APPPATH}/maintenance.on

