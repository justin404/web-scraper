-- Create using the root account

-- 1) Create the new user
CREATE USER IF NOT EXISTS 'admin_user'@'%' IDENTIFIED BY '{admin_password}';

-- 2) Grant full privileges on all databases
GRANT ALL PRIVILEGES ON *.* TO 'admin_user'@'%' WITH GRANT OPTION;

-- Global/dynamic admin privileges commonly needed in MySQL 8.0
GRANT
  SYSTEM_USER,                    -- allow admin sessions even under max connections
  SYSTEM_VARIABLES_ADMIN,         -- SET GLOBAL, etc.
  SESSION_VARIABLES_ADMIN,        -- SET SESSION
  SUPER,                          -- deprecated,  can likely remove
  PERSIST_RO_VARIABLES_ADMIN,     -- SET PERSIST_ONLY variables
  RELOAD,                         -- FLUSH statements
  PROCESS,                        -- SHOW PROCESSLIST, KILL
  CONNECTION_ADMIN,               -- manage connections
  SHUTDOWN,                       -- stop the server
  REPLICATION SLAVE,      -- renamed in 8.1
  REPLICATION CLIENT,             -- view replication/GTID status
  BINLOG_ADMIN,                   -- manage binary logs
  BACKUP_ADMIN                    -- admin for backup-related ops
ON *.* TO 'admin_user'@'%';

-- 4) Apply changes
FLUSH PRIVILEGES;

