from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://blahblahblah'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    where = db.Column(db.String)
    comments = db.Column(db.Text())

    def __init__(self, name, email, where, comments):
        self.name = name
        self.email = email
        self.where = where
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        where = request.form['where']
        comments = request.form['comments']
        # print(name, email, where, comments)
        if name == '' or email == '':
            return render_template('index.html', message='Please enter fill out the form correctly')
        if db.session.query(Feedback).filter(Feedback.name == name).count() == 0:
            data = Feedback(name, email, where, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(name, email, where, comments)
            return render_template('success.html')
        return render_template('index.html', message="You've already submitted feedback silly")


if __name__ == '__main__':
    app.run()