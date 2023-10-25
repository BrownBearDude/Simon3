from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Event, Artist, Ticket
from . import db
import os
from .forms import EventForm
from werkzeug.utils import secure_filename
import sys

destbp = Blueprint('events', __name__, url_prefix='/events')

@destbp.route('/<id>/book', methods=['GET', 'POST'])
def book(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    return render_template('events/booking.html', event=event)

@destbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    min_ticket_price = min(event.tickets, key=lambda x: x.ticket_price).ticket_price

    return render_template('events/show.html', event=event, min_ticket_price=min_ticket_price, id=id)

@destbp.route('/all', methods=['GET', 'POST'])
def all():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('events/all.html', events=events)


@destbp.route('/create', methods=['GET', 'POST'])
def create():
    form = EventForm()
    
    if form.image.data:
        form.imagePath.data = check_upload_file(form)
        print(form.image.data, sys.stderr)


    if form.addArtist.data:
        form.artists.append_entry()
    elif form.subArtist.data:
        form.artists.pop_entry()
    elif form.addTicket.data:
        form.tickets.append_entry()
    elif form.subTicket.data:
        form.tickets.pop_entry()
    elif form.submitsubmit.data and request.method == 'POST' and form.validate_on_submit():
        event = Event(
            event_name=form.event_name.data,
            date=form.date.data,
            description=form.description.data,
            image = form.imagePath.data,
        )
        for artist in form.artists:
            a = Artist(artist_name = artist.data)
            event.artists.append(a)
        for ticket in form.tickets:
            t = Ticket(
                ticket_name = ticket.ticket_name.data,
                ticket_price = ticket.ticket_price.data,
                ticket_description = ticket.ticket_description.data
            )
            event.tickets.append(t)
            db.session.add(event)
        db.session.commit()

    

    return render_template('events/eventcreation.html', form=form)




# 




def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path