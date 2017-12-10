from flask import Blueprint, request
from app import db , requires_auth
from .models import Like
from app.match.models import Match
from sqlalchemy import and_ , or_

mod_like = Blueprint('like', __name__)


@mod_like.route('/like',methods=['POST'])
@requires_auth
def like():
    user1 = request.form['id1']
    user2 = request.form['id2']
    l = Like(user1 , user2 , True)
    x = Like.query.filter( and_( Like.user1 == user1 , Like.user2 == user2) ).first()
    if x == None :
        db.session.add(l)
        db.session.commit()
    else:
        x.status = True
        db.session.commit()
    return 'Liked!!'

@mod_like.route('/unlike',methods=['POST'])
@requires_auth
def unlike():
    user1 = request.form['id1']
    user2 = request.form['id2']
    l = Like(user1 , user2 , False)
    x = Like.query.filter(and_(Like.user1 == user1, Like.user2 == user2)).first()
    if x == None:
        db.session.add(l)
        db.session.commit()
    else:
        x.status = False
        db.session.commit()
    return 'Unliked!!'

@mod_like.route('/match',methods=['POST'])
@requires_auth
def match():
    user1 = request.form['id1']
    user2 = request.form['id2']
    x = Like.query.filter(and_(Like.user1 == user1, Like.user2 == user2)).first()
    y = Like.query.filter(and_(Like.user1 == user2, Like.user2 == user1)).first()
    z1 = Match.query.filter(and_(Match.user1 == user2 , Match.user2 == user1)).first()
    z2 = Match.query.filter(and_(Match.user1 == user1, Match.user2 == user2)).first()
    if y != None and x != None:
        if x.status == True and y.status == True:
            if z1 == None and z2 == None:
                m = Match(user1 , user2)
                db.session.add(m)
                db.session.commit()
                return 'match found!!'
            return "match already exists!!"
    return 'no match!!'