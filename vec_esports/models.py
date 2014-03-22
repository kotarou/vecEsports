# As per any django project; a models file.

from google.appengine.ext import db

class Greeting(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_key_from_name(cls, guestbook_name=None):
        return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

class Team(db.Model):
    """Models a Team entry with a captain, 4-6 other players, and contact details."""
    name      = db.StringProperty()
    captain   = db.StringProperty()
    player_2  = db.StringProperty()
    player_3  = db.StringProperty()
    player_4  = db.StringProperty()
    player_5  = db.StringProperty()
    player_6  = db.StringProperty()
    player_7  = db.StringProperty()
    contact_email = db.EmailProperty()

class Matchup(db.Model):
    """Models a matchup between two teams """
    team_1 = db.ReferenceProperty(Team, collection_name= "T1")
    team_2 = db.ReferenceProperty(Team, collection_name= "T2")
    date   = db.DateProperty()


class Player(db.Model):
    """Models a Player entry with a player name, alias, contact details"""
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    alias = db.StringProperty()
