"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


def serialize_cake(cake):
    """Return JSON {'desserts': [{id, name, calories}, ...]}"""
    return {
        'id': cake.id,
        'flavor': cake.flavor,
        'size': cake.size,
        'rating': cake.rating,
        'image': cake.image
    }


@app.route('/')
def index_page():
    """Renders html Homepage"""
    return render_template('index.html')


@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cake.serialize() for cake in Cupcake.query.all()]
    return jsonify(cake=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcat in particular"""
    cake = Cupcake.query.get_or_404(id)
    return jsonify(cake=cake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created todo"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cake = Cupcake.query.get_or_404(id)
    cake.flavor = request.json.get("flavor", cake.flavor)
    cake.size = request.json.get("size", cake.size)
    cake.rating = request.json.get("rating", cake.rating)
    cake.image = request.json.get("image", cake.image)

    db.session.commit()
    return jsonify(cake=cake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cake = Cupcake.query.get_or_404(id)
    db.session.delete(cake)
    db.session.commit()
    return jsonify(message="Deleted")
