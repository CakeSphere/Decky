
DROP TABLE if exists decks;
DROP TABLE if exists decksToCards;

create TABLE decks (
  id INTEGER PRIMARY KEY autoincrement,
  author VARCHAR(50) NOT NULL,
  colors VARCHAR(50),
  commander VARCHAR(50),
  created VARCHAR(10),
  description VARCHAR(500),
  formats VARCHAR(50),
  image VARCHAR(500),
  legality VARCHAR(50),
  likes INTEGER,
  mainboard VARCHAR(50),
  maybeboard VARCHAR(50),
  name VARCHAR(50) NOT NULL,
  sideboard VARCHAR(50),
  tags VARCHAR(500),
  updated VARCHAR(10),
  makeup VARCHAR(500)
);

create TABLE decksToCards (
  id INTEGER PRIMARY KEY autoincrement,
  deckId INTEGER,
  cardId INTEGER,
  foil INTEGER,
  featured INTEGER,
  commander INTEGER,
  mainboard INTEGER,
  sideboard INTEGER,
  maybeboard INTEGER,
  acquireboard INTEGER,
  FOREIGN KEY(deckId) REFERENCES decks(id),
  FOREIGN KEY(cardId) REFERENCES cards(multiverseid)
);

INSERT INTO decks VALUES(NULL, "Blotterhead", "{w}{u}{r}", NULL, "2017-07-28", "Great card advantage with a lot of control. Chuck out what you don't need and get to what you do need quickly. Don't be afraid to counter things early, you want to lock down the board.

If you're successful in locking down the board, Fevered Visions will pretty much win it for you. Kill creatures with Lightning Axe and Fiery Temper . (9 out of the 10 most played creatures in Standard right now have a toughness of under 3, and that doesn't even include Smuggler's Copter and Fleetwheel Cruiser. See MTGGoldfish.)

Swing with Wandering Fumarole, refuel your hand with Bedlam Reveler or toss it with Nahiri's Wrath for some major damage against both creatures and planeswalkers. Collective Defiance will also do the trick.

DO NOT FORGET: You can change Wandering Fumarole's zero ability at any time. If you attack as a 4/1, and your opponent throws down a Galvanic Bombardment on the stack for three damage, you just switch it back to a 1/4.

Chandra, Torch of Defiance is best used with its ramp ability, and is practically a two drop on turn four. Drop a Chandra, Torch of Defiance AND a Fevered Visions on turn five. You'll hit your land drops with the card advantage from Cathartic Reunion and the Visions.

Here's the fun part: drop Combustible Gearhulk. You're either going to gain massive card advantage or do massive damage. If you can keep it alive (not too hard) until the next turn, drop Saheeli's Artistry to make TWO copies of Combustible Gearhulk.

Remember to choose BOTH ;-) Aren't enter the battlefield effects just the best? Since your opponent will probably choose draw, you'll have exactly what you need in-hand to finish them off.

And that's how you win.", "Standard", "417822", "Standard", 11, "main", "maybe", "Jeskai Fog", "side", "Control, Discard, Izzet", date('now'), "39, 34, 0, 29, 0");

INSERT INTO decksToCards VALUES(NULL, 1, 417815, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417815, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417815, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417815, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417819, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417819, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417819, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417819, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417826, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417826, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417823, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417823, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417823, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417823, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410046, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410046, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410046, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417822, 0, 1, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417822, 0, 1, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417822, 0, 1, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417822, 0, 1, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407692, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407692, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407692, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 410009, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407667, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407667, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407667, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407667, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414332, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414332, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414332, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414332, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414494, 1, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414494, 1, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414494, 1, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414494, 1, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414427, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414427, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414427, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414427, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407530, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407530, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407530, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 407530, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417683, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 417683, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 401897, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 401897, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414432, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414432, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414432, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, 414432, 0, 0, 0);
