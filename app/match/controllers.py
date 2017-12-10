from flask import Blueprint, render_template
from app import db, requires_auth , session
from .models import Match
from app.user.models import User
from sqlalchemy import or_

mod_match = Blueprint('match', __name__)


@mod_match.route('/Match/<id>', methods=['GET'])
@requires_auth
def matchmake(id):
    user_id = session['user_id']
    if int(id) != user_id :
        return render_template('error.html', message="You are not authorised to access this page")

    matches = Match.query.filter(or_(Match.user1 == int(id), Match.user2 == int(id))).all()
    arr = []
    for match in matches:
        match = match.to_dict()
        if match['user1'] == int(id):
            user = User.query.filter(User.id == match['user2']).first()
            user = user.to_dict()
            arr.append(user)
        else:
            user = User.query.filter(User.id == match['user1']).first()
            user = user.to_dict()
            arr.append(user)

    return render_template('match.html', users=arr)