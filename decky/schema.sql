DROP TABLE if exists sets;
DROP TABLE if exists cards;
DROP TABLE if exists users;

create TABLE users ( 
  id INTEGER PRIMARY KEY autoincrement,
  email VARCHAR(100) NOT NULL,
  username VARCHAR(32) NOT NULL,
  password VARCHAR(160) NOT NULL
);

create TABLE sets (
  id INTEGER PRIMARY KEY autoincrement,
  baseSetSize INTEGER,
  block VARCHAR(50) NOT NULL,
  boosterV3 VARCHAR(50),
  code VARCHAR(4) NOT NULL,
  codeV3 VARCHAR(4),
  isFoilOnly INTEGER,
  isOnlineOnly INTEGER,
  keyruneCode VARCHAR(4),
  mcmName VARCHAR(50),
  mcmId INTEGER,
  meta VARCHAR(200),
  mtgoCode VARCHAR(4),
  name VARCHAR(50) NOT NULL,
  parentCode VARCHAR(4),
  releaseDate VARCHAR(15),
  tcgplayerGroupId INTEGER,
  tokens VARCHAR(200),
  totalSetSize INTEGER,
  translations VARCHAR(200),
  type VARCHAR(50) NOT NULL
);

create TABLE cards (
  id INTEGER PRIMARY KEY autoincrement,
  artist VARCHAR(50) NOT NULL,
  borderColor VARCHAR(50),
  colorIdentity VARCHAR(50),
  colorIndicator VARCHAR(50),
  colors VARCHAR(50),
  convertedManaCost INTEGER NOT NULL,
  duelDeck VARCHAR(1),
  faceConvertedManaCost INTEGER,
  flavorText VARCHAR(200),
  foreignData VARCHAR(200),
  frameEffect VARCHAR(200),
  frameVersion VARCHAR(6),
  hand VARCHAR(5),
  hasFoil INTEGER,
  hasNonFoil INTEGER,
  isAlternative INTEGER,
  isOnlineOnly INTEGER,
  isOversized INTEGER,
  isReserved INTEGER,
  isStarter INTEGER,
  isTimeshifted INTEGER,
  layout VARCHAR(50),
  legalities VARCHAR(200),
  life VARCHAR(200),
  loyalty VARCHAR(200),
  manaCost VARCHAR(50) NOT NULL,
  mcmId INTEGER,
  mcmMetaId INTEGER,
  mcmName VARCHAR(50),
  mciNumber NUMBER,
  multiverseId INTEGER, 
  name VARCHAR(50) NOT NULL,
  names VARCHAR(50),
  number INTEGER,
  originalText VARCHAR(200),
  originalType VARCHAR(50),
  power INTEGER,
  prices VARCHAR(200),
  printings VARCHAR(50),
  purchaseUrls VARCHAR(200),
  rarity VARCHAR(50) NOT NULL,
  rulings VARCHAR(200),
  scryfallId VARCHAR(50),
  scryfallOracleId VARCHAR(50),
  scryfallIllustrationId VARCHAR(50),
  setCode VARCHAR(4) NOT NULL,
  side VARCHAR(10),
  subtypes VARCHAR(50),
  supertypes VARCHAR(50),
  tcgplayerProductId INTEGER,
  tcgplayerPurchaseUrl VARCHAR(50),
  text VARCHAR(200) NOT NULL,
  toughness INTEGER,
  type VARCHAR(50) NOT NULL,
  types VARCHAR(50),
  uuid VARCHAR(200),
  variations VARCHAR(50),
  watermark VARCHAR(50)
);
