from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200))
    date = db.Column(db.String(200))
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    artists = db.relationship('Artist', backref='events')
    tickets = db.relationship('Ticket', backref='events')
    comments = db.relationship('Comment', backref='events')

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(200))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(200))
    ticket_price = db.Column(db.Numeric(200))
    ticket_description = db.Column(db.String(400))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"