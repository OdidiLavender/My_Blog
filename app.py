from flask import Flask,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


#Create a Flask Instance
app = Flask(__name__)

# Old SQLite DB
# Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

# New MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abc@localhost/our_users'





# Secret Key
app.config['SECRET_KEY'] = "LavenderKirigha"

# Initialized Database
db = SQLAlchemy(app)
# migrate = Migrate(app, db)




# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    favorite_color = db.Column(db.String(120))
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Do Some password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)



    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!!!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form,name=name,our_users=our_users)

    except:
        flash("An Error occured when deleting user!!")
        return render_template('add_user.html', form=form,name=name,our_users=our_users)



# Create a Form Class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField("Favourite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit  = SubmitField('submit')

# Update Database record
@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)

    if request.method == 'POST':

        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']


        try:
             db.session.commit()
             flash("User Updated Successfully!")
             return render_template("update.html", form=form,name_to_update=name_to_update)
        except:
                flash("Error! Problem Occured .....try again")
                return render_template("update.html", form=form,name_to_update=name_to_update)

    else:

        return render_template("update.html", form=form,name_to_update=name_to_update,id=id)

               






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
            #Hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data,favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
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


