
# sudo apt install postgresql postgresql-contrib
# vachagan@OMEN:~$ sudo -i -u postgres
# postgres@OMEN:~$ psql
# psql (12.6 (Ubuntu 12.6-0ubuntu0.20.04.1))
# Type "help" for help.
#
# postgres=# \q
# postgres@OMEN:~$ exit
# logout
# vachagan@OMEN:~$ sudo -u postgres psql
# psql (12.6 (Ubuntu 12.6-0ubuntu0.20.04.1))
# Type "help" for help.
#
# postgres=# createuser --interactive
# postgres-# sudo -u postgres createuser --interactive
# postgres-# \q
# vachagan@OMEN:~$ sudo -u postgres createuser --interactive
# Enter name of role to add: vachagan
# Shall the new role be a superuser? (y/n) y
# vachagan@OMEN:~$ sudo su - postgres
# postgres@OMEN:~$ psql
# psql (12.6 (Ubuntu 12.6-0ubuntu0.20.04.1))
# Type "help" for help.
#
# postgres=# CREATE DATABASE checkers;

# postgres=# CREATE USER vachagan WITH PASSWORD '542652';
# postgres=# CREATE USER checkers WITH PASSWORD '542652';
# CREATE ROLE
# postgres=# GRANT ALL PRIVILEGES ON DATABASE checkers TO checkers;
# GRANT
# postgres=# \q
# postgres@OMEN:~$ exit
# logout
