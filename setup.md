1) Config network

- Go to postgresql config on C:\ProgramFiles\PostgreSQL\<version>\data\postgresql.conf

- #listen_addresses = 'localhost' change to listen_addresses = '*'

- In the same folder: pg_hba.conf
- Add # IPv4 LAN connections:
host    all             all             192.168.1.0/24          scram-sha-256
where ip is host device's ipconfig ipv4 address

2) Restart postgresql
- Win+R -> services.msc -> postgresql-x64-18 - restart

3) Firewall
Press:

Windows key → type Windows Defender Firewall with Advanced Security → open it

Then:

Inbound Rules → New Rule...

Select:

Port → Next

Select:

TCP

For Specific local ports, enter: 5432 / whiev port

Allow the connection

