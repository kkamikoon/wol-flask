CREATE USER 'wol_example'@'localhost' IDENTIFIED BY 'wol_example';
GRANT ALL PRIVILEGES ON wol_example.* TO 'wol_example'@'localhost';
FLUSH PRIVILEGES;
