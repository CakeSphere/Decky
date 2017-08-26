drop table if exists sets;
drop table if exists cards;
drop table if exists decks;
drop table if exists decksToCards;

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

create table decksToCards (
  id INTEGER primary key autoincrement,
  deckId INTEGER,
  cardId INTEGER,
  FOREIGN KEY(deckId) REFERENCES decks(id),
  FOREIGN KEY(cardId) REFERENCES cards(id)
);

insert into decks values(null, "Blotterhead", "{w}{u}{r}", null, "
        Great card advantage with a lot of control. Chuck out what you don’t need and get to what you do need quickly. Don’t be afraid to counter things early, you want to lock down the board.
      
        If you’re successful in locking down the board, Fevered Visions will pretty much win it for you. Kill creatures with Lightning Axe and Fiery Temper. (9 out of the 10 most played creatures in Standard right now have a toughness of under 3, and that doesn’t even include Smuggler’s Copter and Fleetwheel Cruiser. See MTGGoldfish.)
      
        Swing with Wandering Fumarole, refuel your hand with Bedlam Reveler or toss it with Nahiri’s Wrath for some major damage against both creatures and planeswalkers. Collective Defiance will also do the trick.
      
        DO NOT FORGET: You can change Wandering Fumarole's zero ability at any time. If you attack as a 4/1, and your opponent throws down a Galvanic Bombardment on the stack for three damage, you just switch it back to a 1/4.
      
        Chandra, Torch of Defiance is best used with its ramp ability, and is practically a two drop on turn four. Drop a Chandra, Torch of Defiance AND a Fevered Visions on turn five. You'll hit your land drops with the card advantage from Cathartic Reunion and the Visions.
      
        Here's the fun part: drop Combustible Gearhulk. You're either going to gain massive card advantage or do massive damage. If you can keep it alive (not too hard) until the next turn, drop Saheeli's Artistry to make TWO copies of Combustible Gearhulk.
      
        Remember to choose BOTH ;-) Aren't enter the battlefield effects just the best? Since your opponent will probably choose draw, you'll have exactly what you need in-hand to finish them off.
      
        And that's how you win.
      ", "Standard", "414494", "Standard", 11, "main", "maybe", "Jeskai Fog", "side", "Control, Discard, Izzet");
insert into decksToCards values(null, 1, 3357);


-- SELECT * FROM decksToCards INNER JOIN cards ON cardId=cards.id WHERE deckId=1;
