from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_ALCHEMY'] = False

db = SQLAlchemy(app)

class History(db.Model):
	id = db.Column('id',db.Integer,primary_key = True)
	message = db.Column('message',db.String(500))

	def __init__(self, message):
		self.message = message

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	message = History(message=msg)
	db.session.add(message)
	db.session.commit()
	send(msg, broadcast=True)

@app.route('/')
def index():
	messages = History.query.all()
	return render_template('index.html',messages = messages)

if __name__ == '__main__':
	socketio.run(app)