
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
  cardId VARCHAR(100),
  foil INTEGER,
  featured INTEGER,
  commander INTEGER,
  sideboard INTEGER,
  maybeboard INTEGER,
  acquireboard INTEGER,
  mainboard INTEGER,
  FOREIGN KEY(deckId) REFERENCES decks(id),
  FOREIGN KEY(cardId) REFERENCES cards(multiverseid)
);

INSERT INTO decks VALUES(NULL, " Happymaster19 ", "{w}{u}{r}", NULL, "2017-07-28", "

Hello, everybody. Welcome to my primer for Modern U/W Spirits. Tribes are built around a core of creatures that have effects that support their shared creature type. We’ll discuss how Spirits went from a back-burner creature type to a supported tribe with identity. We’ll discuss the various builds of Spirits, how the strengths and weaknesses of this build compare to other builds as well as the meta itself.

CREATURES

Tribes consist of a core that gives the tribe an identity, the thing they do. Spirits specialize in disruption, especially proactive disruption. Most will sit on the battlefield and serve as potential disruption while they beat in and even blanket protection at times. Our sacrifice spirits like Selfless Spirit , Remorseful Cleric , and Mausoleum Wanderer get in damage and are constantly at the ready to throw a wrench in a variety of plans. Drogskol Captain gives us passive proactive disruption or protection. And some can come in reactively to surprise the opponent such as Rattlechains and Spell Queller .

    Mausoleum Wanderer has to be one of the more versatile one drops in competitive tribal decks (if Zombies were more competitive, Cryptbreaker would easily be in contention). It’s a lowly 1/1 but it has natural evasion, a hallmark of the tribe. It has great early game value by forcing your opponent off curve for their spells. It has decent late game value as lords accrue and those Force Spike s turn into Spell Pierce s that beat in harder. Not the best topdeck if you’re recovering from a sweeper but how much can you ask of a one drop really? As opposed to being an all in beater like Champion of the Parish or an all in synergy piece like Heritage Druid , Mausoleum Wanderer brings versatility. Combatting spells through its tribal identity, and beating over aggro decks while adding a little gravy when you order mashed potatoes. If it’s only bad after recovering from an empty board, I can’t ask much more. It’s part of the deck because it’s strictly the best one drop Spirit. It’s a part of the core because it brings that rounded package of a cost effective beater in the air, a constant threat to our opponent’s curve, a perfect one mana slice of the tribe’s identity.

    Rattlechains gets its numbers tweaked in builds that sport Aether Vial or Collected Company . While this build has the Vial, I include Rattlechains as a core playset because 1) Redundancy of instant speed play, 2) The format is overrun with creatures and the best way to deal with creatures is removal. Rattlechains answers those answers. Not only does it act as an instant speed counter to that removal but enables many of our other Spirits to do the same in their own way. Vial is also a once per turn card without access to Merrow Reejery shenanigans. Rattlechains ’s only bottleneck is mana. We can dump a bunch of ghosts on our opponent’s end step and go to our turn for the swing. Rattlechains reshapes how all of our creatures function. Whether it’s simply getting to cast it on that end step for pseudo-haste or for instant speed hexproof counters, upkeep gotchas, etc. Sometimes you have to stay focused so as to not forget which spirits have intrinsic flash. Just keep the lines in mind and you will be rewarded. This card is a part of the tribes core for its ability to reshape how many of the tribe mates function and stun opponents as well as the gravy instant speed protection.

    Selfless Spirit isn’t a full playset inclusion in most builds but makes it as a solid 3x in the majority of builds and sees solid play beyond the tribe. The Spirit doesn’t need much explaining. A tribe’s biggest weakness is most often sweepers and removal. Selfless Spirit is at its best when it’s eating sweepers but can also give opponents headaches in combat and when handling removal spells. Great way to backup a Drogskol Captain from those wraths. While probably not the most sound of logic, if a creature is solid enough to see play in decks outside the tribe, it can only be better in the tribe. Other decks are jamming 2/1 flying Ajani’s Interventions while we get those same Interventions as potentially 4/3 Hexproof flash beaters? Same goes for other cards that see play outside the tribe. We just take good cards that happen to be Spirits and then support them for being Spirits. My Selfless Spirit is better than yours! The Spirit is a part of the core because it is many creature decks’ answer to sweepers and as a tribe we fall into that category. As Selfless Spirit ’s tribe, we make it better than most other decks running it. Same bird, bigger stone.

    Spell Queller encapsulates the disruptive identity of the tribe. Instant speed flying beater that feasts on the efficiency of the format taking most spells prisoner. Good enough to see play in decks that support its colors, Spirits grant the Queller their protective boons, making Queller more durable in those grindy matchups. The choice of wording to have ‘exile’ over ‘counter’ means Queller can get those pesky Abrupt Decay s, Supreme Verdict s, and Cavern of Souls casts. Given the efficiency of the format, the Queller has live targets (good or not) in most matchups. This reliabile disruption in tribe brings Queller firmly into the core.

    Drogskol Captain finishes up the core of the deck with the tribal trademark anthem effect and a complimentary static ability that turns our ghosts into nightmares. They saying with Drog daddy is ‘Sweeper or bust’ and it’s so true. Thank God Spirits are a tribe of protection because Drog daddy is a removal magnet. What makes Droggy a part of the core while Supreme Phantom is relegated to the title of ‘support piece’ is that hexproof. The deck was perfectly playable when it was just Droggy and Phantasmal Image . But if Supreme Phantom and Droggy had their releases switched, I doubt that would have been the case. Phantom is great for anthem redundancy but it’s the boon of hexproof that really establishes Drogskol Captain as the anthem of choice in our core.

