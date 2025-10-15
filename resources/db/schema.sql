-- Create stat_site table
CREATE TABLE sports.stat_site (
    stat_site_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) Engine = InnoDB
  DATA DIRECTORY = '/tablespaces/sports'
;


-- Create team table
CREATE TABLE sports.team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    abbreviation VARCHAR(10),
    sport_type VARCHAR(50),
    league VARCHAR(100),
    level VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) Engine = InnoDB
  DATA DIRECTORY = '/tablespaces/sports'
;

-- Create player table
CREATE TABLE sports.player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    name VARCHAR(200),
    position VARCHAR(10),
    height VARCHAR(10),
    weight INT,
    birth_date DATE,
    experience INT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) Engine = InnoDB
  DATA DIRECTORY = '/tablespaces/sports'
;



-- Create team_stat_site_map table
CREATE TABLE sports.team_stat_site_map (
    team_stat_site_map_id INT AUTO_INCREMENT PRIMARY KEY,
    stat_site_id INT,
    team_id INT,
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) Engine = InnoDB
  DATA DIRECTORY = '/tablespaces/sports'
;

-- Create player_stat_site_map table
CREATE TABLE sports.player_stat_site_map (
    player_stat_site_map_id INT AUTO_INCREMENT PRIMARY KEY,
    stat_site_id INT,
    player_id INT,
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) Engine = InnoDB
  DATA DIRECTORY = '/tablespaces/sports'
;