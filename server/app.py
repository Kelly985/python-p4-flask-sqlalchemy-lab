#!/usr/bin/env python3

from flask import Flask, make_response, jsonify

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    response = {
        'name': animal.name,
        'species': animal.species,
        'zookeeper': animal.zookeeper.name if animal.zookeeper else None,
        'enclosure': animal.enclosure.environment if animal.enclosure else None
    }
    return make_response(jsonify(response), 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    response = {
        'name': zookeeper.name,
        'birthday': zookeeper.birthday.strftime('%Y-%m-%d'),
        'animals': [animal.name for animal in zookeeper.animals]
    }
    return make_response(jsonify(response), 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    response = {
        'environment': enclosure.environment,
        'open_to_visitors': enclosure.open_to_visitors,
        'animals': [animal.name for animal in enclosure.animals]
    }
    return make_response(jsonify(response), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
