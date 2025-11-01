import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')              # this __name__ thing is actually for telling flask which file it is defined in
                                                                        # the url-prefix will be prepended to all urls associated with the bp

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':                                        # request is the global object holding all the info about current request from the user
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = 'User already exists.'
            else:
                return redirect(url_for('auth.login')) # finds url by first looking for the function named login # if no errors load login page

        flash(error)                                                                                    # adds message t flash stack # can make it display red error message
    return render_template('auth/register.html') # if there is an error load same page but with flash   # sends html to the browser

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()              # returns one row from the query If the query returned no results, it returns None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):          # hashes the submitted password in the same way as the stored hash and securely compares them
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']                                 # stored in browser cookies so on the next page it will load the same user on the same browser
            return redirect(url_for('index'))                               # if no issues load main page but as a logged in user

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():                              # so before any view is run we always have the current user
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()                                                        # stores active user in g.user remember it is type of sqliteRow


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))                      # if the g.user is None redirect to login page

        return view(**kwargs)                                           # otherwise proceed to normal function execution

    return wrapped_view