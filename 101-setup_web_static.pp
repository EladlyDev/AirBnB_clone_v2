# Seting up the web server for the deployment of web_static (task 0)

# Installing nginx...
exec {'apt-update':
  command => '/usr/bin/apt-get update -y',
}

exec {'nginx-install':
  command => '/usr/bin/apt-get install nginx -y',
  require => Exec['apt-update'],
}

# The files herarichy
$files=['/data', '/data/web_static', '/data/web_static/releases',
        '/data/web_static/shared', '/data/web_static/releases/test']
file {$files:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Sample to test
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Hello Holberton!',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Symi link to the html
file {'/data/web_static/current':
  ensure  => 'link',
  force   => true,
  target  => '/data/web_static/releases/test/',
  require => File['/data/web_static/releases/test/'],
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Configuring nginx to serve the /data/web_static/current
$conf='
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
'
file {'/etc/nginx/sites-available/default':
  ensure  => present,
  content => $conf,
  require => Exec['nginx-install'],
  notify  => Service['nginx'],
}

# Restarting nginx
service {'nginx':
  ensure => running,
  enable => true,
}
