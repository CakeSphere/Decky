drop table if exists sets;
drop table if exists cards;
drop table if exists decks;

create table sets (
	id INTEGER primary key autoincrement,
	block VARCHAR(50) NOT NULL,
	booster VARCHAR(50),
	border VARCHAR(50) NOT NULL,
	code VARCHAR(4) NOT NULL,
	gathererCode VARCHAR(4),
	magicCardsInfoCode VARCHAR(4),
	name VARCHAR(50) NOT NULL,
	oldCode VARCHAR(4),
	releaseDate DATE NOT NULL,
	type VARCHAR(50) NOT NULL
);

create table cards (
	id INTEGER primary key autoincrement,
	artist VARCHAR(50) NOT NULL,
	border VARCHAR(50),
	cmc INTEGER NOT NULL,
	colorIdentity VARCHAR(50),
	colors VARCHAR(50),
	flavor VARCHAR(200),
	hand NUMBER,
	imageName VARCHAR(50),
	layout VARCHAR(50),
	life NUMBER,
	loyalty INTEGER,
	manaCost VARCHAR(50) NOT NULL,
	mciNumber NUMBER,
	multiverseid INTEGER,
	name VARCHAR(50) NOT NULL,
	names VARCHAR(50),
	number INTEGER,
	power INTEGER,
	printings VARCHAR(50),
	rarity VARCHAR(50) NOT NULL,
	releaseDate DATE,
	reserved VARCHAR(50),
	setCode VARCHAR(4),
	setId INTEGER,
	starter VARCHAR(50),
	subtypes VARCHAR(50),
	supertypes VARCHAR(50),
	text VARCHAR(200) NOT NULL, 
	timeshifted VARCHAR(50),
	toughness INTEGER,
	type VARCHAR(50) NOT NULL,
	types VARCHAR(50),
	watermark VARCHAR(50),
	variations VARCHAR(50)
);

create table decks (
	id INTEGER primary key autoincrement,
	author VARCHAR(50) NOT NULL,
	colors VARCHAR(50),
	commander VARCHAR(50),
	description VARCHAR(500),
	formats VARCHAR(50),
	image VARCHAR(500),
	legality VARCHAR(50),
	likes INTEGER,
	mainboard VARCHAR(50),
	maybeboard VARCHAR(50),
	name VARCHAR(50) NOT NULL,
	sideboard VARCHAR(50),
	tags VARCHAR(500)
);