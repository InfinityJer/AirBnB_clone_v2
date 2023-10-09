#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo 'Holberton School' | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/

sudo sed -i '/:80 default_server/a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-enabled/default

sudo service nginx restart
