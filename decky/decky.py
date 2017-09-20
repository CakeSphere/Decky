import os, sqlite3, sass, json, smartypants, re

from pprint import pprint
from HTMLParser import HTMLParser
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from sassutils.wsgi import SassMiddleware
from datetime import datetime
from math import ceil

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
        pos_json for pos_json in os.listdir(path_to_json)
        if pos_json.endswith('.json')
    ]
    for file in json_files:
        with open(os.path.join(path_to_json, file)) as json_file:
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
        pos_json for pos_json in os.listdir(path_to_json)
        if pos_json.endswith('.json')
    ]
    for file in json_files:
        with open(os.path.join(path_to_json, file)) as json_file:
            set_data = json.load(json_file)
            set_data = format_set(set_data)
            print "\033[96m\033[1m" + set_data["code"] + " " + set_data[
                "name"] + "\n\033[0m\033[94m"
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
                    6) + " " + card_data["name"]
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


@app.route('/decks/', defaults={'page': 1})
@app.route('/decks/page/<int:page>')
def decks(page):
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
@app.route('/cards/page/<int:page>')
def cards(page):
    db = get_db()
    cur_count = db.execute(
        'SELECT COUNT(*) FROM cards WHERE type LIKE "%Vampire%" AND type LIKE "%Creature%" AND multiverseid != ""'
    )
    count = cur_count.fetchone()[0]
    cur_cards = db.execute(
        'SELECT * FROM cards WHERE type LIKE "%Vampire%" AND type LIKE "%Creature%" AND multiverseid != "" ORDER BY releaseDate DESC, multiverseid DESC LIMIT '
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
        # Convert new lines to html line breaks
        text = Markup('<br>'.join(text.split('\n')))
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
    # Convert new lines to html line breaks
    card_text = Markup('<br>'.join(card_text.split('\n')))
    card_flavor = card['flavor']
    card_flavor = Markup('<br>'.join(card_flavor.split('\n')))
    return render_template(
        'card.html',
        card=card,
        card_text=card_text,
        card_mana=card_mana,
        card_flavor=card_flavor,
        flip_card_a=flip_card_a,
        flip_card_b=flip_card_b)


@app.route('/deck/<id>')
def deck(id):
    db = get_db()
    cur = db.execute('SELECT * FROM decks WHERE id="' + id + '"')
    deck = cur.fetchone()
    if not deck:
        abort(404)
    cur = db.execute(
        'SELECT name, count(name), type, multiverseid FROM decksToCards INNER JOIN cards ON cardId=cards.multiverseid WHERE deckId=1 GROUP BY name'
    )
    cards = cur.fetchall()
    count = {}
    for card in cards:
        card_count = card[1]
        count[card["multiverseid"]] = card_count
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
        deck=deck,
        cards=cards,
        deck_tags=deck_tags,
        deck_legality=deck_legality,
        deck_created=deck_created,
        deck_updated=deck_updated,
        count=count,
        deck_description=deck_description)


@app.route('/builder')
def builder():
    db = get_db()
    cur_cards = db.execute(
        'SELECT * FROM cards WHERE type LIKE "%Spirit%" AND type LIKE "%Creature%" ORDER BY multiverseId ASC LIMIT 3'
    )
    cur_decks = db.execute('SELECT * FROM decks ORDER BY likes DESC LIMIT 33')
    cur_sets = db.execute(
        'SELECT * FROM sets ORDER BY releaseDate DESC LIMIT 5')
    decks = cur_decks.fetchall()
    cards = cur_cards.fetchall()
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
        'builder.html',
        cards=cards,
        sets=sets,
        decks=decks,
        tags=tags,
        legality=legality)


@app.route('/add_deck', methods=['POST'])
def add_deck():
    deck_author = "Casanova Killing Spree"
    deck_colors = "{r}{b}"
    deck_description = request.form['description']
    deck_formats = request.form['formats']
    deck_image = "414494"
    deck_legality = "Standard"
    deck_likes = 99
    deck_mainboard = "main"
    deck_maybeboard = "maybe"
    deck_name = request.form['name'].strip().title()
    deck_sideboard = "side"
    deck_tags = request.form['tags']

    if deck_name == "":
      error = Markup("<strong>Oops!</strong>")
      flash(error + " Looks like your deck doesn't have a name.", 'error')
    else:
      db = get_db()
      db.execute(
          'INSERT INTO decks values (null, ?, ?, null, date("now"), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date("now"))',
          [
              deck_author, deck_colors, deck_description, deck_formats,
              deck_image, deck_legality, deck_likes, deck_mainboard,
              deck_maybeboard, deck_name, deck_sideboard, deck_tags
          ])
      db.commit()

      success = Markup("<strong>Double, double toil and trouble.</strong> ")
      flash(success + deck_name + " was brewed successfully!", 'success')

    return redirect(url_for('decks'))


@app.route('/login')
def index():
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
