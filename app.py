import os

from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    org = db.Column(db.String(80))
    updates = db.Column(db.Boolean())

    def __init__(self, name, email, org, updates):
        self.name = name
        self.email = email
        self.org = org
        self.updates = updates

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/reg', methods=['POST'])
def reg():
    error = False
    name = request.form.get('name')
    email = request.form.get('email')
    org = request.form.get('org', '')
    updates = request.form.get('updates') == 'yes'

    if name and email:
        try:
            registration = Registration(name, email, org, updates)
            db.session.add(registration)
            db.session.commit()
        except:
            error = 'dupe'
    else:
        error = 'blank'

    return render_template('thx.html', error=error)


@app.route('/reg/l1st')
def reg_list():
    regs = Registration.query.all()
    return render_template('list.html', regs=regs)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
