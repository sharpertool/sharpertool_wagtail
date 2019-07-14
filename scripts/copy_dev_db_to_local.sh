#!/usr/bin/env bash

server=localhost
dt=$(date '+%Y-%m-%d-%H_%M')
filename="sharpertool_dev_db_${dt}.sql"
backup_path=~/DropboxST/SharpertoolDev/database
full_filename=${backup_path}/${filename}
echo "Dumping to filename ${full_filename}"

#ls -al ${backup_path}
# Can can do this all in one command!
ssh st.root "pg_dump -h ${server} -U django_user sharpertool" > ${full_filename}

