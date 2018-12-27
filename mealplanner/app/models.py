from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import logging
logger = logging.getLogger(__name__)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    notes = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<User {self.date}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def update(_date, _title="", _ingredients="", _url="", _notes=""):
    """Pass a date and whatever we would like to change"""
    post = Post.query.filter_by(date=_date).first()
    logging.info(f'Updating DB for post with date: {_date}')
    # Grab an existing post
    if post:
        post.title = _title
        post.ingredients = _ingredients
        post.url = _url
        post.notes = _notes
    else:
        # No existing post.  Let's create one.
        db.session.add(Post(date=_date, title=_title, ingredients=_ingredients, url=_url, notes=_notes))
    db.session.commit()
