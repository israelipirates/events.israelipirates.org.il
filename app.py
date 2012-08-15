import os

from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://a:b@c:d/e'
db = SQLAlchemy(app)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/reg', methods=['POST'])
def reg():
    error = False
    name = request.form['name']
    email = request.form['email']

    if name and email:
        try:
            registration = Registration(name, email)
            db.session.add(registration)
            db.session.commit()
        except:
            error = 'dupe'
    else:
        error = 'blank'

    return render_template('thx.html', error=error)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
