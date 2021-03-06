import json
import secrets
from enum import Enum, unique

from flask import render_template, Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__, static_folder='html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@unique
class Errors(Enum):
    EMPTY_NAME = 'A name is required.'
    EMPTY_DESCRIPTION = 'A description is required.'
    EMPTY_NICK = 'A nick is required to create an attendee.'
    TOO_FEW_PROPOSALS = 'Too view proposals for provided.'
    UNKNOWN_PROPOSAL = 'Proposal does not exist'
    DUPLICATE_NICK = 'This nick name is already present at this event.'
    UNKNOWN = 'unknown'

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime(), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

def serialise_proposal(target):
    return {
        'id': target.id,
        'appointment': target.appointment.isoformat()+"Z"
    }

frees = db.Table('frees',
    db.Column('attendee_id', db.Integer, db.ForeignKey('attendee.id'), primary_key=True),
    db.Column('proposal_id', db.Integer, db.ForeignKey('proposal.id'), primary_key=True)
)

occupides = db.Table('occupides',
    db.Column('attendee_id', db.Integer, db.ForeignKey('attendee.id'), primary_key=True),
    db.Column('proposal_id', db.Integer, db.ForeignKey('proposal.id'), primary_key=True)
)

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(128), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    free = db.relationship('Proposal', lazy=False, secondary=frees)
    occupied = db.relationship('Proposal', lazy=False, secondary=occupides)

def serialise_attendee(target):
    return {
        'id': target.id,
        'nick': target.nick,
        'free': [p.id for p in target.free],
        'occupied': [p.id for p in target.occupied],
    }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(4), nullable=False, unique=True, index=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text())
    duration = db.Column(db.Integer, nullable=False)
    proposals = db.relationship('Proposal', lazy=False)
    attendees = db.relationship('Attendee', lazy=False)

def serialise_event(target):
    return {
        'key': target.key,
        'name': target.name,
        'description': target.description,
        'duration': target.duration,
        'proposals': [serialise_proposal(p) for p in target.proposals],
        'attendees': [serialise_attendee(a) for a in target.attendees],
    }

@app.route("/", methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route("/config.js", methods=['GET'])
def send_frontend_config():
    return app.send_static_file('config.js')

@app.route("/favicon.icon", methods=['GET'])
def send_frontend_favicon():
    return (200)

@app.route("/<event_id>", methods=['GET'])
def event(event_id):
    return app.send_static_file('index.html')

@app.route("/api/<event_key>", methods=['GET'])
def api_event(event_key):
    target_event = Event.query.filter_by(key=event_key)

    if target_event.count() == 0:
        return ('Unknown event', 404)

    return (json.dumps(serialise_event(target_event.first())), 200)


@app.route("/api/all", methods=['GET'])
def all():
    return jsonify([serialise_event(e) for e in Event.query.all()], 200)

@app.route("/api/<event_key>/attendee", methods=['POST'])
def create_attendee(event_key):
    params = request.get_json()

    target_event = Event.query.filter_by(key=event_key).first()

    if target_event is None:
        return (Errors.UNKNOWN_PROPOSAL.value, 400)

    if not 'nick' in params or len(params['nick']) < 1:
        return (Errors.EMPTY_NICK.value, 400)

    if any(Attendee.query.filter_by(nick=params['nick'], event_id=target_event.id)):
        return (Errors.DUPLICATE_NICK.value, 400)

    attendee = Attendee(nick=params['nick'], event_id=target_event.id)
    db.session.add(attendee)
    db.session.commit()
    return (json.dumps(serialise_attendee(attendee)), 201)

@app.route("/api/<event_id>/attendee/<attendee_id>", methods=['PUT'])
def update_attendee(event_id, attendee_id):
    params = request.get_json()

    a = Attendee.query.get(attendee_id)

    a.free.clear()
    for proposal_free in params['free']:
        free = Proposal.query.get(proposal_free)
        a.free.append(free)

    a.occupied.clear()
    for proposal_occupied in params['occupied']:
        occupied = Proposal.query.get(proposal_occupied)
        a.occupied.append(occupied)

    db.session.commit()
    return (json.dumps(serialise_attendee(a)), 200)


@app.route("/api/", methods=['POST'])
def create():
    params = request.get_json()

    if not 'name' in params or len(params['name']) == 0:
        return (Errors.EMPTY_NAME.value, 400)

    if not 'description' in params:
        return (Errors.EMPTY_DESCRIPTION.value, 400)

    if not 'proposals' in params or len(params['proposals']) < 2:
        return (Errors.TOO_FEW_PROPOSALS.value, 400)

    new_key = secrets.token_urlsafe(4)
    while Event.query.filter_by(key=new_key).count() > 0:
            new_key = secrets.token_urlsafe(4)

    e = Event(key=new_key,
              name=params['name'],
              description=params['description'],
              duration=86400)

    for proposed_date in params['proposals']:
        e.proposals.append(Proposal(appointment=datetime.strptime(proposed_date,
                                              "%Y-%m-%dT%H:%M:%S.%f%z")))

    if 'attendee' in params:
        for attendee in params['attendee']:
            e.attendees.append(Attendee(nick=attendee.nick))

    db.session.add(e)
    db.session.commit()

    return (json.dumps(serialise_event(e)), 200)

if __name__ == "__main__":
    app.run()
