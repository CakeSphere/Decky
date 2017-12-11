import os, sqlite3, sass, json, smartypants, re, sys

from pprint import pprint
from HTMLParser import HTMLParser
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, jsonify, Response
from sassutils.wsgi import SassMiddleware
from datetime import datetime
from math import ceil
from random import randint
from titlecase import titlecase

reload(sys)
sys.setdefaultencoding('utf8')

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

PER_PAGE = 45
ABILITY_WORDS = [
    "battalion", "bloodrush", "channel", "chroma", "cohort", "constellation",
    "converge", "council\'s dilemma", "delirium", "domain", "fateful hour",
    "ferocious", "formidable", "grandeur", "hellbent", "heroic", "imprint",
    "inspired", "join forces", "kinship", "landfall", "lieutenant",
    "metalcraft", "morbid", "parley", "radiance", "raid", "rally", "revolt",
    "spell mastery", "strive", "sweep", "tempting offer", "threshold",
    "will of the council", "eminence"
]
KEYWORD_ABILITIES = [
    "Deathtouch", "Defender", "Double Strike", "Enchant", "Equip",
    "First Strike", "Flash", "Flying", "Haste", "Hexproof", "Indestructible",
    "Intimidate", "Landwalk", "Lifelink", "Protection", "Reach", "Shroud",
    "Trample", "Vigilance", "Banding", "Rampage", "Cumulative Upkeep",
    "Flanking", "Phasing", "Buyback", "Shadow", "Cycling", "Echo",
    "Horsemanship", "Fading", "Kicker", "Flashback", "Madness", "Fear",
    "Morph", "Amplify", "Provoke", "Storm", "Affinity", "Entwine", "Modular",
    "Sunburst", "Bushido", "Soulshift", "Splice", "Offering", "Ninjutsu",
    "Epic", "Convoke", "Dredge", "Transmute", "Bloodthirst", "Haunt",
    "Replicate", "Forecast", "Graft", "Recover", "Ripple", "Split Second",
    "Suspend", "Vanishing", "Absorb", "Aura Swap", "Delve", "Fortify",
    "Frenzy", "Gravestorm", "Poisonous", "Transfigure", "Champion",
    "Changeling", "Evoke", "Hideaway", "Prowl", "Reinforce", "Conspire",
    "Persist", "Wither", "Retrace", "Devour", "Exalted", "Unearth", "Cascade",
    "Annihilator", "Level Up", "Rebound", "Totem Armor", "Infect",
    "Battle Cry", "Living Weapon", "Undying", "Miracle", "Soulbond",
    "Overload", "Scavenge", "Unleash", "Cipher", "Evolve", "Extort", "Fuse",
    "Bestow", "Tribute", "Dethrone", "Hidden Agenda", "Outlast", "Prowess",
    "Dash", "Exploit", "Menace", "Renown", "Awaken", "Devoid", "Ingest",
    "Myriad", "Surge", "Skulk", "Emerge", "Escalate", "Melee", "Crew",
    "Fabricate", "Partner", "Undaunted", "Improvise", "Aftermath", "Embalm",
    "Eternalize", "Afflict"
]

PATH_TO_JSON = app.root_path + '/static/json'

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


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self,
                   left_edge=1,
                   left_current=1,
                   right_current=1,
                   right_edge=1):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


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
        pos_json for pos_json in os.listdir(PATH_TO_JSON)
        if pos_json.endswith('.json')
    ]
    for file in json_files:
        with open(os.path.join(PATH_TO_JSON, file)) as json_file:
            set_data = json.load(json_file)
            set_data = format_set(set_data)
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
            print "\033[95m" + set_data["name"]
    print "\033[92m\033[1mAll sets imported.\033[0m"


@app.cli.command('import_cards')
def import_cards():
    init_db()
    print('\033[92m\033[1mInitialized the database.\033[0m')
    db = get_db()
    json_files = [
        pos_json for pos_json in os.listdir(PATH_TO_JSON)
        if pos_json.endswith('.json')
    ]
    for file in json_files:
        with open(os.path.join(PATH_TO_JSON, file)) as json_file:
            set_data = json.load(json_file)
            set_data = format_set(set_data)
            print "\033[96m\033[1m" + set_data["code"].encode(
                "utf8") + " " + set_data["name"].encode(
                    "utf8") + "\n\033[0m\033[94m"
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
                print str(card_data["multiverseid"]).zfill(
                    6) + " " + card_data["name"].encode("utf8")
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


