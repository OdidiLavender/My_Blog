from flask import Flask,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#Create a Flask Instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'


# Secret Key
app.config['SECRET_KEY'] = "LavenderKirigha"

# Initialized Database
db = SQLAlchemy(app)




# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit  = SubmitField('submit')

# Update Database record
@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)

    if request.method == 'POST':

        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']

        try:
             db.session.commit()
             flash("User Updated Successfully!")
             return render_template("update.html", form=form,name_to_update=name_to_update)
        except:
                flash("Error! Problem Occured .....try again")
                return render_template("update.html", form=form,name_to_update=name_to_update)

    else:
        
        return render_template("update.html", form=form,name_to_update=name_to_update)

               






# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is you name?', validators=[DataRequired()])
    submit  = SubmitField('submit')




# def index():
#     return "<h1> Hello Bebe!!<h1>"

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!!")


    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form,name=name,our_users=our_users)

#Create a route decorator
@app.route('/')
def index():
    first_name = 'Lavender'
    return render_template ("index.html", first_name=first_name)

# localhost:5000/user/lavender
@app.route('/user/<name>')

def user(name):
    return render_template ("user.html", name=name)


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Successfully Submitted!!")
    return render_template("name.html", name=name, form=form)


