from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Set some App configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flasql'
app.config['FLASK_ENV'] = 'development'
app.config['FLASK_APP'] = 'api.py'

# Init a db
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(150))

  # posts = db.relationship('Post', backref='author', lazy=True)
  # ^ this line AUTO CREATES w/in Post class
  # author = db.relationship('User', backref='posts', lazy=True)
  posts = db.relationship('Post', lazy=True, back_populates='author')

  def as_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "bio": self.bio
    }

  def __repr__(self):
    return f'User(id={self.id}, email="{self.email}", name="{self.name}")'

post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  header = db.Column(db.String(150), unique=True, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
  body = db.Column(db.String, nullable=False)

  author = db.relationship('User', lazy=True, back_populates='posts')
  tags = db.relationship('Tag', secondary=post_tags, lazy='subquery', back_populates='posts')
  # tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
        # backref=db.backref('posts', lazy=True))

  def __repr__(self):
    return f'User(id={self.id}, email="{self.email}", display_name="{self.display_name}")'

class Tag(db.Model):
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(50), unique=True, nullable=False)

  posts = db.relationship('Post', secondary=post_tags, lazy=True, back_populates='tags')

  def __repr__(self):
    return f'Tag(id={self.id}, tag="{self.tag}")'