@app.route('/show_entries/<setId>')
def show_entries(setId):
    db = get_db()
    cur_cards = db.execute('select * from cards where setId like "%' + setId +
                           '%" order by multiverseid asc')
    cur_sets = db.execute('select *, block from sets where name like "%' +
                          setId + '%" order by releaseDate desc')
    cards = cur_cards.fetchall()
    sets = cur_sets.fetchall()
    return render_template('show_entries.html', cards=cards, sets=sets)


@app.route('/', defaults={'page': 1})
@app.route('/decks/', defaults={'page': 1})
@app.route('/decks/<int:page>')
def decks(page):
    PER_PAGE = 36
    db = get_db()
    cur_count = db.execute('select count(*) from decks')
    count = cur_count.fetchone()[0]
    cur_decks = db.execute('select * from decks order by likes desc limit ' +
                           str(PER_PAGE) + ' offset ' + str(PER_PAGE * page -
                                                            PER_PAGE))
    pagination = Pagination(page, PER_PAGE, count)
    cur_sets = db.execute(
        'select * from sets order by releaseDate desc limit 5')
    decks = cur_decks.fetchall()
    sets = cur_sets.fetchall()
    legality = {}
    tags = {}
    for deck in decks:
        deck_tags = deck["tags"]
        deck_tags = deck_tags.split(', ')
        tags[deck["id"]] = deck_tags
        deck_legality = deck["legality"]
        deck_legality = deck_legality.split(', ')
        legality[deck["id"]] = deck_legality

    return render_template(
        'decks.html',
        decks=decks,
        sets=sets,
        tags=tags,
        legality=legality,
        pagination=pagination)


@app.route('/cards/', defaults={'page': 1})
@app.route('/cards/<int:page>')
def cards(page):
    db = get_db()
    cur_count = db.execute(
        'SELECT COUNT(*) FROM cards WHERE multiverseid != "" AND releaseDate ==""'
    )
    count = cur_count.fetchone()[0]
    cur_cards = db.execute(
        'SELECT * FROM cards WHERE multiverseid != "" AND releaseDate == "" ORDER BY multiverseId DESC LIMIT '
        + str(PER_PAGE) + ' offset ' + str(PER_PAGE * page - PER_PAGE))
    cur_sets = db.execute(
        'SELECT * FROM sets ORDER BY releaseDate DESC LIMIT 5')
    cards = cur_cards.fetchall()
    pagination = Pagination(page, PER_PAGE, count)
    card_mana = {}
    for card in cards:
        mana = card["manaCost"]
        mana = mana.replace('}{', ' ')
        mana = mana.replace('{', '')
        mana = mana.replace('}', '')
        mana = mana.replace('/', '')
        card_mana[card["id"]] = mana
    card_text = {}
    for card in cards:
        text = card["text"]
        # Italicize ability words
        text = re.compile(r'(((' + '|'.join(ABILITY_WORDS) + ')\s*?)+)',
                          re.I).sub(r'<em>\1</em>', text)
        # Making keyword abilities links so they can be used for tooltips and to
        # link to the glossary eventually
        text = re.compile(
            r'(((' + '|'.join(KEYWORD_ABILITIES) + ')\s*?)+)', re.I
        ).sub(
            r'<span class="tooltip" href="tooltip" title="Keyword Ability: \1">\1</span>',
            text)
        # Convert mana symbols to styled span elements
        text = text.replace('{', '<span class="mana small shadow s')
        text = text.replace('}', '">&nbsp;</span>')
        # Text on cards in parentheses is always italicized
        text = text.replace('(', '<em class="card-explanation">(')
        text = text.replace(')', ')</em>')
        text = text.replace('sW/U', 'swu')
        text = text.replace('sW/B', 'swb')
        text = text.replace('sU/B', 'sub')
        text = text.replace('sU/R', 'sur')
        text = text.replace('sB/R', 'sbr')
        text = text.replace('sB/G', 'sbg')
        text = text.replace('sR/W', 'srw')
        text = text.replace('sR/G', 'srg')
        text = text.replace('sG/W', 'sgw')
        text = text.replace('sG/U', 'sgu')
        # Convert new lines to html line breaks
        text = Markup('</p><p>'.join(text.split('\n')))
        card_text[card["id"]] = text
    sets = cur_sets.fetchall()
    return render_template(
        'cards.html',
        cards=cards,
        sets=sets,
        card_mana=card_mana,
        card_text=card_text,
        pagination=pagination)


