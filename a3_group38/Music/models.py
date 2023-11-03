from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase



class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    booked_tickets = db.relationship('Booking', backref='user')

categories = db.Table('categorieslist',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200))
    status = db.Column(db.Integer)
    date = db.Column(db.String(200))
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    artists = db.relationship('Artist', backref='events')
    tickets = db.relationship('Ticket', backref='events')
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('categories', lazy=True))
    booked_tickets = db.relationship('Booking', backref='events')
    comments = db.relationship('Comment', backref='events')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200))


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(200))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class BookingTicket(db.Model):
    __tablename__ = 'bookingtickets'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer())
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(200))
    ticket_price = db.Column(db.Numeric(200))
    ticket_description = db.Column(db.String(400))
    ticket_quantity = db.Column(db.Numeric(200))
    #foreign keys 
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booked_tickets = db.relationship('BookingTicket', backref='tickets')


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booked_tickets = db.relationship('BookingTicket', backref='booking')



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='events')

    def __repr__(self):
        return f"Comment: {self.text}"