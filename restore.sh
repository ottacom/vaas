rm ./tinydb/vaas.json
rm /var/cache/bind/*
cp /etc/bind/db.80.168.192 /var/cache/bind/
cp /etc/bind/db.dpl-dmi.dk /var/cache/bind/
service bind9 restart