@app.route('/card/<multiverseId>')
def card(multiverseId):
    db = get_db()
    cur = db.execute('SELECT * FROM cards WHERE multiverseId="' + multiverseId
                     + '"')
    card = cur.fetchone()
    if not card:
        abort(404)
    cur_decks = db.execute(
        'SELECT DISTINCT decks.id, name, tags, legality, image, likes FROM decksToCards INNER JOIN decks ON deckId=decks.id WHERE cardId=(?) ORDER BY likes DESC',
        (card['multiverseId'], ))
    decks = cur_decks.fetchall()
    legality = {}
    tags = {}
    for deck in decks:
        deck_tags = deck["tags"]
        deck_tags = deck_tags.split(', ')
        tags[deck["id"]] = deck_tags
        deck_legality = deck["legality"]
        deck_legality = deck_legality.split(', ')
        legality[deck["id"]] = deck_legality
    card_number = card['number']
    flip_card_a = False
    flip_card_b = False
    if re.search('[a]', unicode(card_number)):
        flip_card_a = True
    if re.search('[b]', unicode(card_number)):
        flip_card_b = True
    card_mana = card['manaCost']
    card_mana = card_mana.replace('}{', ' ')
    card_mana = card_mana.replace('{', '')
    card_mana = card_mana.replace('}', '')
    card_mana = card_mana.replace('/', '')
    card_text = card["text"]
    # Italicize ability words
    card_text = re.compile(r'(((' + '|'.join(ABILITY_WORDS) + ')\s*?)+)',
                           re.I).sub(r'<em>\1</em>', card_text)
    # Making keyword abilities links so they can be used for tooltips and to
    # link to the glossary eventually
    card_text = re.compile(
        r'(((' + '|'.join(KEYWORD_ABILITIES) + ')\s*?)+)', re.I).sub(
            r'<a href="tooltip" title="Keyword Ability: \1">\1</a>', card_text)
    # Convert mana symbols to styled span elements
    card_text = card_text.replace('{', '<span class="mana medium shadow s')
    card_text = card_text.replace('}', '">&nbsp;</span>')
    # Text on cards in parentheses is always italicized
    card_text = card_text.replace('(', '<em class="card-explanation">(')
    card_text = card_text.replace(')', ')</em>')
    card_text = card_text.replace('sW/U', 'swu')
    card_text = card_text.replace('sW/B', 'swb')
    card_text = card_text.replace('sU/B', 'sub')
    card_text = card_text.replace('sU/R', 'sur')
    card_text = card_text.replace('sB/R', 'sbr')
    card_text = card_text.replace('sB/G', 'sbg')
    card_text = card_text.replace('sR/W', 'srw')
    card_text = card_text.replace('sR/G', 'srg')
    card_text = card_text.replace('sG/W', 'sgw')
    card_text = card_text.replace('sG/U', 'sgu')
    # Convert new lines to html line breaks
    card_text = Markup('</p><p>'.join(card_text.split('\n')))
    card_flavor = card['flavor']
    card_flavor = Markup('</p><p>'.join(card_flavor.split('\n')))
    return render_template(
        'card.html',
        card=card,
        card_text=card_text,
        card_mana=card_mana,
        card_flavor=card_flavor,
        flip_card_a=flip_card_a,
        flip_card_b=flip_card_b,
        decks=decks,
        legality=legality,
        tags=tags)


