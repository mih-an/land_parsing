CREATE DATABASE IF NOT EXISTS ads_db;

--DROP TABLE ads_to_call;
--DROP TABLE ads_price_history;
--DROP TABLE tmp_ads;
--DROP TABLE ads;

CREATE TABLE IF NOT EXISTS ads(
	id INT AUTO_INCREMENT PRIMARY KEY,
	ads_id VARCHAR(100) NOT NULL UNIQUE,
	ads_title VARCHAR(100) NOT NULL,
	square FLOAT NOT NULL,
	price DECIMAL NOT NULL,
	vri VARCHAR(100),
	link VARCHAR(100) NOT NULL,
	kp VARCHAR(100),
	address VARCHAR(500),
	description VARCHAR(10000),
	kadastr VARCHAR(500),
	electronic_trading VARCHAR(100),
	ads_owner VARCHAR(100),
	ads_owner_id VARCHAR(100),
	first_parse_datetime DATETIME NOT NULL,
	sector_number INT NOT NULL,
	last_parse_datetime DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS tmp_ads(
	id INT AUTO_INCREMENT PRIMARY KEY,
	ads_id VARCHAR(100) NOT NULL UNIQUE,
	ads_title VARCHAR(100) NOT NULL,
	square FLOAT NOT NULL,
	price DECIMAL NOT NULL,
	vri VARCHAR(100),
	link VARCHAR(100) NOT NULL,
	kp VARCHAR(100),
	address VARCHAR(500),
	description VARCHAR(10000),
	kadastr VARCHAR(500),
	electronic_trading VARCHAR(100),
	ads_owner VARCHAR(100),
	ads_owner_id VARCHAR(100),
	first_parse_datetime DATETIME NOT NULL,
	sector_number INT NOT NULL,
	last_parse_datetime DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS ads_price_history(
	id INT AUTO_INCREMENT PRIMARY KEY,
	ads_id VARCHAR(100) NOT NULL,
	price DECIMAL NOT NULL,
	price_datetime DATETIME NOT NULL
);

ALTER TABLE ads ADD is_unpublished BIT DEFAULT(FALSE) NOT NULL;
ALTER TABLE tmp_ads ADD is_unpublished BIT DEFAULT(FALSE) NOT NULL;
ALTER TABLE ads ADD to_call_datetime DATETIME;
ALTER TABLE tmp_ads ADD to_call_datetime DATETIME;


CREATE TABLE IF NOT EXISTS ads_to_call(
	id INT AUTO_INCREMENT PRIMARY KEY,
	ads_id VARCHAR(100) NOT NULL UNIQUE,
	ads_title VARCHAR(100) NOT NULL,
	square FLOAT NOT NULL,
	price DECIMAL NOT NULL,
	vri VARCHAR(100),
	link VARCHAR(100) NOT NULL,
	kp VARCHAR(100),
	address VARCHAR(500),
	description VARCHAR(10000),
	kadastr VARCHAR(500),
	electronic_trading VARCHAR(100),
	ads_owner VARCHAR(100),
	ads_owner_id VARCHAR(100),
	first_parse_datetime DATETIME NOT NULL,
	sector_number INT NOT NULL,
	last_parse_datetime DATETIME NOT NULL,
	is_unpublished BIT DEFAULT(FALSE) NOT NULL,
	to_call_datetime DATETIME NOT NULL
);

DROP TABLE sectors_priority;

CREATE TABLE IF NOT EXISTS sectors_priority(
	id INT AUTO_INCREMENT PRIMARY KEY,
	sector_number INT NOT NULL,
	sector_order INT NOT NULL,
	UNIQUE (sector_number),
	UNIQUE (sector_order)
);

INSERT INTO sectors_priority (sector_number, sector_order)
VALUES (51, 1), (52, 2),
	(41, 3),
	(72, 4), (73, 5), (74, 6),
	(62, 7), (65, 8), (66, 9), (67, 10), (68, 11),
	(42, 12), (43, 13), (44, 14), (45, 15),
	(53, 16), (54, 17), (55, 18), (56, 19),
	(61, 20), (63, 21), (64, 22), (69, 23),
	(71, 24)
