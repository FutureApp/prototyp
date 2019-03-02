CREATE USER 'hive'@'%'IDENTIFIED by 'password';
GRANT all on *.* to 'hive'@localhost IDENTIFIED by'password';
flush privileges;