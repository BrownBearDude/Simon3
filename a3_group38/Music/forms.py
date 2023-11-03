from flask_wtf import FlaskForm, Form
from wtforms import widgets
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, FieldList, FormField, DecimalField, HiddenField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class Explore(FlaskForm):
    categories = MultiCheckboxField("Categories", coerce=int)
    submitsubmit = SubmitField("Search")

class Ticket(Form):
    ticket_name = StringField("Ticket Name", validators=[InputRequired()])
    ticket_price = DecimalField("Ticket Price", validators=[InputRequired()])
    ticket_description = TextAreaField("Ticket Description", validators=[InputRequired()])
    ticket_quantity = IntegerField("Ticket Quantity", validators=[InputRequired()])
    
# creating a new event
class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    event_status = SelectField("Event Status")
    categories = MultiCheckboxField("Categories", coerce=int)
    description = TextAreaField("Description", validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    imagePath = HiddenField()
    addArtist = SubmitField("AddArtist")
    subArtist = SubmitField("SubArtist")
    artists = FieldList(StringField("Artist", validators=[InputRequired()]), min_entries=1)
    addTicket = SubmitField("AddTicket")
    subTicket = SubmitField("SubTicket")
    tickets = FieldList(FormField(Ticket), min_entries=1)
    #couldn't be named just submit for some reason, i forgor. but it breaks if its just submit
    submitsubmit = SubmitField("Submit")

class CategoriesForm(FlaskForm):
    name =  StringField("Event Name", validators=[InputRequired()])
    submitsubmit = SubmitField("Submit")

class BookingForm(FlaskForm):
    tickets = FieldList(IntegerField("amount", default=0, validators=[InputRequired("0 or a +ve number")]))
    submit = SubmitField("Check Out")

#login for user
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# registration for user
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])

    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# comment from user 
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')
