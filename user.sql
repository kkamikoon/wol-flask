CREATE USER 'wol'@'localhost' IDENTIFIED BY 'wol';
GRANT ALL PRIVILEGES ON wol.* TO 'wol'@'localhost';
FLUSH PRIVILEGES;
