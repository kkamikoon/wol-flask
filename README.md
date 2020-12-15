# Ubuntu 18.04 ~ 

if you use ubuntu 18.04 or higher version of OS, you can follow these settings.

## APT setting
```bash
apt update -y
apt install -y apache2 letsencrypt redis python3-pip mysql-server libapache2-mod-wsgi-py3 libapache2-mod-log-sql-mysql
```

## Python3 requirements install
```bash
pip3 install redis flask flask_migrate flask_sqlalchemy Flask-Mail flask_caching flask_socketio flask-recaptcha sqlalchemy sqlalchemy_utils pymysql
```

## Create mysql default user
```bash
> sudo mysql -u root < user.sql
```
You should add your default account for wake on lan web server. this sql file makes __default mysql account__ on your mysql-server. If you wanna change your account, you have to change account informations on __`app/config.py`__ and __`user.sql`__

## Init Flask
```
python3 run.py
```
I recommand the reverse proxy setting. If you use web server like apache2 or nginx, you need to use wsgi( or uwsgi) or gunicorn or something.


# Apache2 Service(Option - Recommand)

## Add Apache2 envvar value
```
...
export WOL_DIR=/var/www/wol/
...
```
This is apache2 environment value that it helps you to configure your config file(like wol.conf). This value can be written on __`/etc/apache2/envvar`__.

## Add apache2 module
```bash
sudo a2enmod rewrite
sudo a2enmod wsgi
sudo a2enmod ssl
```
You should enable these modules, if you want to init apache2 service.

> rewrite : One of apache2 module what makes your request forward to other URL or File.
>
> * RewriteEngine
> * RewriteCond
> * RewriteRule
> * etc.
>
> wsgi : One of apache2 module that it makes you can use 'kind of WSGI configuration' on your apache2 config files. This module can install using apt-get(or apt).
>
> library name : __`libapache2-mod-wsgi-py3`__.
>
> * WSGIScriptAlias
> * WSGIDaemonProcess
> * WSGIApplicationGroup
> * etc.
>
> ssl : One of apache2 module that it makes you can use SSL configuration in your apache2 config files.
>
> * SSLCertificateFile
> * SSLCertificateKeyFile
> * SSLCertificateChainFile
> * etc.

## Add apache2 conf
```bash
sudo a2ensite wol
sudo a2dissite 000-default
```
Your configuration file(wol.conf) should be ensited, and should dissite default config file(000-default.conf)
