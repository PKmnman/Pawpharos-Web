#!/bin/bash

#############################################################################
# Petpharos Web Server Setup Script
# Author: Gary Reeves
# Date: 1/25/2022
# Desc: A script that automates the process of setting up the Petpharos web 
# application on a remote virtual server.
#############################################################################

# Define Variables

# Use an environment variable to see if we've already installed everything
if [ -n ${PAWPHAROS_INSTALLED:-''} ]
then
    export PAWPHAROS_INSTALLED=False
fi

DJANGO_PROJECT=pawpharos
PROJECT_REPOSITORY=git@github.com:PKmnman/PetBeaconWebsite.git

DJANGO_USER=pawpharos
DJANGO_GROUP=${DJANGO_USER}

PAWPHAROS_SETTINGS=/etc/opt/$DJANGO_PROJECT
PAWPHAROS_DATA=/var/opt/$DJANGO_PROJECT

DOMAIN=pawpharos.com

#apt -y update && apt -y upgrade

precompile () {
	/opt/$DJANGO_PROJECT/venv/bin/python -m compileall -x /opt/$DJANGO_PROJECT/venv/ /opt/$DJANGO_PROJECT
}

collect-static () {
    PYTHONPATH=/etc/opt/$DJANGO_PROJECT:/opt/$DJANGO_PROJECT /opt/$DJANGO_PROJECT/venv/bin/python /opt/$DJANGO_PROJECT/manage.py collectstatic --settings=settings
}

install-apache () {
    apt -y install apache2

    cat > /etc/apache2/sites-available/$DOMAIN.conf << EOF
<VirtualHost *:80>
    ServerName ${DOMAIN}
    ServerAlias www.${DOMAIN}
    DocumentRoot /var/www/${DOMAIN}
    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyPass / http://localhost:8000/
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "http"
    Alias /static/ /var/cache/${DJANGO_PROJECT}/static/
    <Directory /var/cache/${DJANGO_PROJECT}/static/>
        Require all granted
    </Directory>
    Alias /media/ /var/opt/${DJANGO_PROJECT}/media/
    <Directory /var/opt/${DJANGO_PROJECT}/media/>
        Require all granted
    </Directory>
</VirtualHost>
EOF
    pushd $PWD
    cd /etc/apache2/sites-enabled
    ln -s ../sites-available/$DOMAIN.conf
    popd | cd

    a2enmod proxy proxy_http headers

    service apache2 reload

}

uninstall-apache() {
    service apache2 stop
    rm /etc/apache2/sites-available/pawpharos.com.conf
    apt -y remove apache2
}

setup () {
	apt update && apt -y upgrade
	apt install git python virtualenvwrapper 

    # Add user for running the program
	adduser --system --home=/var/opt/$DJANGO_PROJECT --no-create-home --disabled-password --group --shell=/bin/bash $DJANGO_USER

	# Clone the repository
	git clone $PROJECT_REPOSITORY /opt/$DJANGO_PROJECT

	# Setup virtual python environment
	virtualenv --system-site-packages --python=/bin/python3 /opt/$DJANGO_PROJECT/venv
	/opt/$DJANGO_PROJECT/venv/bin/pip install -r /opt/$DJANGO_PROJECT/requirements.txt

	# Setup data, log, and settings Directories
	mkdir -p $PAWPHAROS_DATA
	chown $DJANGO_USER $PAWPHAROS_DATA

	mkdir -p /var/log/$DJANGO_PROJECT
	chown $DJANGO_USER /var/log/$DJANGO_PROJECT

	mkdir $PAWPHAROS_SETTINGS
    chgrp $DJANGO_GROUP /etc/opt/$DJANGO_PROJECT
    chmod u=rwx,g=rx,o= /etc/opt/$DJANGO_PROJECT

    # Create the settings.py file
	cat > "$PAWPHAROS_SETTINGS/settings.py" << EOF
from PetBeaconWebsite.settings import *

DEBUG = True
ALLOWED_HOSTS = ['${DOMAIN}', 'www.${DOMAIN}']
DATABASES = {
    default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'var/opt/${DJANGO_PROJECT}/${DJANGO_PROJECT}.db',
    }
}

STATIC_ROOT = 'var/cache/$DJANGO_PROJECT/static/'
STATIC_URL = '/static/'
EOF

    # Compile whenever we update our settings
    precompile
    collect-static

    # Install & Configure Apache

    # Install & Configure Gunicorn
}

uninstall () {


    rm -r $PAWPHAROS_SETTINGS
    rm -r $PAWPHAROS_DATA
    rm -r /var/log/$DJANGO_PROJECT
    rm -r /opt/$DJANGO_PROJECT

    userdel $DJANGO_USER
    groupdel $DJANGO_GROUP

    uninstall-apache
} 

case "${1}" in
    "install-apache") 
        echo "Installing apache..."
        install-apache
    ;;
    "setup")
        echo "Performing web server setup..."
        setup
    ;;
    *)
        echo "No commands matching ${1}"
    ;;
esac
