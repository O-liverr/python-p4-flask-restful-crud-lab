from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return make_response(jsonify(plant.to_dict()), 200)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid request body"}), 400)

        # Update fields if provided in the request body
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
        if 'name' in data:
            plant.name = data['name']
        if 'image' in data:
            plant.image = data['image']
        if 'price' in data:
            plant.price = data['price']

        db.session.commit()
        return make_response(jsonify(plant.to_dict()), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__== '_main_':
    app.run(port=5555, debug=True)