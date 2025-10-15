
-- 1) Create the user (from anywhere). You can tighten host later.
CREATE USER IF NOT EXISTS 'sports_app_user'@'%' IDENTIFIED BY '{sports_app_password}';

-- 2) Grant only what the app needs on your schema.
GRANT
  SELECT, INSERT, UPDATE, DELETE,          -- CRUD
  CREATE TEMPORARY TABLES,                 -- for temp tables
  INDEX,                                   -- create/drop indexes on existing tables (e.g., via migrations)
  EXECUTE                                  -- call stored procedures/functions if you use them
ON `sports`.* TO 'sports_app_user'@'%';