While I would make strong arguments for Spirit decks to include the creatures you’ll see below, I would almost require the above just to make a playable deck. They are the most well-rounded and support our identity the best. The rest are utility spirits or redundant effects.

    Spectral Sailor is a simple body but with a mana cost of one and flash, the opportunity cost to play it is extraordinarily low. It’s not flashy but it’s a bit of fairly reliable damage and an additional draw per turn in the late game which is very valuable to an aggro deck.

    Supreme Phantom is a new member to the core of Spirits. I leave him out of the core because the deck was still functional before Phantom. That does not at all diminish the boon of redundant anthems. The text is simple so I won’t complicate it. Supreme Phantom ’s presence is what gives Phantasmal Image admission. Image can copy just about whatever it wants but lords are best and a higher density of lords makes Image much better.

    Remorseful Cleric has enough play against the current meta that we’ll mainboard one. Lots of decks rely on their graveyard and more still use them to some degree. Why not jam a singleton and get some surprise wins? I have gotten very excited by how many great sideboard creatures happen to be spirits. This guys is good enough to get the main/side split.

    Phantasmal Image has borderlined on being considered a core member. Regardless it has found a home in Humans and Spirits. While our lords are obviously ideal targets, we are fine with taking extra disruption where we need to. I wouldn’t call it core because it needs a core to support. It has the tiny downside of not getting flash from Rattlechains . That’s not going to come up a ton and Aether Vial can alleviate that anyway. Image is inherently a card with variance attached. If we have nothing on board, it’s absolutely terrible. Other than that, it can be anything from a backup Selfless Spirit to a lord to a Spell Queller (off Aether Vial ). Some lists will go heavy with three. I prefer a pair to keep from getting into that situation against grindy decks or post sweeper. At least too often.

    Empyrean Eagle is a redundant anthem for all our Spirits as the tribe wholly, yet incidentally has flying. The Eagle itself seems almost incidentally to be a spirit. And that’s all it is. A redundant flying anthem. But with its inclusion, we have enough natural anthems that this frees up Phantasmal Image to either copy backup utility spirits or press the aggro by cloning anthems. In other words, Empyrean Eagle takes the pressure off of Image to serve as the lord it so commonly does. On the flip side we have an insane amount of lords at our disposal. And anthems on flyers are big trouble.

