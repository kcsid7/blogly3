"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connecting SQLAlchemy to our Flask App"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class Post(db.Model):
    """ Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column( db.Integer, db.ForeignKey('users.id'), nullable=False,)



class Tag(db.Model):
    """ Tags Model """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary = "poststags", backref="tags")


class PostsTag(db.Model):
    """ Connection between the posts and tags """

    __tablename__ = "poststags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key = True)