@app.route('/deck/<id>')
def deck(id):
    db = get_db()
    cur = db.execute('SELECT * FROM decks WHERE id="' + id + '"')
    deck = cur.fetchone()
    if not deck:
        abort(404)
    cur = db.execute(
        'SELECT name, count(name), type, multiverseid, foil, featured, commander FROM decksToCards INNER JOIN cards ON cardId=cards.multiverseid WHERE deckId="'
        + id + '" GROUP BY name')
    cards = cur.fetchall()
    count = {}
    foil = {}
    commander = {}
    lands = {}
    planeswalkers = {}
    creatures = {}
    sorceries = {}
    instants = {}
    enchantments = {}
    artifacts = {}
    for card in cards:
        card_count = card[1]
        count[card["multiverseid"]] = card_count
        card_foil = card['foil']
        foil[card["multiverseid"]] = card_foil
        card_commander = card['commander']
        commander[card["multiverseid"]] = card_commander

        # Sort the cards by type
        if "Land" in card["type"]:
            lands[card['multiverseid']] = card
        if "Planeswalker" in card["type"]:
            planeswalkers[card['multiverseid']] = card
        if "Creature" in card["type"] and "Land" not in card["type"]:
            creatures[card['multiverseid']] = card
        if "Sorcery" in card["type"]:
            sorceries[card['multiverseid']] = card
        if "Instant" in card["type"]:
            instants[card['multiverseid']] = card
        if "Enchantment" in card["type"] and "Artifact" not in card[
                "type"] and "Creature" not in card["type"]:
            enchantments[card['multiverseid']] = card
        if "Artifact" in card["type"] and "Creature" not in card["type"]:
            artifacts[card['multiverseid']] = card

    deck_image = deck["image"]
    deck_tags = deck["tags"]
    deck_tags = deck_tags.split(', ')
    deck_legality = deck["legality"]
    deck_legality = deck_legality.split(', ')

    def is_today(date):
        if (date == datetime.now().strftime("%B %d, %Y")):
            date = "today"
            return date
        else:
            return date

    def format_date(date):
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime("%B %d, %Y")
        date = is_today(date)
        return date

    deck_created = format_date(deck["created"])
    deck_updated = format_date(deck["updated"])
    deck_description = deck["description"]
    # Convert new lines to html line breaks
    deck_description = Markup('</p><p>'.join(deck_description.split('\n')))
    return render_template(
        'deck.html',
        lands=lands,
        planeswalkers=planeswalkers,
        creatures=creatures,
        sorceries=sorceries,
        instants=instants,
        enchantments=enchantments,
        artifacts=artifacts,
        deck=deck,
        cards=cards,
        foil=foil,
        deck_image=deck_image,
        deck_tags=deck_tags,
        deck_legality=deck_legality,
        deck_created=deck_created,
        deck_updated=deck_updated,
        count=count,
        commander=commander,
        deck_description=deck_description)


@app.route('/builder/', defaults={'id': False}, methods=['GET', 'POST'])
@app.route('/builder/<id>', methods=['GET', 'POST'])
def builder(id):
    db = get_db()
    card_name = request.get_json()
    card_sets = {}
    edit_mode = False
    edit_name = ''
    edit_featured = ''
    edit_formats = ''
    edit_tags = ''
    edit_description = ''
    edit_cards = ''
    edit_sets = {}
    count = ''
    commander = ''
    foil = ''
    edit_id = ''
    edit_card = {
      'edit_names': [],
      'edit_sets': [],
      'edit_ids': []
    }
    if id:
        edit_id = id
        edit_mode = True
        edit_data = db.execute('SELECT * FROM decks WHERE id=' + id + ';')
        edit_data = edit_data.fetchone()
        edit_name = edit_data["name"]
        edit_featured = edit_data["image"]
        edit_formats = edit_data["formats"]
        edit_tags = edit_data["tags"]
        edit_description = edit_data["description"]
        cur = db.execute(
            'SELECT name, setId, count(name), type, multiverseid, foil, featured, commander FROM decksToCards INNER JOIN cards ON cardId=cards.multiverseid WHERE deckId="'
            + id + '" GROUP BY name')
        edit_cards = cur.fetchall()
        count = {}
        foil = {}
        commander = {}
        for card in edit_cards:
            card_count = card[2]
            count[card["multiverseid"]] = card_count
            card_foil = card['foil']
            foil[card["multiverseid"]] = card_foil
            card_commander = card['commander']
            commander[card["multiverseid"]] = card_commander
            card_id = card["multiverseid"]
            edit_sets_data = db.execute('SELECT multiverseid, name, setId FROM cards WHERE name LIKE "' + HTMLParser().unescape(smartypants.smartypants(card[0])) + '" AND multiverseid != "" AND releaseDate == "" ORDER BY multiverseid DESC LIMIT 5 ')
            edit_sets = edit_sets_data.fetchall()
            for edit_set in edit_sets:
                edit_card['edit_names'].append(edit_set[1])
                edit_card['edit_ids'].append(str(edit_set[0]))
                edit_card['edit_sets'].append(edit_set[2])
    if card_name:
        card_name = card_name['cardName']
        card_data = db.execute(
            'SELECT multiverseid, setId, type FROM cards WHERE name LIKE "' +
            HTMLParser().unescape(smartypants.smartypants(card_name)) +
            '" AND multiverseid != "" AND releaseDate == "" ORDER BY multiverseid ASC '
        )
        card_data = card_data.fetchall()
        if card_data:
            card_id = ''
            for card in card_data:
                card_id = unicode(card[0])
                card_sets[card_id] = unicode(card[1])
                card_type = unicode(card[2])
                card_return = json.dumps({
                    'card_found': True,
                    'card_id': card_id,
                    'card_sets': card_sets,
                    'card_type': card_type
                })

            return card_return
        else:
            card_return = json.dumps({'card_found': False})
            return card_return
    return render_template(
        'builder.html',
        edit_mode=edit_mode,
        edit_id=edit_id,
        edit_name=edit_name,
        edit_formats=edit_formats,
        edit_featured=edit_featured,
        edit_tags=edit_tags,
        edit_description=edit_description,
        edit_cards=edit_cards,
        count=count,
        commander=commander,
        foil=foil,
        edit_card=edit_card)


