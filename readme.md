
<p align="center">
<img src="https://raw.githubusercontent.com/CakeSphere/Decky/master/decky/static/images/favicon-2.png">
</p>

# Decky
### Decky lets users create, search, and view decks for Magic: The Gathering.

Decky is an application that makes it easy to build decks for the Magic: The Gathering card game. Search through all of the thousands of cards in the game to find the one that’s right for your deck, or look at decks other people around the world have created for inspiration.

### Current functionality is extremely limited:

**Deck Search**:
Decks are visible and formatted but it is not currently possible to search.

**Deck Details**:
Decks’ contents are visible but in progress. Prices are unavailable and many controls don’t work.

**Card Search**:
Cards are visible and formatted but it is not currently possible to search.

**Card Details**:
Cards contents are visible and properly formatted, but only cards from the past ten or so sets are available. Prices are unavailable and many controls don’t work.

**Deck Builder**:
Basic Deck Builder functionality exists but the finer details are in progress. This page
needs a redesign and Edit Deck functionality needs a lot of work.

**Glossary**:
The glossary is in the conceptual stage.

**Settings & User Profile**:
HTML and CSS exist for the Settings screen. This page still needs specific requirements. User Profile does not exist so far.

**Account Registration & Authorization**:
A sign-in page and dialog box exist. The full-page sign-in will probably not be used. Authorization, like User Profiles, does not exist in any form.


---

### To run Decky:

1. Ensure Flask is installed by following the instructions [here](http://flask.pocoo.org/docs/0.12/installation/).
2. Run `. venv/bin/activate` to activate the virtual environment.
3. Run `pip install -r requirements.txt` to install Decky’s dependencies.
4. Run `export FLASK_APP=decky` to set Decky as your Flask application.
5. *Optionally* run `export FLASK_DEBUG=true` to run the Flask debugger.
6. Run `flask run` to run the Decky app.
7. Navigate to `localhost:5000/decks` in your browser.

---

### To do:

- Use Scryfall images instead of Gatherer.
- Implement auth to allow things like My Grimoire to work.
- Indicate cards that are in a user's Grimoire with an icon.
- Implement help tooltip on Magic keywords and abilities.

###### These are next steps and not a comprehensive list of planned features and fixes. ######

---

###### Decky is not in any way associated with [Wizards of the Coast](http://wizards.com/).

###### Special thanks to [MTGJSON](http://mtgjson.com/), [Keyrune](https://andrewgioia.github.io/Keyrune/), and [Mana-Cost](https://github.com/micku/mana-cost).

<!--
```
______          _
|  _  \        | |
| | | |___  ___| | ___   _
| | | / _ \/ __| |/ / | | |
| |/ /  __/ (__|   <| |_| |
|___/ \___|\___|_|\_\\__, |v0.0.01a
                      __/ |
                     |___/
```
 -->
