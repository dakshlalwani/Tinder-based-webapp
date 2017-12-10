from app import db
from app.user.models import User


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1 = db.Column(db.Integer, db.ForeignKey(User.id))
    user2 = db.Column(db.Integer, db.ForeignKey(User.id))
    status = db.Column(db.Boolean, default=False)

    def __init__(self, user1, user2, status):
        self.user1 = user1
        self.user2 = user2
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'user1': self.user1,
            'user2': self.user2,
            'status': self.status
        }

