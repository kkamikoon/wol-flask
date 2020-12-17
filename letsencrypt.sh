WOL_DOMAIN="[your-domain]";
WOL_DIR="/var/www/wol";

systemctl stop apache2

rm -rf ${WOL_DIR}/ssl/${WOL_DOMAIN};
rm -rf /etc/letsencrypt/archive/${WOL_DOMAIN};
rm -rf /etc/letsencrypt/live/${WOL_DOMAIN};
rm -rf /etc/letsencrypt/renewal/${WOL_DOMAIN};

letsencrypt certonly --standalone -d ${WOL_DOMAIN};

cp -r /etc/letsencrypt/archive/${WOL_DOMAIN}/* ${WOL_DIR}/ssl;

systemctl start apache2
