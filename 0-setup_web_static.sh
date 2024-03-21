#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

# installing nginx
sudo apt-get update -y
sudo apt-get install nginx -y

# creating the folder and its required parents (if any)
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
# sample index.html to test
echo "Hello Holberton!"  | sudo tee /data/web_static/releases/test/index.html > /dev/null
# symbolic link to the html samples
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# giving user `ubuntu` the ownership
sudo chown -hR ubuntu:ubuntu /data

# configuring nginx to serve the /data/web_static/current
sudo bash -c 'cat << EOF > /etc/nginx/sites-enabled/default
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        server_name _;

        location / {
                try_files \$uri \$uri/ =404;
        }

        location /hbnb_static {
                 alias /data/web_static/current/;
		 index index.html;
        }

        error_page 404 /404.html;

        location = /404.html {
                root /usr/share/nginx/html;
                internal;
        }

        location /redirect_me {
                return 301 https://www.youtube.com/watch?v=QH3-TGUlwu4;
        }
}
EOF'

# restart nginx
sudo service nginx restart
