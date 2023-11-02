from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Event, Artist, Ticket, Category
from . import db
import os
from .forms import EventForm, CategoriesForm
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


#page which should not be accessible to users to add or remove ccategory options
@destbp.route('/admin/categories', methods=['GET', 'POST'])
def categories():
    form = CategoriesForm()
   
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(
            category_name = form.name.data
        )
        db.session.add(category)
        db.session.commit()
    categories = db.session.scalars(db.select(Category)).all()
    return render_template('admin/categories.html', categories=categories, form=form)


@destbp.route('/create', methods=['GET', 'POST'])
def create():
    categories = db.session.scalars(db.select(Category)).all()
    form = EventForm()
    form.categories.choices = [(g.id, g.category_name) for g in categories]
    form.event_status.choices = [(0, "Open"), (1, "Inactive"), (3, "Sold Out"), (4, "Cancelled")]
    
    print(form.categories.data, file=sys.stderr)

    if form.image.data:
        form.imagePath.data = check_upload_file(form)


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
                ticket_description = ticket.ticket_description.data,
                ticket_quantity = ticket.ticket_quantity.data
            )
            event.tickets.append(t)
        for category in form.categories.data:
            category_object = db.session.scalar(db.select(Category).where(Category.id==category))
            event.categories.append(category_object)
        db.session.add(event)
        db.session.commit()

    

    return render_template('events/eventcreation.html', form=form)


def check_upload_file(form): 
  fp = form.image.data
  filename = fp.filename 
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  db_upload_path = '/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path