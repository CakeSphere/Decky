drop table if exists sets;
drop table if exists cards;
drop table if exists cardstosets;
drop table if exists colors;
drop table if exists cardstocolors;

create table sets (
	id INTEGER primary key autoincrement,
	name VARCHAR(50) NOT NULL,
	code VARCHAR(4) NOT NULL,
	gathererCode VARCHAR(4),
	oldCode VARCHAR(4),
	magicCardsInfoCode VARCHAR(4),
	releaseDate DATE NOT NULL,
	border VARCHAR(50) NOT NULL,
	type VARCHAR(50) NOT NULL,
	block VARCHAR(50) NOT NULL,
	booster VARCHAR(50)
);

create table cards (
	id INTEGER primary key autoincrement,
	layout VARCHAR(50),
	name VARCHAR(50) NOT NULL,
	names VARCHAR(50),
	manaCost VARCHAR(50) NOT NULL,
	cmc INTEGER NOT NULL,
	colors VARCHAR(50),
	colorIdentity VARCHAR(50),
	type VARCHAR(50) NOT NULL,
	supertypes VARCHAR(50),
	types VARCHAR(50),
	subtypes VARCHAR(50),
	rarity VARCHAR(50) NOT NULL,
	text VARCHAR(200) NOT NULL, 
	flavor VARCHAR(200),
	artist VARCHAR(50) NOT NULL,
	number INTEGER,
	power INTEGER,
	toughness INTEGER,
	loyalty INTEGER,
	multiverseid INTEGER,
	variations VARCHAR(50),
	imageName VARCHAR(50),
	watermark VARCHAR(50),
	border VARCHAR(50),
	timeshifted VARCHAR(50),
	hand NUMBER,
	life NUMBER,
	reserved VARCHAR(50),
	releaseDate DATE,
	starter VARCHAR(50),
	mciNumber NUMBER,
	printings VARCHAR(50),
	setId INTEGER,
	setCode VARCHAR(4)
);

create table decks (
	id INTEGER primary key autoincrement,
	name VARCHAR(50) NOT NULL,
	author VARCHAR(50) NOT NULL,
	formats VARCHAR(50),
	legality VARCHAR(50),
	tags VARCHAR(50),
	commander VARCHAR(50),
	mainboard VARCHAR(50),
	sideboard VARCHAR(50),
	maybeboard VARCHAR(50),
	colors VARCHAR(50),
	description VARCHAR(500)
);