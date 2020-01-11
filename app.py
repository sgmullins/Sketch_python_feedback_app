import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SKETCHUP_DB_CONNECTION')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SKETCHUP_HEROKU_DB_CONNECTION')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100), unique=True)
    product = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, product, rating, comments):
        self.customer = customer
        self.product = product
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        product = request.form['product']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, product, rating, comments)
        if customer == "" or product == "":
            return render_template('index.html', message="Please enter required fields")
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, product, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, product, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="Your feedback on this product has already been submitted")


if __name__ == '__main__':
    app.run()
