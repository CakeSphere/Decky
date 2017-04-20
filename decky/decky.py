import os, sqlite3, sass, json, datetime, smartypants, re

from pprint import pprint
from HTMLParser import HTMLParser
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from sassutils.wsgi import SassMiddleware

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

path_to_json = 'static/json'

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
					str(out_card[field][x]) for x in range(
						len(out_card[field]))
				]))
		else:
			out_card[field] = ""
	out_card['name'] = HTMLParser().unescape(
		smartypants.smartypants(out_card['name']))
	out_card['text'] = HTMLParser().unescape(
		smartypants.smartypants(out_card['text']))
	out_card['flavor'] = HTMLParser().unescape(
		smartypants.smartypants(out_card['flavor']))
	return out_card


@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('\033[92m\033[1mInitialized the database.\033[0m')


@app.cli.command('import_colors')
def import_colors():
	init_db()
	colors_query = "INSERT INTO 'colors' (name) VALUES ('White'), ('Black'), ('Blue'), ('Red'), ('Green');"
	db = get_db()
	db.execute(colors_query)
	db.commit()
	print "\033[92m\033[1mColors imported.\033[0m"


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
			print "\033[95m"
			pprint(set_data["name"])
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
	colors_query = "INSERT INTO 'colors' (name) VALUES ('White'), ('Black'), ('Blue'), ('Red'), ('Green');"
	db.execute(colors_query)
	print "\033[92m\033[1mColors imported.\033[0m"
	json_files = [
		pos_json for pos_json in os.listdir(path_to_json)
		if pos_json.endswith('.json')
	]
	for js in json_files:
		with open(os.path.join(path_to_json, js)) as json_file:
			set_data = json.load(json_file)
			set_data = format_set(set_data)
			print "\033[95m"
			pprint(set_data["name"])
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
				print "\033[94m"
				pprint(card_data)
				import_cards_query = 'INSERT INTO `cards` (layout, name, names, manaCost, cmc, colors, colorIdentity, type, supertypes, types, subtypes, rarity, text, flavor, artist, number, power, toughness, loyalty, multiverseid, variations, watermark, border, timeshifted, hand, life, reserved, releaseDate, starter, mciNumber, imageName, setId, setCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
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
			print "\033[92m\033[1mCards imported.\033[0m"


@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select * from cards order by multiverseid asc')
	cur_sets = db.execute(
		'select *, block from sets order by releaseDate desc')
	cards = cur.fetchall()
	sets = cur_sets.fetchall()
	return render_template('show_entries.html', cards=cards, sets=sets)


@app.route('/search')
def search():
	db = get_db()
	cur = db.execute(
		'select * from cards where colorIdentity="U" or colorIdentity="B" or colorIdentity="G" order by multiverseId asc limit 20'
	)
	cur_sets = db.execute(
		'select * from sets order by releaseDate desc limit 5')
	cards = cur.fetchall()
	sets = cur_sets.fetchall()
	return render_template('search.html', cards=cards, sets=sets)


@app.route('/card/<multiverseId>')
def card(multiverseId):
	db = get_db()
	cur = db.execute('select * from cards where multiverseId="' + multiverseId
					 + '"')
	card = cur.fetchall()
	card = card[0]
	cardNumber = card['number']
	flipCardA = False
	flipCardB = False
	if re.search('[a]', str(cardNumber)):
		flipCardA = True
	if re.search('[b]', str(cardNumber)):
		flipCardB = True
	cardMana = card['manaCost']
	cardMana = cardMana.replace('}{', ' ')
	cardMana = cardMana.replace('{', '')
	cardMana = cardMana.replace('}', '')
	cardText = card["text"]
	# Italicize Ability Words
	cardText = re.compile(
		r'(((battalion|bloodrush|channel|chroma|cohort|constellation|converge|council\'s dilemma|delirium|domain|fateful hour|ferocious|formidable|grandeur|hellbent|heroic|imprint|inspired|join forces|kinship|landfall|lieutenant|metalcraft|morbid|parley|radiance|raid|rally|spell mastery|strive|sweep|tempting offer|threshold|will of the council)\s*?)+)',
		re.I).sub(r'<em>\1</em>', cardText)

	# Code that doesn't work for making mana symbols lowercase
	# if re.search(r'{(.*)}', cardText):
	#   manaText = re.search(r'{(.*)}', cardText)
	#   manaText = manaText.group(0).lower()
	#   print manaText

	# Convert mana symbols to the styled span tags
	cardText = cardText.replace('{', '<span class="mana medium shadow s')
	cardText = cardText.replace('}', '">&nbsp;</span>')
	# Text on cards in parentheses is always italicized
	cardText = cardText.replace('(', '<em>(')
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


@app.route('/deck')
def deck():
	return render_template('deck.html')