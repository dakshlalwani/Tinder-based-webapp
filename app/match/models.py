from app import db
from app.user.models import User


class Match(db.Model):
    __tablename__ = 'match'
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1 = db.Column(db.Integer, db.ForeignKey(User.id))
    user2 = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2

    def to_dict(self):
        return{
            'match_id' : self.match_id,
            'user1' : self.user1,
            'user2' : self.user2
        }