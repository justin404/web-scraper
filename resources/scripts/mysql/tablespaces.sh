# execute this against the host after initial creation
# This assumes that we're using a /tablespaces volume
docker exec -it mysql-container bash -lc 'mkdir -p /tablespaces && chown -R mysql:mysql /tablespaces && chmod 770 /tablespaces'

# For every schema created, the directory for its tablespaces will need to be explicitly created

docker exec -it mysql-container bash -ls 'mkdir -p /tablespace/sports && chown -R mysql:mysql /tablespaces/sports && chmod 770 /tablespaces/sports'

# Can then create tablespaces like `CREATE TABLESPACE ts_table ADD DATAFILE '/var/lib/mysql/ts/ts_table.ibd' ENGINE=InnoDB;`
# Since we have innodb_file_per_table turned on by default, we can also just use the DATA DIRECTORY directive:
#   CREATE TABLE sports.test (
#     id int
#   ) ENGINE = InnoDB
#     DATA DIRECTORY = '/tablespaces/sports'
#
#



# Troubleshooting -

docker exec -it mysql-container bash -lc '
  set -e
  mkdir -p /tablespaces/sports
  # ensure no stale file
  rm -f /tablespaces/sports/ts_sports.ibd
  # mysql user in the official image owns the dir
  chown -R mysql:mysql /tablespaces
  chmod 770 /tablespaces /tablespaces/sports
  ls -ld /tablespaces /tablespaces/sports || true
'