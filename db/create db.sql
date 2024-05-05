CREATE DATABASE IF NOT EXISTS ads_db;

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
	is_unpublished BIT DEFAULT(FALSE) NOT NULL
);

