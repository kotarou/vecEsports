# As per any django project; a models file.

from google.appengine.ext import db

class Team(db.Model):
    """Models a Team entry with a captain, 4-6 other players, and contact details."""
    name      = db.StringProperty()
    game      = db.StringProperty()
    captain   = db.StringProperty()
    player_2  = db.StringProperty()
    player_3  = db.StringProperty()
    player_4  = db.StringProperty()
    player_5  = db.StringProperty()
    sub_1     = db.StringProperty()
    sub_2     = db.StringProperty()
    contact_email = db.EmailProperty()


class Matchup(db.Model):
    """Models a matchup between two teams. Match type is a string BO1 BO3 etc """
    team_1  = db.ReferenceProperty(Team, collection_name= "T1")
    team_2  = db.ReferenceProperty(Team, collection_name= "T2")
    game    = db.StringProperty()
    m_type  = db.StringProperty()
    m_class = db.StringProperty()
    date    = db.DateTimeProperty()
    m_id    = db.StringProperty()
    completed = db.BooleanProperty()

class Result(db.Model):
    """Models a matchup between two teams. Results are stored as integers showing each teams number of wins in the match """
    match  = db.ReferenceProperty(Matchup, collection_name= "m")
    score_1 = db.StringProperty()
    score_2 = db.StringProperty()

class Player(db.Model):
    """Models a Player entry with a player name, alias, contact details"""
    first_name = db.StringProperty()
    last_name  = db.StringProperty()
    email      = db.EmailProperty()
    alias      = db.StringProperty()
