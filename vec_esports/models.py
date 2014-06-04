# As per any django project; a models file.

from google.appengine.ext import db

class Tournament(db.Model):
    """Models a tournament with a name, game, a dict of entered teams and their standings, and a dict of matches and their winners"""
    name        = db.StringProperty()
    game        = db.StringProperty(choices=set(["lol", "dota"]))
    completed   = db.BooleanProperty()

class Player(db.Model):
    """Models a Player entry with a player name, alias, contact details"""
    first_name = db.StringProperty()
    last_name  = db.StringProperty()
    email      = db.EmailProperty()
    alias      = db.StringProperty()

class Team(db.Model):
    """Models a Team entry with a captain, 4-6 other players, and contact details. Each team has a dict of entered tournaments and their results thereof."""
    name      = db.StringProperty()
    game      = db.StringProperty(choices=set(["lol", "dota"]))
    captain   = db.StringProperty()
    player_2  = db.StringProperty()
    player_3  = db.StringProperty()
    player_4  = db.StringProperty()
    player_5  = db.StringProperty()
    sub_1     = db.StringProperty()
    sub_2     = db.StringProperty()
    contact_email = db.EmailProperty()
    results = db.StringProperty(multiline=True)

class Matchup(db.Model):
    """Models a matchup between two teams. Match type is a string BO1 BO3 etc. Match class is roundrobin / final / etc """
    team_1  = db.ReferenceProperty(Team, collection_name= "T2")
    team_2  = db.ReferenceProperty(Team, collection_name= "T3")
    game    = db.StringProperty(choices=set(["lol", "dota"]))
    m_type  = db.StringProperty()
    m_class = db.StringProperty()
    date    = db.DateTimeProperty()
    m_id    = db.StringProperty()
    completed = db.BooleanProperty()
    score_1 = db.IntegerProperty()
    score_2 = db.IntegerProperty()
    tournament = db.StringProperty()
    #tournament = db.ReferenceProperty(Tournament, collection_name= "T4")



