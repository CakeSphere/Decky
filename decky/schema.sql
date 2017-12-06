DROP TABLE if exists sets;
DROP TABLE if exists cards;

create TABLE sets (
  id INTEGER PRIMARY KEY autoincrement,
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

create TABLE cards (
  id INTEGER PRIMARY KEY autoincrement,
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
