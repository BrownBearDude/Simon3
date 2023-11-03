from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Event, Artist, Ticket, Category, Booking, BookingTicket, Comment
from . import db
import os
from .forms import EventForm, CategoriesForm, BookingForm, CommentForm, Explore
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import sys
from datetime import datetime



destbp = Blueprint('events', __name__, url_prefix='/events')




@destbp.route('/explore', methods=['GET', 'POST'])
def explore():
    categories = db.session.scalars(db.select(Category)).all()
    form = Explore()
    form.categories.choices = [(g.id, g.category_name) for g in categories]
        
    

    events = db.session.scalars(db.select(Event)).all()
    if request.method == 'POST' and form.is_submitted():
        def myFunc(event):
            return any((True for x in list(e.id for e in event.categories) if x in form.categories.data))
        events = filter(myFunc, events)
    return render_template('events/explore.html', events=events, form=form)


@destbp.route('/mine', methods=['GET', 'POST'])
@login_required
def mine():
    events = db.session.scalars(db.select(Event).where(Event.user_id == current_user.id))
    return render_template('events/mine.html', events=events)

@destbp.route('/booked/<id>', methods=['GET', 'POST'])
@login_required
def bookedshow(id):
    booking = db.session.scalar(db.select(Booking).where(Booking.id==id))
    booked_tickets = db.session.scalars(db.select(BookingTicket).filter(BookingTicket.id == booking.id)).all()
    return render_template('events/bookedshow.html', booking=booking, booked_tickets=booked_tickets)


@destbp.route('/booked', methods=['GET', 'POST'])
@login_required
def booked():
    bookings = db.session.scalars(db.select(Booking)).all()
    return render_template('events/booked.html', bookings=bookings)


@destbp.route('/<id>/book', methods=['GET', 'POST'])
@login_required
def book(id):
    form = BookingForm()
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    
    if request.method == 'POST' and form.is_submitted():
        if all(i >= 0 for i in form.tickets.data):
            if any(i > 0 for i in form.tickets.data):
                booking = Booking(
                    user = current_user,
                    event_id = event.id
                )
                for pack in zip(event.tickets, form.tickets):
                    if pack[1].data > 0:
                        bookingticket = BookingTicket(
                            ticket_id = pack[0].id,
                            quantity = pack[1].data
                        )
                        booking.booked_tickets.append(bookingticket)
                db.session.add(booking)
                db.session.commit()
        return redirect(url_for('events.booked'))
                
    
    for ticket in event.tickets:
        form.tickets.append_entry()
    form.tickets.min_entries = len(event.tickets)
    return render_template('events/booking.html', event=event, packed=zip(event.tickets, form.tickets), form=form)


@destbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    min_ticket_price = min(event.tickets, key=lambda x: x.ticket_price).ticket_price

    if (datetime.strptime(event.date, "%Y-%m-%d").date() < datetime.now().date()):
        event.status = 4

    commentform = CommentForm()

    return render_template('events/show.html', event=event, min_ticket_price=min_ticket_price, id=id, commentform=commentform)



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
@login_required
def create():
    
    categories = db.session.scalars(db.select(Category)).all()
    form = EventForm()
    form.categories.choices = [(g.id, g.category_name) for g in categories]
    form.event_status.choices = [(0, "Open"), (1, "Inactive"), (3, "Sold Out"), (4, "Cancelled")]

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
            user = current_user,
            status = form.event_status.data
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
        return redirect(url_for('events.mine'))
    

    return render_template('events/eventcreation.html', form=form)

@destbp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    


    
    categories = db.session.scalars(db.select(Category)).all()
    form = EventForm()
    form.categories.choices = [(g.id, g.category_name) for g in categories]
    form.event_status.choices = [(0, "Open"), (1, "Inactive"), (3, "Sold Out"), (4, "Cancelled")]

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
        event = db.session.scalar(db.select(Event).where(Event.id == id))

        
        event.event_name=form.event_name.data
        event.date=form.date.data
        event.description=form.description.data
        event.image = form.imagePath.data
        event.user = current_user
        event.status = form.event_status.data
        
        for artist in event.artists:
            db.session.delete(artist)
        event.artists = []
        for artist in form.artists:
            a = Artist(artist_name = artist.data)
            event.artists.append(a)
        for ticket in event.tickets:
            db.session.delete(ticket)
        event.tickets = []
        for ticket in form.tickets:
            t = Ticket(
                ticket_name = ticket.ticket_name.data,
                ticket_price = ticket.ticket_price.data,
                ticket_description = ticket.ticket_description.data,
                ticket_quantity = ticket.ticket_quantity.data
            )
            event.tickets.append(t)
        event.categories = []
        for category in form.categories.data:
            category_object = db.session.scalar(db.select(Category).where(Category.id==category))
            event.categories.append(category_object)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events.mine'))
    else:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
        form.event_name.data = event.event_name
        form.date.data = datetime.strptime(event.date, "%Y-%m-%d").date()
        form.event_status.data = event.status
        form.categories.data = [o.id for o in event.categories]
        form.description.data = event.description
        form.imagePath.data = event.image
        
        artists = db.session.scalars(db.select(Artist).where(Artist.event_id == id))
        form.artists.pop_entry()
        for artist in artists:
            form.artists.append_entry(artist.artist_name)
        tickets = db.session.scalars(db.select(Ticket).where(Ticket.event_id == id))
        form.tickets.pop_entry()
        for ticket in tickets:
            form.tickets.append_entry(ticket)
        
    return render_template('events/eventcreation.html', form=form)


def check_upload_file(form): 
  fp = form.image.data
  filename = fp.filename 
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  db_upload_path = '/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path


@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('events.show', id=id))