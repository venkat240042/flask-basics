from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#instance the Class (Flask)
app=Flask(__name__)

#Python enviornment configuraiton

app.config.update(

    SECRECT_KEY ='chaitra4me', # secure our data transfer (we have to define this key)
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:chaitra4me@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

#instance of class SQLAlchemy to let flask knows about database
db = SQLAlchemy(app)


#define the route
@app.route('/index')
@app.route('/')

#write function/method

def hello_flask():
    return "Hello Flask!!"

@app.route('/new/')
def query_string(greeting='hello'):
    query_val=request.args.get('greeting', greeting)
    return '<h1> The greeting is : {0} <h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>') #name is a variable and use <> brackets for variables

def no_query_string(name='ninja'):
    return '<h1> hello there ! {} <h1>'.format(name)

#STRING
@app.route('/text/<string:name>')

def working_with_strings(name):
    return '<h1> Here is the string: ' + name + '<h1>'

#Numbers

@app.route('/numbers/<int:num>')

def working_with_numbers(num):
    return '<h1> The number you picked is: ' + str(num) + '<h1>'

#Numbers

@app.route('/numbers/<int:num1>/<int:num2>')

def adding_two_numbers(num1,num2):
    return '<h1> the sum is : {}'.format(num1 + num2) + '<h1>'

#USING Templates (rendering )

@app.route('/temp')

def using_template():
    return render_template('hello.html')

#JINJA Templates

@app.route('/watch')

def top_movies():
    movie_list=['Spiderman:2','ninja','varsham','guru']
    return render_template('movies.html',movies=movie_list,name='Harry')

# Tables
@app.route('/tables')
def movie_plus():
    movie_dict={'spidername':2,
                'nion demo': 3.20,
                'john wick 2': 02.32}
    return render_template('table_data.html',movies=movie_dict,name='Salay')

# Jinja2 Filters
@app.route('/filters')
def filter_data():
    movie_dict={'spidername':2,
                'nion demo': 3.20,
                'john wick 2': 02.32}
    return render_template('filter_data.html',movies=movie_dict,name=None,film='a christmas carol')

#Creating a database tables using python classes

# PUBLICATION TABLE
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Name is is {}'.format(self.name)


# BOOK TABLE
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH A RELATIONSHIP BETWEEN PUBLICATION AND BOOK TABLES
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()   # to create a tables, we don't have to add this line in case tables has already been created p
    app.run(debug=True)
