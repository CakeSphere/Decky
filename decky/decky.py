import os, sqlite3, sass, json, smartypants, re

from pprint import pprint
from HTMLParser import HTMLParser
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from sassutils.wsgi import SassMiddleware
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {'decky': ('static/sass', 'static/css', '/static/css')})

app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, 'decky.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'))

print app.root_path

path_to_json = app.root_path + '/static/json'

app.config.from_envvar('DECKY_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def format_set(raw_set):
    out_set = {}
    fields = {
     "name", \
     "code", \
     "gathererCode", \
     "oldCode", \
     "magicCardsInfoCode", \
     "releaseDate", \
     "border", \
     "type", \
     "block", \
     "cards"}
    for field in fields:
        if field in raw_set:
            out_set[field] = raw_set[field]
        else:
            out_set[field] = ""
    return out_set


def format_card(raw_card):
    out_card = {}
    fields = {
     "layout", \
     "name", \
     "names", \
     "manaCost", \
     "cmc", \
     "colors", \
     "colorIdentity", \
     "type", \
     "supertypes", \
     "types", \
     "subtypes", \
     "rarity", \
     "text", \
     "flavor", \
     "artist", \
     "number", \
     "power", \
     "toughness", \
     "loyalty", \
     "multiverseid", \
     "variations", \
     "watermark", \
     "border", \
     "timeshifted", \
     "hand", \
     "life", \
     "reserved", \
     "releaseDate", \
     "starter", \
     "mciNumber", \
     "imageName" }
    for field in fields:
        if field in raw_card:
            out_card[field] = raw_card[field]
            if isinstance(out_card[field], list):
                out_card[field] = unicode(", ".join([
                    unicode(out_card[field][x])
                    for x in range(len(out_card[field]))
                ]))
        else:
            out_card[field] = ""

    def format_HTML(text):
        text = HTMLParser().unescape(smartypants.smartypants(text))
        return text

    out_card['name'] = format_HTML(out_card['name'])
    out_card['text'] = format_HTML(out_card['text'])
    out_card['flavor'] = format_HTML(out_card['flavor'])
    return out_card


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('\033[92m\033[1mInitialized the database.\033[0m')


@app.cli.command('import_sets')
def import_sets():
    init_db()
    print('\033[92m\033[1mInitialized the database.\033[0m')
    json_files = [
        pos_json for pos_json in os.listdir(path_to_json)
        if pos_json.endswith('.json')
    ]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            set_data = json.load(json_file)
            set_data = format_set(set_data)
            print "\033[95m" + 'set_data["name"])'
            db = get_db()
            import_sets_query = "INSERT INTO 'sets' (name, code, gathererCode, oldCode, magicCardsInfoCode, releaseDate, border, type, block) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
            db.execute(import_sets_query, \
             (set_data["name"], \
             set_data["code"], \
             set_data["gathererCode"], \
             set_data["oldCode"], \
             set_data["magicCardsInfoCode"], \
             set_data["releaseDate"], \
             set_data["border"], \
             set_data["type"], \
             set_data["block"]))
            db.commit()
    print "\033[92m\033[1mSets imported.\033[0m"


@app.cli.command('import_cards')
def import_cards():
    init_db()
    print('\033[92m\033[1mInitialized the database.\033[0m')
    db = get_db()
    json_files = [
        pos_json for pos_json in os.listdir(path_to_json)
        if pos_json.endswith('.json')
    ]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            set_data = json.load(json_file)
            set_data = format_set(set_data)
            print "\033[96m\033[1m" + set_data["name"] + "\n\033[0m\033[94m"
            import_sets_query = "INSERT INTO 'sets' (name, code, gathererCode, oldCode, magicCardsInfoCode, releaseDate, border, type, block) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
            db.execute(import_sets_query, \
             (set_data["name"],\
             set_data["code"].lower(),\
             set_data["gathererCode"],\
             set_data["oldCode"],\
             set_data["magicCardsInfoCode"],\
             set_data["releaseDate"],\
             set_data["border"],\
             set_data["type"],\
             set_data["block"]))
            for card_data in set_data["cards"]:
                card_data = format_card(card_data)
                import_cards_query = 'INSERT INTO `cards` (layout, name, names, manaCost, cmc, colors, colorIdentity, type, supertypes, types, subtypes, rarity, text, flavor, artist, number, power, toughness, loyalty, multiverseid, variations, watermark, border, timeshifted, hand, life, reserved, releaseDate, starter, mciNumber, imageName, setId, setCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
                print card_data["name"]
                db.execute(import_cards_query, \
                 (card_data["layout"], \
                  card_data["name"], \
                  card_data["names"], \
                  card_data["manaCost"], \
                  card_data["cmc"], \
                  card_data["colors"], \
                  card_data["colorIdentity"], \
                  card_data["type"], \
                  card_data["supertypes"], \
                  card_data["types"], \
                  card_data["subtypes"], \
                  card_data["rarity"], \
                  card_data["text"], \
                  card_data["flavor"], \
                  card_data["artist"], \
                  card_data["number"], \
                  card_data["power"], \
                  card_data["toughness"], \
                  card_data["loyalty"], \
                  card_data["multiverseid"], \
                  card_data["variations"], \
                  card_data["watermark"], \
                  card_data["border"], \
                  card_data["timeshifted"], \
                  card_data["hand"], \
                  card_data["life"], \
                  card_data["reserved"], \
                  card_data["releaseDate"], \
                  card_data["starter"], \
                  card_data["mciNumber"], \
                  card_data["imageName"], \
                  set_data["name"], \
                  set_data["code"]))
            db.commit()
            print "\n\033[96m\033[1mSet imported.\033[0m \n"
    print "\033[95m\033[1mAll cards imported.\033[0m"


@app.route('/show_entries')
def show_entries():
    db = get_db()
    cur = db.execute('select * from cards order by multiverseid asc')
    cur_sets = db.execute(
        'select *, block from sets order by releaseDate desc')
    cards = cur.fetchall()
    sets = cur_sets.fetchall()
    return render_template('show_entries.html', cards=cards, sets=sets)


@app.route('/decks')
def decks():
    db = get_db()
    cur = db.execute(
        'select * from cards where colorIdentity="U" or colorIdentity="B" or colorIdentity="G" order by multiverseId asc limit 33'
    )
    cur_sets = db.execute(
        'select * from sets order by releaseDate desc limit 5')
    cards = cur.fetchall()
    sets = cur_sets.fetchall()
    return render_template('decks.html', cards=cards, sets=sets)


@app.route('/cards')
def cards():
    db = get_db()
    cur = db.execute(
        'select * from cards where type like "%Vampire%" and type like "%Creature%" and multiverseid != "" order by multiverseid desc limit 45'
    )
    cur_sets = db.execute(
        'select * from sets order by releaseDate desc limit 5')
    cards = cur.fetchall()
    cardMana = {}
    for card in cards:
        mana = card["manaCost"]
        mana = mana.replace('}{', ' ')
        mana = mana.replace('{', '')
        mana = mana.replace('}', '')
        mana = mana.replace('/', '')
        cardMana[card["id"]] = mana
    cardText = {}
    for card in cards:
        text = card["text"]
        # Italicize ability words
        text = re.compile(
            r'(((battalion|bloodrush|channel|chroma|cohort|constellation|converge|council\'s dilemma|delirium|domain|fateful hour|ferocious|formidable|grandeur|hellbent|heroic|imprint|inspired|join forces|kinship|landfall|lieutenant|metalcraft|morbid|parley|radiance|raid|rally|revolt|spell mastery|strive|sweep|tempting offer|threshold|will of the council)\s*?)+)',
            re.I).sub(r'<em>\1</em>', text)
        # Making keyword abilities links so they can be used for tooltips and to
        # link to the glossary eventually
        text = re.compile(
            r'(((Deathtouch|Defender|Double Strike|Enchant|Equip|First Strike|Flash|Flying|Haste|Hexproof|Indestructible|Intimidate|Landwalk|Lifelink|Protection|Reach|Shroud|Trample|Vigilance|Banding|Rampage|Cumulative Upkeep|Flanking|Phasing|Buyback|Shadow|Cycling|Echo|Horsemanship|Fading|Kicker|Flashback|Madness|Fear|Morph|Amplify|Provoke|Storm|Affinity|Entwine|Modular|Sunburst|Bushido|Soulshift|Splice|Offering|Ninjutsu|Epic|Convoke|Dredge|Transmute|Bloodthirst|Haunt|Replicate|Forecast|Graft|Recover|Ripple|Split Second|Suspend|Vanishing|Absorb|Aura Swap|Delve|Fortify|Frenzy|Gravestorm|Poisonous|Transfigure|Champion|Changeling|Evoke|Hideaway|Prowl|Reinforce|Conspire|Persist|Wither|Retrace|Devour|Exalted|Unearth|Cascade|Annihilator|Level Up|Rebound|Totem Armor|Infect|Battle Cry|Living Weapon|Undying|Miracle|Soulbond|Overload|Scavenge|Unleash|Cipher|Evolve|Extort|Fuse|Bestow|Tribute|Dethrone|Hidden Agenda|Outlast|Prowess|Dash|Exploit|Menace|Renown|Awaken|Devoid|Ingest|Myriad|Surge|Skulk|Emerge|Escalate|Melee|Crew|Fabricate|Partner|Undaunted|Improvise|Aftermath|Embalm|Eternalize|Afflict)\s*?)+)',
            re.I
        ).sub(
            r'<span class="tooltip" href="tooltip" title="Keyword Ability: \1">\1</span>',
            text)
        # Convert mana symbols to styled span elements
        text = text.replace('{', '<span class="mana small shadow s')
        text = text.replace('}', '">&nbsp;</span>')
        # Text on cards in parentheses is always italicized
        text = text.replace('(', '<em class="card-explanation">(')
        text = text.replace(')', ')</em>')
        # Convert new lines to html line breaks
        text = Markup('<br>'.join(text.split('\n')))
        cardText[card["id"]] = text
    sets = cur_sets.fetchall()
    return render_template(
        'cards.html',
        cards=cards,
        sets=sets,
        cardMana=cardMana,
        cardText=cardText)


@app.route('/card/<multiverseId>')
def card(multiverseId):
    db = get_db()
    cur = db.execute('select * from cards where multiverseId="' + multiverseId
                     + '"')
    card = cur.fetchone()
    cardNumber = card['number']
    flipCardA = False
    flipCardB = False
    if re.search('[a]', unicode(cardNumber)):
        flipCardA = True
    if re.search('[b]', unicode(cardNumber)):
        flipCardB = True
    cardMana = card['manaCost']
    cardMana = cardMana.replace('}{', ' ')
    cardMana = cardMana.replace('{', '')
    cardMana = cardMana.replace('}', '')
    cardMana = cardMana.replace('/', '')
    cardText = card["text"]
    # Italicize ability words
    cardText = re.compile(
        r'(((battalion|bloodrush|channel|chroma|cohort|constellation|converge|council\'s dilemma|delirium|domain|fateful hour|ferocious|formidable|grandeur|hellbent|heroic|imprint|inspired|join forces|kinship|landfall|lieutenant|metalcraft|morbid|parley|radiance|raid|rally|revolt|spell mastery|strive|sweep|tempting offer|threshold|will of the council)\s*?)+)',
        re.I).sub(r'<em>\1</em>', cardText)
    # Making keyword abilities links so they can be used for tooltips and to
    # link to the glossary eventually
    cardText = re.compile(
        r'(((Deathtouch|Defender|Double Strike|Enchant|Equip|First Strike|Flash|Flying|Haste|Hexproof|Indestructible|Intimidate|Landwalk|Lifelink|Protection|Reach|Shroud|Trample|Vigilance|Banding|Rampage|Cumulative Upkeep|Flanking|Phasing|Buyback|Shadow|Cycling|Echo|Horsemanship|Fading|Kicker|Flashback|Madness|Fear|Morph|Amplify|Provoke|Storm|Affinity|Entwine|Modular|Sunburst|Bushido|Soulshift|Splice|Offering|Ninjutsu|Epic|Convoke|Dredge|Transmute|Bloodthirst|Haunt|Replicate|Forecast|Graft|Recover|Ripple|Split Second|Suspend|Vanishing|Absorb|Aura Swap|Delve|Fortify|Frenzy|Gravestorm|Poisonous|Transfigure|Champion|Changeling|Evoke|Hideaway|Prowl|Reinforce|Conspire|Persist|Wither|Retrace|Devour|Exalted|Unearth|Cascade|Annihilator|Level Up|Rebound|Totem Armor|Infect|Battle Cry|Living Weapon|Undying|Miracle|Soulbond|Overload|Scavenge|Unleash|Cipher|Evolve|Extort|Fuse|Bestow|Tribute|Dethrone|Hidden Agenda|Outlast|Prowess|Dash|Exploit|Menace|Renown|Awaken|Devoid|Ingest|Myriad|Surge|Skulk|Emerge|Escalate|Melee|Crew|Fabricate|Partner|Undaunted|Improvise|Aftermath|Embalm|Eternalize|Afflict)\s*?)+)',
        re.I).sub(r'<a href="tooltip" title="Keyword Ability: \1">\1</a>',
                  cardText)
    # Convert mana symbols to styled span elements
    cardText = cardText.replace('{', '<span class="mana medium shadow s')
    cardText = cardText.replace('}', '">&nbsp;</span>')
    # Text on cards in parentheses is always italicized
    cardText = cardText.replace('(', '<em class="card-explanation">(')
    cardText = cardText.replace(')', ')</em>')
    # Convert new lines to html line breaks
    cardText = Markup('<br>'.join(cardText.split('\n')))
    cardFlavor = card['flavor']
    cardFlavor = Markup('<br>'.join(cardFlavor.split('\n')))
    return render_template(
        'card.html',
        card=card,
        cardText=cardText,
        cardMana=cardMana,
        cardFlavor=cardFlavor,
        flipCardA=flipCardA,
        flipCardB=flipCardB)


@app.route('/deck/<id>')
def deck(id):
    db = get_db()
    cur = db.execute('SELECT * FROM decks WHERE id="' + id + '"')
    deck = cur.fetchone()
    cur = db.execute(
        'SELECT name, count(name), type, multiverseid FROM decksToCards INNER JOIN cards ON cardId=cards.multiverseid WHERE deckId=1 GROUP BY name'
    )
    cards = cur.fetchall()
    count = {}
    for card in cards:
        card_count = card[1]
        count[card["multiverseid"]] = card_count
    deckTags = deck["tags"]
    deckTags = deckTags.split(', ')
    deckLegality = deck["legality"]
    deckLegality = deckLegality.split(', ')


    def isToday(date):
        if (date == datetime.now().strftime("%B %d, %Y")):
            date = "today"
            return date
        else:
            return date

    def formatDate(date):
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime("%B %d, %Y")
        date = isToday(date)
        return date

    deckCreated = formatDate(deck["created"])
    deckUpdated = formatDate(deck["updated"])
    deckDescription = deck["description"]
    # Convert new lines to html line breaks
    deckDescription = Markup('</p><p>'.join(deckDescription.split('\n')))
    return render_template(
        'deck.html',
        deck=deck,
        cards=cards,
        deckTags=deckTags,
        deckLegality=deckLegality,
        deckCreated=deckCreated,
        deckUpdated=deckUpdated, 
        count=count,
        deckDescription=deckDescription)


@app.route('/builder')
def builder():
    db = get_db()
    cur = db.execute(
        'select * from cards where type like "%Spirit%" and type like "%Creature%" order by multiverseId asc limit 3'
    )
    cur_sets = db.execute(
        'select * from sets order by releaseDate desc limit 5')
    cards = cur.fetchall()
    sets = cur_sets.fetchall()
    return render_template('builder.html', cards=cards, sets=sets)


@app.route('/login')
def index():
    return render_template('login.html')
