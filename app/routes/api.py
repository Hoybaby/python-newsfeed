from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# we add a new route that will resole to /api/users and specified the method to be POST
# purpose of a POST route is to receive data but then using, request from flask to retrieve it
@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()

    # this data that we are getting is returning an object which we will pass into a new User model.

    # create a new user

    try:
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # saving into the database
        db.add(newUser)
        db.commit()
    except:

        print(sys.exc_info()[0])

        # the db.rollback() is for if the db.comit fails, the connection will stay in a pending state which will break us in production with this.
        db.rollback()
        
        return jsonify(message = 'Sign up failed'), 500

    # print(data)

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True
    # This clears any existing session data and creates two new session properties: a user_id to aid future database queries and a Boolean property that the templates will use to conditionally render elements.
    return jsonify(id = newUser.id)

@bp.route('/users/logout/', methods=['POST'])
def logout():
    # remove session variables so user can logout
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email ==data['email']).one()

    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400

    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400

        #  the data['password] is second because the first parameter is for self if we remember correctly.
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)

# ROUTE FOR COMMENTS. very similar to the login route we made on line 11

@bp.route('/comments', methods=['POST'])
def comment():
    data = request.get_json()
    db = get_db()
    # this part takes care of connecting to the database
    try:
    # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )
        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify(message = 'Comment failed'), 500
        
    return jsonify(id = newComment.id)