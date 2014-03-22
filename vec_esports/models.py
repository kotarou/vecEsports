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
    member_1  = db.StringProperty()
    member_2  = db.StringProperty()
    member_3  = db.StringProperty()
    member_4  = db.StringProperty()
    member_5  = db.StringProperty()
    member_6  = db.StringProperty()
    contact_email = db.EmailProperty()
