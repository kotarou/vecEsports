# As per any django project; a models file.

from google.appengine.ext import db
import pickle

class DictProperty(db.Property):
  data_type = dict

  def get_value_for_datastore(self, model_instance):
    value = super(DictProperty, self).get_value_for_datastore(model_instance)
    return db.Blob(pickle.dumps(value))

  def make_value_from_datastore(self, value):
    if value is None:
      return dict()
    return pickle.loads(value)

  def default_value(self):
    if self.default is None:
      return dict()
    else:
      return super(DictProperty, self).default_value().copy()

  def validate(self, value):
    if not isinstance(value, dict):
      raise db.BadValueError('Property %s needs to be convertible '
                         'to a dict instance (%s) of class dict' % (self.name, value))
    return super(DictProperty, self).validate(value)

  def empty(self, value):
    return value is None


class Tournament(db.Model):
    """Models a tournament with a name, game, a dict of entered teams and their standings, and a dict of matches and their winners"""
    name        = db.StringProperty()
    game        = db.StringProperty(choices=set(["lol", "dota"]))
    teams       = DictProperty()
    matches     = DictProperty()
    completed   =  db.BooleanProperty()

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
    paid = db.BooleanProperty()
    tournaments = DictProperty()

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



