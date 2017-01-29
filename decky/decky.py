import os, sqlite3, sass, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)
app.config.from_object(__name__)


app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'decky': ('static/sass', 'static/css', '/static/css')
})

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'decky.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

print app.root_path

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

def format_card(raw_card):
    out_card = {}
    fields = {"name", "manaCost", "cmc", "colors", "type", "supertypes", "types", "subtypes", "rarity", "text", "flavor", "artist", "number", "power", "toughness", "layout", "multiverseid", "imageName"}
    for field in fields:
        if field in raw_card:
            out_card[field] = raw_card[field]
            if isinstance(out_card[field], basestring):
                out_card[field] = out_card[field].replace('"', '\\')
        else:
            out_card[field] = None
    return out_card

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.cli.command('card_import')
def card_import():
    path_to_json = 'decky/static/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            set_data = json.load(json_file)
            db = get_db()
            import_sets_query = 'INSERT INTO `sets` (name, code, releaseDate, border, type, block) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(set_data["name"], set_data["code"], set_data["releaseDate"], set_data["border"], set_data["type"], set_data["block"])
            db.cursor().executescript(import_sets_query)
            for card in set_data["cards"]:
                card = format_card(card)
                import_cards_query = 'INSERT INTO `cards` (name, manaCost, cmc, colors, type, supertypes, types, subtypes, rarity, text, flavor, artist, number, power, toughness, layout, multiverseid, imageName) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(card["name"], card["manaCost"], card["cmc"], card["colors"], card["type"], card["supertypes"], card["types"], card["subtypes"], card["rarity"], card["text"], card["flavor"], card["artist"], card["number"], card["power"], card["toughness"], card["layout"], card["multiverseid"], card["imageName"])
                print import_cards_query
                db.cursor().executescript(import_cards_query)
            db.commit()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                  [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries'))