SPELLS

    Path to Exile is an easy include for any white deck. Keep those laser beams handy in case the battlefield gets hairy.

    Aether Vial fianlly comes to the build. After much deliberation. While the Snapcaster Mage Spell package was handy for dealing with top end threats and longer games, the format has blazed past that so we press into new territory. Vial will open up our mana for Rattlechains plays and also take the burden off of Rattlechains both in effect and from our hand. Also gives us the edge Vial normally gives against counters, Chalice of the Void , etc. Vial just allows us to unload faster against the increasing speed of the format.

That’s the main deck. We want to trip up our opponent while we stack anthems and beat over the ground.

Forming a Foundation So where did we get this core? Spirits have always been around for as long as Magic but never really got any focus until Kamigawa. While there was a lot of interplay in those Spirits, they still didn’t have a real focus. Ghost-Lit Redeemer , Oyobi, Who Split the Heavens , Forked-Branch Garami . Soulshift was powerful but generally came at high cost. No lord. No real efficient Spirit payoffs. No focus. After returning to obscurity, Spirit were given some spotlight with a trip to Innistrad. Spirits found their first true lord in Drogskol Captain all but solidifying blue and white as a part of the tribes banner and hexproof giving the tribe a seed to bloom an identity from. Unfortunately the rest of the tribe in block was rather lackluster and Drogskol Captain simply wasn’t going to hoist them into Modern on his lonesome. Geist of Saint Traft is certainly a solid Spirit but not really the type of card that rounds out a tribe. The tribe needed to develop more. It wasn’t until we returned to Innistrad that Spirits got its support. Shadows over Innistrad began as a trickle with Rattlechains really being the only solid Spirit to support a tribal strategy. However, Eldritch Moon changed everything. Mausoleum Wanderer , Selfless Spirit , Spell Queller , Nebelgast Herald . Spell disruption, wrath protection, a counter that exiles, board control. With a blue-white base formed, the tribe found its identity. Disrupt the opponent, secure your board, beat over the top. By this point, Eldritch Moon had fleshed out 85% of the deck you see listed. That last chunk came when Spirits got a surprise lord along with a Tormod's Crypt on wings in Core 2019 with Supreme Phantom and Remorseful Cleric . This gave the tribe much needed teeth and a tribal tool for graveyard strategies.

Common Builds

    W/U/G (Bant): Since Core 2019, Spirits have become a formidable fighter in the format. Most commonly built in W/U/G Collected Company shells, this build is likely the most aggressive, able to defend itself with Mausoleum Wanderer and Spell Queller until it gets to Collected Company , which it ramps into with the help of Noble Hierarch . That exalted trigger on those Nobles also has subtle but sweet synergy with Mausoleum Wanderer . This build puts the priority on aggression with the secondary ability to defend itself more than disrupt the opponent. Punishing against metas with few creatures. That variance found in CoCo just makes the ability to disrupt less reliable. You could hit the jackpot and get double lord or Queller to hit something juicy on the stack. Or you could hit a Noble and a nothing. Maybe you’re CoCoing for that Queller you need and you flip two lords but the spell resolves, killing you. I feel CoCo builds water down the identity for a tribe that can CoCo into anthems on wings, even so far as to main deck a third Phantasmal Image much of the time. It might be the more popular build but that style doesn’t appeal to me as much.

    W/U Vial: The next most popular is some tweak on what you see before you. Vial is a bit of a cop out card for low curve creature decks from various tribes to Death and Taxes decks. Many decks can use it to load creatures on the battlefield and most can abuse its ability to activate at instant speed. While Spirits can’t abuse it with effects like Merrow Reejery, we definitely get an advantage in our mana. With disruptive abilities that can activate immediately, this can lead to blow out plays and furthers the mantra given by the Spirit’s tribal identity. Vial can allow us to unload our hand without being forced to commit to the board the way Collected Company does. We can stay aggressive against aggro decks while being more methodical against midrange and control. This retains the identity of the tribe while allowing it to get mean when it wants.

    W/U/B (Epser): A few trace builds will opt to go W/U/B for Lingering Souls as the tokens are great with lords and the spell synergizes with Mausoleum Wanderer to great effect. I lean away from this build as it puts focus on a sorcery. While it’s a strong interaction with those power boosts, it again waters the disruptive identity for an aggro deck that can disrupt.

    Magic Aids and the 5c Spirits deck: I know Magic Aids posted a 5-color Spirits deck and while I was particularly impressed with Eidolon of Great Revels, Bloodghast , and Strangleroot Geist struck me as cute beaters. They work well with the anthems but they don’t add anything to the disruptive nature of the tribe. If even one more solid red Spirit shows up, I could see Jeskai supplant its Azorious contemporary. As for the 5c deck, I think it too goes aggressive with resilient but non-evasive beaters. They are helped by being Spirits. They do little for our other Spirits.

