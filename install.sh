#!/bin/bash

PID=$(pgrep -f /opt/salic/salic-api/run.py)
PROJECT_PATH="`dirname \"$0\"`"


echo "Syncing project..."
cd $PROJECT_PATH
git checkout install.sh
git checkout master &> /dev/null
git fetch &> /dev/null
git pull origin master
echo "Repository Updated"

if [ $PID ]; then

    echo "Stopping services"
    /etc/init.d/salic-api stop
fi


echo "Installing SALIC API..."

echo "Installing dependencies:"
apt-get update && apt-get install python-dev python-pip freetds-dev libxml2-dev libxslt1-dev libz-dev
pip install -r salic-api/requirements.txt

echo "Dependencies installed"


if [ -d "/opt/salic/salic-api/" ]; then
    if [ -f "/opt/salic/salic-api/app/deployment.cfg" ]; then

        echo "Moving temporarily old configuration files for a new instance..."
        cp -av /opt/salic/salic-api/app/deployment.cfg /tmp/
        old_config=true
    fi

    echo "Cleaning up old project..."
    rm -r /opt/salic/salic-api/
fi


if [ -e "/etc/init.d/salic-api" ]; then

    echo "Cleaning up old daemon..."
    rm /etc/init.d/salic-api
fi



echo "Copying files..."
mkdir -p /opt/salic/salic-api/
mkdir /opt/salic/salic-api/log
cp -r salic-api/* /opt/salic/salic-api/
touch /opt/salic/salic-api/log/salic_api.log
cp swagger_specification_PT-BR.json /opt/salic/salic-api/resources/api_doc/
cp startup-script /etc/init.d/salic-api

if [ $old_config ]; then
    echo "Moving back old configuration files.."
    mv /tmp/deployment.cfg /opt/salic/salic-api/app/

    echo "ENVIRONMENT = \"deployment.cfg\" " > /opt/salic/salic-api/app/general_config.py
fi

echo "Done copying..."



chmod +x /etc/init.d/salic-api

echo "SALIC API has been successfuly installed"
echo "If it is your first installation edit the file /opt/salic/salic-api/app/deployment.cfg according to your needs"
