#!/usr/bin/env bash
set -e

# Check if we are in the correct directory before running commands.
if [[ ! $(pwd) == '/home/meetingcenter/meeting-center' ]]; then
	echo "Running in the wrong directory...switching to..."
	cd /home/meetingcenter/meeting-center
fi

python3 manage.py migrate
python3 manage.py collectstatic


exec $@