@app.route('/add_deck', methods=['GET', 'POST'])
def add_deck():
    deck = request.get_json()
    if deck:
        deck_id = deck['edit_id']
        deck_description = deck['description']
        deck_formats = deck['formats']
        deck_legality = deck['formats']
        deck_tags = deck['tags']
        deck_name = titlecase(deck['name'].strip())
        deck_cards = deck['cards']
    # This needs to be set to the currently logged-in user.
    deck_author = "Casanova Killing Spree"
    # This needs to be calculated somehow.
    deck_colors = "{r}{b}"
    # This is based on the Featured image selected while building.
    deck_image = "414494"
    deck_likes = 0
    # These are probably obsolete.
    deck_mainboard = "main"
    deck_maybeboard = "maybe"
    deck_sideboard = "side"
    # Double checking form fields that should've been verified on the front-end.
    if deck_name == "":
        error = Markup("<strong>Oops!</strong>")
        flash(error + " Looks like your deck doesn't have a name.", 'error')
    elif deck_tags == "":
        error = Markup("<strong>Oops!</strong>")
        flash(error + " Looks like your deck doesn't have any tags.", 'error')
    elif deck_legality == "":
        error = Markup("<strong>Oops!</strong>")
        flash(error + " Looks like your deck isn't legal in any format.",
              'error')
    else:
        db = get_db()
        for card in deck_cards:
            if deck_cards[card]['featured'] == 1:
                deck_image = card
        if deck_id == '':
            cur_cards = db.execute('INSERT INTO decks values (null, ?, ?, null, date("now"), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date("now"))',(deck_author, deck_colors, deck_description, deck_formats, deck_image, deck_legality, deck_likes, deck_mainboard, deck_maybeboard, deck_name, deck_sideboard, deck_tags))

        else:
            cur_cards = db.execute('UPDATE decks SET colors = ?, description = ?, formats = ?, image = ?, legality = ?, name = ?, tags = ? WHERE id = ?',(deck_colors, deck_description, deck_formats, deck_image, deck_legality, deck_name, deck_tags, deck_id))

        deck_row = cur_cards.lastrowid
        for card in deck_cards:
            quantity = deck_cards[card]['quantity']
            for i in range(int(quantity)):
                if deck_cards[card]['foil'] == 1:
                    card_foil = 1
                else:
                    card_foil = 0
                if deck_cards[card]['featured'] == 1:
                    card_featured = 1
                else:
                    card_featured = 0
                if deck_cards[card]['commander'] == 1:
                    card_commander = 1
                else:
                    card_commander = 0
                if deck_id == '':
                    db.execute('INSERT INTO decksToCards VALUES(NULL, ' + str(
                        deck_row) + ', ' + card + ', ' + str(card_foil) + ', ' +
                               str(card_featured) + ', ' + str(
                                   card_commander) + ')')
                else:
                    db.execute('UPDATE decksToCards SET featured = 0 WHERE featured = 1;')
                    db.execute('UPDATE decksToCards SET foil = ?, featured = ?, commander = ? WHERE cardId = ?', (card_foil, card_featured, card_commander, card))
            if deck_id == '':
                print "Inserted Multiverse ID " + card + " into Deck " + str(
                    deck_row) + " " + str(quantity) + " times."
        db.commit()
        return 'success'
    return redirect(url_for('decks'))


@app.route('/login')
def index():
    return render_template('login.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/delete_deck/<id>', methods=['GET', 'POST'])
def delete_deck(id):
    db = get_db()
    db.execute('DELETE FROM decks WHERE id=' + id + ';')
    db.execute('DELETE FROM decksToCards where deckId=' + id + ';')
    db.commit()
    flash('Deck ' + id + ' was successfully deleted.', 'success')
    return redirect(url_for('decks'))


@app.errorhandler(404)
def page_not_found(e):
    version = randint(0, 2)
    return render_template('404.html', version=version), 404
