CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS trusted;

DROP TABLE IF EXISTS raw.users;
CREATE TABLE raw.users(
	user_id int PRIMARY KEY,
	createdAt timestamp,
	updatedAt timestamp,
	firstName varchar(250),
	lastName varchar(250),
	address varchar(250),
	city varchar(250),
	country varchar(250),
	zipCode varchar(20),
	email  varchar(250),
	birthDate timestamp,
	gender varchar(20),
	isSmoking boolean,
	profession varchar(250),
	income float
);

DROP TABLE IF EXISTS raw.subscription;
CREATE TABLE raw.subscription(
	subscription_id SERIAL PRIMARY KEY,
	user_id int,
	createdAt timestamp,
	updatedAt timestamp,
	endDate timestamp,
	status varchar(100),
	amount float	
);
CREATE INDEX IF NOT EXISTS idx_user ON raw.subscription (user_id);

DROP TABLE IF EXISTS raw.messages;
CREATE TABLE raw.messages(
	message_id bigint PRIMARY KEY,
	createdAt timestamp,
	message varchar(1000),
	reciverId int,
	senderId int
);
CREATE INDEX IF NOT EXISTS idx_reciver ON raw.messages (reciverId);
CREATE INDEX IF NOT EXISTS idx_sender ON raw.messages (senderId);