I find that most of these builds try to hard to be aggressive when there are plenty of decks that can outmatch Spirits for power. Spirits have natural evasion which means they don’t rely on high power to break through ground situations. I feel too many builds try to take advantage of the air and focus less on what the tribe really does. Sure they fly. But faeries do too. Faeries disrupt. But they don’t really rely on anthems. Thanks to heavier beaters like Vendilion Clique and Mistbind Clique as well as the one card swarm, Bitterblossom , faeries don’t need to build as much of a board presence supported by anthems. In that regard, I feel faeries don’t really operate like a tribe, or even a tribal control deck. Faeries simply feels like classic control. Pick off what’s important and beat in quickly with a heavy beater once you obtain control. Spirits are small scale. Your Selfless Spirit simply doesn’t match Mistbind Clique for power. Faeries have more hard stopping power. Spirits must be crafty and meticulous. Relying on a lone Drogskol Captain to close the game isn’t nearly as viable as that lone Mistbind Clique . This means the deck must play together as a tribe. If you want anthems.dec play Merfolk. If you want disruption.dec (in tribe) play Faeries. If you want a tribe of disruptive creatures that work together, play Spirits. Use their identity to defend the establishment of a cooperative board. Spirits are pack disruptors. Spirits can hold back and try to play weak control. They can go all in and play weak aggro. Or they can work together and play the best balance of aggro and tempo in the format with an exciting tribal motif.

Sideboarding

