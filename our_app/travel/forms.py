from flask_wtf import FlaskForm, Form
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, FieldList, FormField, DecimalField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}



    
# creating a new event
class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    artists = FieldList(StringField("Artist", validators=[InputRequired()]), min_entries=1)
    tickets = FieldList(FormField(Ticket))
    submit = SubmitField("Submit")

class Ticket(Form):
    ticket_name = StringField("Ticket Name", validators=[InputRequired()])
    ticket_price = DecimalField("Ticket Price", validators=[InputRequired()])
    ticket_description = TextAreaField("Ticket Description", validators=[InputRequired()])

class EventTicketsForm(FlaskForm):
    tickets = FieldList(FormField(Ticket), min_entries=1)
    submit = SubmitField("Submit")
    

# Create new destination
class DestinationForm(FlaskForm):
    name = StringField('Country', validators=[InputRequired()])
    description = TextAreaField('Description')
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    currency = StringField('Currency', validators=[InputRequired()])
    submit = SubmitField("Create")

# User login


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User comment


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')
