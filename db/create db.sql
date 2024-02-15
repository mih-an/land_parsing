CREATE DATABASE IF NOT EXISTS ads_db;

CREATE TABLE IF NOT EXISTS ads(
	id INT AUTO_INCREMENT PRIMARY KEY,
	ads_id VARCHAR(100) NOT NULL UNIQUE,
	ads_title VARCHAR(100) NOT NULL,
	square FLOAT NOT NULL,
	price INT NOT NULL,
	vri VARCHAR(100),
	link VARCHAR(100) NOT NULL,
	locality VARCHAR(100),
	kp VARCHAR(100),
	address VARCHAR(500),
	description VARCHAR(10000),
	kadastr VARCHAR(500),
	electronic_trading VARCHAR(100),
	ads_owner VARCHAR(100),
	ads_owner_id VARCHAR(100),
	ads_first_parce_datetime DATETIME NOT NULL,
	sector_number INT NOT NULL
);