The format is a hot mess. There have been top contenders that move in and out of that spot. It we haven’t had a dominant deck since Death’s Shadow had Gitaxian Probe banned. Since then we’ve had classics like U/W control, Affinity, Storm, Tron, and new blood like Hollow One, Humans, Arclight Phoenix, G/B control, and the resurgence of sleeping monsters Grishaolbrand and Dredge. It’s hard to have enough in a 15 card sideboard to deal with everything going on in the format these days. But before getting into the topic of the sideboard, it’s important to remember that sideboards are to give your deck flexibility in dealing with your local meta. I try to keep my posted list as generic as possible to cover as much space as I can. Your meta may dictate you in a different direction. That said, let’s begin.

    Blessed Alliance gives us that extra bit of removal against a go tall deck that leans on few creatures. Aim for Titanshift, Tron, Death’s Shadow, Bogles in particular but can also be more removal in creature matchups of all sorts. The other modes are seldom used but the lifegaun can be handy to have in Burn and aggro matchups.

    Kataki, War's Wage is a deliciously on tribe artifact punisher. Most artifact decks want to keep their artifacts around. This slows them down drastically if they choose to pay and obliterates their board if they don’t. They get to choose for each but the price can not be ignored.

    Nebelgast Herald keeps opposing creature decks slowed down and keeps our damage rate above theirs. Gives us more play to our Vial as well.

    Negate is classic spell tech for blue decks. Solid against Tron, combo, and control decks. Simple text, elegant effect.

    Nikko-Onna is our anti-enchantment Spirit tech. Gets rid of pesky Detention Sphere s, Ghostly Prison s, Courser of Kruphix , etc. also had the nifty ability to bounce to our hand when we play Spirits for more enchantment removal and potentially other Spirit shenanigans.

    Remorseful Cleric is a delightfully on tribe graveyard hate creature. Many decks use their graveyard to some degree. For those that focus more heavily on it as a resource, Remorseful Cleric beats in the air and strips them bare.

    Serra the Benevolent is our counter control piece. Her -3 and -6 are backbreaking effects to have on a stick in those matchups. She may have to drop to 1 to get that first Serra Angel (which normally costs five mana anyway so good deal there) but any planeswalker that can gain more than one loyalty counter per turn will have a lot more flexibility in its options including its ultimate. She is a Glorious Anthem for all our ghosties giving us the ability to close games very quickly. Her emblem is derived from a card that is a classic combo with hexproof creatures: Worship . Very easy to achieve and very potent against a fair chunk of the meta. Spirits are the perfect tribe to bring the +2 and -6 together. Tons of natural flyers to match the conditions anthem and tons of protective creatures to solidify the Worship lock. The combined versatility of big body production, a relevant anthem, and a powerful late game lock make Serra a potent threat against decks that want to durdle.

    Settle the Wreckage is the one-sided sweeper of the format. We could try to be cute with Supreme Verdict backed up by Selfless Spirit but I don’t like relying on that synergy from my sideboard. Settle is good clean fun.

    Stony Silence gives us additional artifact tech. The decks that Kataki is good in are the ones where the opponent wants to keep their artifacts around. Affinity, Lantern, etc. Stony is solid against most of that but also halts decks that like to chain artifacts or abuse them for one big turn like KCI or Thopter Sword.

", "Modern", "9b76bcd4-580a-4435-afe9-290940b1837f", "Modern", 11, "main", "maybe", "Spirited Away: A Paranormal Primer [U/W Spirits]", "side", "Competitive, Primer, Spirits, Tempo, Tribal, WU (Azorius)", date('now'), "43, 57, 0, 0, 0");

