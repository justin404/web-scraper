/**

	What will we need to store?
    
		stat_site
			id
			name
            url
		
        team_stat_site_map
			id
            stat_site_id
            team_id
            url
		
        player_stat_site_map
			id
            stat_site_id
            player_id
        
    
        Team
			id
			name
            abbreviation
            sport
            league
            level
            city
            state            
            
        Player
			id
            team_id
            first_name
            last_name
            suffix
            position
            height
            weight
            birth_date
            experience
		
        injury
        
        team_game_log
			id
            team_id
            opponent_team_id
            season
            game_number
            game_date
            start_time (et)
            points  (tm)
            opponent_points (opp)
            wins
            losses
            attendance
            length_of_game
            loss_streak
            win_streak
            
            
        player_game_log
			id
            team_id
            opponent_team_id
            player_id
            <stats>
			
        
        Game statistics (flat, per sport)
			basketball (wnba, nba)
				-- standard
                gs games_started
                mp minutes_played
                fg field_goals
                fga field_goal_attempts
                fg% field_goal_percentage
                3p 3point_field_goals
                3pa 3point_field_goal_attempts
                3p% 3point_field_goal_percentage
                ft free_throws
                fta free_throw_attempts
                ft% free_throw_percentage
                orb offensive_rebounds
                drb defensive_rebounds
                trb total_rebounds
                ast assists
                stl steals
                blk blocks
                tov turnovers
                pf personal_fouls
                pts points
                gmsc game_score
                +/- plus_minus
                
                -- advanced
                gcar career_game_number
                gtm season_game_number
                gs games_started
                mp minutes_played
                ts% true_shooting_percentage
                efg% effective_field_goal_percentage
                orb% offensive_rebound_percentage
                drb% defensive_rebound_percentage
                trb% total_rebound_percentage
                ast% assist_percentage
                stl% steal_percentage
                blk% block_percentage
                tov% turnover_percentage
                usg% usage_percentage
                ortg offensive_rating
                drtg defensive_rating
                gmsc game_score
                bpm box_plus_minus
                
            hockey
            mlb
            football	
            
            


*/


CREATE SCHEMA IF NOT EXISTS sports;


-- Drop tables if they exist
DROP TABLE IF EXISTS sports.basketball_player_game_log;
DROP TABLE IF EXISTS sports.team_game_log;
DROP TABLE IF EXISTS sports.player_stat_site_map;
DROP TABLE IF EXISTS sports.team_stat_site_map;
DROP TABLE IF EXISTS sports.player;
DROP TABLE IF EXISTS sports.team;
DROP TABLE IF EXISTS sports.stat_site;

-- Create stat_site table
CREATE TABLE sports.stat_site (
    stat_site_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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
);

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
);

-- Create team_stat_site_map table
CREATE TABLE sports.team_stat_site_map (
    team_stat_site_map_id INT AUTO_INCREMENT PRIMARY KEY,
    stat_site_id INT,
    team_id INT,
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create player_stat_site_map table
CREATE TABLE sports.player_stat_site_map (
    player_stat_site_map_id INT AUTO_INCREMENT PRIMARY KEY,
    stat_site_id INT,
    player_id INT,
    url TEXT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create team_game_log table
CREATE TABLE sports.team_game_log (
    team_game_log_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    opponent_team_id INT,
    season VARCHAR(10),
    game_number INT,
    game_datetime DATETIME,    
    points INT,
    opponent_points INT,
    wins INT,
    losses INT,
    attendance INT,
    length_of_game TIME,
    loss_streak INT,
    win_streak INT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create basketball_player_game_log table
CREATE TABLE sports.basketball_player_game_log (
    basketball_player_game_log_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    team_id INT,
    games_started INT,
    minutes_played DECIMAL(5,2),
    field_goals INT,
    field_goal_attempts INT,
    field_goal_percentage DECIMAL(5,2),
    `3point_field_goals` INT,
    `3point_field_goal_attempts` INT,
    `3point_field_goal_percentage` DECIMAL(5,2),
    free_throws INT,
    free_throw_attempts INT,
    free_throw_percentage DECIMAL(5,2),
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    blocks INT,
    turnovers INT,
    personal_fouls INT,
    points INT,
    game_score DECIMAL(5,2),
    plus_minus INT,
    active_flag CHAR(1) NOT NULL DEFAULT 'Y',
    create_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);



