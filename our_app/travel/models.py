from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase



class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')








categories = db.Table('categorieslist',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200))
    date = db.Column(db.String(200))
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    artists = db.relationship('Artist', backref='events')
    tickets = db.relationship('Ticket', backref='events')
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('categories', lazy=True))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200))

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(200))
    #foreign keys 
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(200))
    ticket_price = db.Column(db.Numeric(200))
    ticket_description = db.Column(db.String(400))
    ticket_quantity = db.Column(db.Numeric(200))
    #foreign keys 
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')
	
    def __repr__(self): #string print method
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    def __repr__(self):
        return f"Comment: {self.text}"