INSERT INTO decksToCards VALUES(NULL, 1, "bea9f6e9-69ae-4c49-9682-ad09e787c01e", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "bea9f6e9-69ae-4c49-9682-ad09e787c01e", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a3aab13c-9d9d-4507-ae5d-da979990ae1b", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "4ca2078c-61c6-4862-a720-2d92435d1140", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "4ca2078c-61c6-4862-a720-2d92435d1140", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "4ca2078c-61c6-4862-a720-2d92435d1140", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "4ca2078c-61c6-4862-a720-2d92435d1140", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "893eb7e4-5d8d-477b-aaa7-fb85ef2a54fc", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ee834e27-595d-4d12-8e69-e94e84ef337a", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ee834e27-595d-4d12-8e69-e94e84ef337a", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ee834e27-595d-4d12-8e69-e94e84ef337a", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "3eef85b2-3e5f-45e1-b669-ad152e55fa6d", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "3eef85b2-3e5f-45e1-b669-ad152e55fa6d", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "105b2118-b22c-4ef5-bac7-836db4b8b9ee", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "105b2118-b22c-4ef5-bac7-836db4b8b9ee", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "105b2118-b22c-4ef5-bac7-836db4b8b9ee", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "1d5569e3-278c-4cf3-860e-712010333fe6", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "7a2c8b8e-2e28-4f10-b04f-9b313c60c0bb", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "99939b90-e88c-4c2f-ba78-56d455611703", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "99939b90-e88c-4c2f-ba78-56d455611703", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ac07e230-0297-4e1d-bdfe-119010e0ad8e", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b8238e36-625f-460d-9e39-fd501e65490c", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b8238e36-625f-460d-9e39-fd501e65490c", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b8238e36-625f-460d-9e39-fd501e65490c", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b8238e36-625f-460d-9e39-fd501e65490c", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ac555709-c7cc-4c64-8a6f-8fe2bc149fcd", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "ac555709-c7cc-4c64-8a6f-8fe2bc149fcd", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "42391fa7-6172-487c-b8aa-d41ab7c64973", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "42391fa7-6172-487c-b8aa-d41ab7c64973", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "42391fa7-6172-487c-b8aa-d41ab7c64973", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "42391fa7-6172-487c-b8aa-d41ab7c64973", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "e7472958-dd1b-48a7-a960-ec2ef3b69ded", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "e7472958-dd1b-48a7-a960-ec2ef3b69ded", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a6fc4db9-a29c-4f50-8e41-105b45af0be9", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a6fc4db9-a29c-4f50-8e41-105b45af0be9", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a6fc4db9-a29c-4f50-8e41-105b45af0be9", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a6fc4db9-a29c-4f50-8e41-105b45af0be9", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "9620716d-9be8-4ebd-80d2-679373f4f897", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a4624976-3773-4a1e-b725-5f6efce147a5", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a4624976-3773-4a1e-b725-5f6efce147a5", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a4624976-3773-4a1e-b725-5f6efce147a5", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a4624976-3773-4a1e-b725-5f6efce147a5", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "67483891-36d1-46f2-8b4f-b8b7bd54bdcc", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "67483891-36d1-46f2-8b4f-b8b7bd54bdcc", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "9b76bcd4-580a-4435-afe9-290940b1837f", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "9b76bcd4-580a-4435-afe9-290940b1837f", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "9b76bcd4-580a-4435-afe9-290940b1837f", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "9b76bcd4-580a-4435-afe9-290940b1837f", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "5d65c22b-7640-4433-930b-4bc381ac7361", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "5d65c22b-7640-4433-930b-4bc381ac7361", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "5d65c22b-7640-4433-930b-4bc381ac7361", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "5d65c22b-7640-4433-930b-4bc381ac7361", 0, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "30233158-01b4-4f14-b7d2-d0377273f6c3", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "30233158-01b4-4f14-b7d2-d0377273f6c3", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "30233158-01b4-4f14-b7d2-d0377273f6c3", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "30233158-01b4-4f14-b7d2-d0377273f6c3", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b3205343-03f8-4ffd-8bbc-6df1ae5621b4", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b3205343-03f8-4ffd-8bbc-6df1ae5621b4", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b3205343-03f8-4ffd-8bbc-6df1ae5621b4", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "b3205343-03f8-4ffd-8bbc-6df1ae5621b4", 1, 0, 0, 0, 0, 0, 1);
INSERT INTO decksToCards VALUES(NULL, 1, "a5c7d16b-8f4e-42b9-be24-3cb091932d7c", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "a5c7d16b-8f4e-42b9-be24-3cb091932d7c", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "a5c7d16b-8f4e-42b9-be24-3cb091932d7c", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "e9be371c-c688-44ad-ab71-bd4c9f242d58", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "e9be371c-c688-44ad-ab71-bd4c9f242d58", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "e9be371c-c688-44ad-ab71-bd4c9f242d58", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "4d84ac44-01d8-415e-af69-7c608ac8ae20", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "4d84ac44-01d8-415e-af69-7c608ac8ae20", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "9620716d-9be8-4ebd-80d2-679373f4f897", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "9620716d-9be8-4ebd-80d2-679373f4f897", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "9620716d-9be8-4ebd-80d2-679373f4f897", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "88bf4af9-4b14-43e7-9d50-0e6a895cece1", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "9cbd346e-098a-4cf6-a72f-468376fd2e8f", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "f56a5a73-5f10-4f97-989f-7cea0a8d95e3", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO decksToCards VALUES(NULL, 1, "3bb17913-fe4d-4acd-9b75-71f5a90f898b", 0, 0, 0, 1, 0, 0, 0);