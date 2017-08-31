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

#### Decky
###### Decky lets users create, search, and view decks for Magic: The Gathering.

Decky is an application that makes it easy to build decks for the Magic: The Gathering card game. Search through all of the thousands of cards in the game to find the one that's right for your deck, or look at decks other people around the world have created for inspiration.

##### Current functionality is extremely limited:

:white_square_button:  Deck Search: 
Decks are visible and formatted but it is not currently possible to search.

:white_square_button:  Deck Details: 
Decks' contents are visible but in progress. Prices are unavailable and many controls don't work.

:white_square_button:  Card Search: 
Cards are visible and formatted but it is not currently possible to search.

:white_square_button: Card Details: 
Cards contents are visible and properly formatted, but only cards from the past ten or so sets are available.

:white_square_button:  Deck Builder: 
The deck builder exists but is not currently functional.

:white_medium_square:  Glossary:
The glossary is in the conceptual stage.

:white_medium_square:  Settings & User Profile:
The settings menu is in the conceptual stage.

:white_medium_square:  Account Registration & Authorization: 
Some work has gone into mocking up this process, but it is not currently functional.


---

##### To run Decky:

1. Ensure Flask is installed by following the instructions [here](http://flask.pocoo.org/docs/0.12/installation/).
2. Run `. venv/bin/activate` to activate the virtual environment
3. Run `pip install -r requirements.txt` to install the required
4. Run `export FLASK_APP=decky` to set Decky as your Flask application
5. *Optionally* run `export FLASK_DEBUG=true` to run the Flask debugger
6. Run `flask run` to run the Decky app

---

Decky issues are tracked on [Trello](https://trello.com/b/eI9QlmUi/decky).

--- 

Decky is not in any way associated with 
[Wizards of the Coast](http://wizards.com/). 

Special thanks to 
[MTGJSON](http://mtgjson.com/), 
[Keyrune](https://andrewgioia.github.io/Keyrune/), and 
[Mana-Cost](https://github.com/micku/mana-cost).

---
