use wol_example;

-- users    dummy
INSERT INTO users(  uid, email, password)       VALUES("kkamikoon",     "kkamikoon@gmail.com", "0bdf0332166a949291a3dd410046be5269dbcff5b7b9edbd897df6d9ac5e4ec855e491c6fd150ad9bf4af1d353e0624f3427ec843e0c4a2319349396efb23989");

-- configs  dummy
INSERT INTO configs(key, value)                 VALUES("wol_domain",    "wol.example.kkamikoon.com");
INSERT INTO configs(key, value)                 VALUES("domain_check",  1);
INSERT INTO configs(key, value)                 VALUES("title_tag",     "KKAMIKOON - WOL -Example");
INSERT INTO configs(key, value)                 VALUES("main_title",    "KKAMIKOON - WOL -Example");

-- hosts    dummy
INSERT INTO configs(name, mac, ip, broadcast)   VALUES("[ALL]",         "FF:FF:FF:FF:FF:FF", "255.255.255.255", 1);
INSERT INTO configs(name, mac, ip, broadcast)   VALUES("ESXI Server 1", "00:00:00:00:00:01", "192.168.0.1"    , 0);
INSERT INTO configs(name, mac, ip, broadcast)   VALUES("My Laptop",     "00:00:00:00:00:02", "192.168.0.2"    , 0);
INSERT INTO configs(name, mac, ip, broadcast)   VALUES("My Desktop",    "00:00:00:00:00:03", "192.168.0.3"    , 0);

