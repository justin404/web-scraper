/*
 NFL Team Schema


    Metrics are broken up as follows:

        Passing
            C/ATT       Completions/Attempts
            YDS         Completed Yards
            AVG         Average yards per completion
            TD          Passing touchdowns
            INT         Interceptions
            SACKS       Sacks  completed-attempts
            QBR         QB Rating (contribution to the game)
            RTG         Passer Rating

        Rushing
            CAR         Carries
            YDS         Yards rushed
            AVG         Average yards per rush
            TD          Rushing touchdown
            LONG        Longest rush

        Receiving
            REC         Receptions
            YDS         Total received yards
            AVG         Average yards per reception
            TD          Reception touchdown
            LONG        Longest reception
            TGTS        Total times targeted

        Fumbles
            FUM         Total times fumbled
            LOST        Number of fumbles that were lost (opposing team recovered)
            REC         Fumble recovered - defensive or special teams player picking up a fumbled ball

        Defense
          TACKLES
            TOT         Total tackles (solo + assisted)
            SOLO        Solo tackles (unassisted)
            SACKS       Defensive player tackles the opposing QB
            TFL         Tackle for loss - defensive player tackles an offensive player for a loss of yardage from LOS
          MISC
            PD          Passes defensed - when a defender gets contact with the ball to cause an incomplete pass
            QB HITS
            TD          Defensive touchdown

        Interceptions
            INT         Passes intercepted
            YDS         Intercepted returned yards
            TD          Interceptions returned for touchdown

        Kick Returns
            NO          Number of kick returns
            YDS         Total yards returned
            AVG         Average kickoff yards per return
            LONG        Longest return
            TD          Kick returned for touchdown

        Punt Returns
            NO          Number of punt returns
            YDS         Total yards returned
            AVG         Average punted yards per return
            LONG        Longest return
            TD          Punt returned for touchdown

        Kicking
            FG          Field Goals made/attempted
            PCT         Percentage made
            LONG        Longest kick
            XP          Extra points made/attempted
            PTS         Total kicking points

        Punting
            NO          Number of punts
            YDS         Total punted yards
            AVG         Average yards per punt
            TB          Touchback
            IN 20       Punts inside the 20 yard line
            LONG        Longest punt

 */

DROP TABLE IF EXISTS sports.football_passing;
DROP TABLE IF EXISTS sports.football_rushing;
DROP TABLE IF EXISTS sports.football_receiving;
DROP TABLE IF EXISTS sports.football_fumbles;
DROP TABLE IF EXISTS sports.football_defense;
DROP TABLE IF EXISTS sports.football_interceptions;
DROP TABLE IF EXISTS sports.football_kick_returns;
DROP TABLE IF EXISTS sports.football_punt_returns;
DROP TABLE IF EXISTS sports.football_kicking;
DROP TABLE IF EXISTS sports.football_punting;


CREATE TABLE sports.football_passing
(
    football_passing_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    completions         INT,
    attempts            INT,
    yards               INT,
    avg                 DECIMAL(5, 2),
    touchdowns          INT,
    interceptions       INT, -- thrown
    sacks               INT, -- times sacked
    qbr                 DECIMAL(5, 2),
    rtg                 DECIMAL(5, 2)
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- RUSHING
CREATE TABLE sports.football_rushing
(
    football_rushing_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    carries             INT,
    yards               INT,
    avg                 DECIMAL(5, 2),
    touchdowns          INT,
    long_gain           INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- RECEIVING
CREATE TABLE sports.football_receiving
(
    football_receiving_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    receptions            INT,
    yards                 INT,
    avg                   DECIMAL(5, 2),
    touchdowns            INT,
    long_gain             INT,
    targets               INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- FUMBLES
CREATE TABLE sports.football_fumbles
(
    football_fumbles_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    fumbles             INT,
    lost                INT,
    recovered           INT -- fumbles recovered
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- DEFENSE
CREATE TABLE sports.football_defense
(
    football_defense_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    total_tackles       INT,
    solo_tackles        INT,
    sacks               INT,
    tackles_for_loss    INT,
    passes_defensed     INT,
    qb_hits             INT,
    touchdowns          INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- INTERCEPTIONS (defense returns)
CREATE TABLE sports.football_interceptions
(
    football_interceptions_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id                   INT,
    player_id                 INT,
    interceptions             INT,
    return_yards              INT,
    touchdowns                INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- KICK RETURNS
CREATE TABLE sports.football_kick_returns
(
    football_kick_returns_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id                  INT,
    player_id                INT,
    returns                  INT,
    yards                    INT,
    avg                      DECIMAL(5, 2),
    long_gain                INT,
    touchdowns               INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- PUNT RETURNS
CREATE TABLE sports.football_punt_returns
(
    football_punt_returns_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id                  INT,
    player_id                INT,
    returns                  INT,
    yards                    INT,
    avg                      DECIMAL(5, 2),
    long_gain                INT,
    touchdowns               INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- KICKING
CREATE TABLE sports.football_kicking
(
    football_kicking_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    fg_made             INT,
    fg_attempted        INT,
    pct                 DECIMAL(5, 2), -- field-goal percentage
    long_gain           INT,           -- longest made FG
    xp_made             INT,
    xp_attempted        INT,
    points              INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';

-- PUNTING
CREATE TABLE sports.football_punting
(
    football_punting_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id             INT,
    player_id           INT,
    punts               INT,
    yards               INT,
    avg                 DECIMAL(5, 2),
    touchbacks          INT,
    inside_20           INT,
    long_gain           INT
) ENGINE=InnoDB DATA DIRECTORY = '/tablespaces/sports';