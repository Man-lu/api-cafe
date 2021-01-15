from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///cafes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mm = Marshmallow(app)


class Cafes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True,nullable=False)
    location = db.Column(db.String(50), unique=False, nullable=False)
    map_url = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)
    has_sockets = db.Column(db.Boolean(), unique=False, nullable=False)
    has_wifi = db.Column(db.Boolean(), unique=False, nullable=False)
    seats = db.Column(db.Integer, unique=False,nullable=False)
    coffee_price= db.Column(db.Float(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Cafes {self.name}'

db.create_all()
class CafeSchema(mm.Schema):
    class Meta:
        fields = ('id', 'name','location', 'map_url', 'img_url', 'has_sockets', 'has_wifi', 'seats', 'coffee_price')


cafe_schema = CafeSchema()
cafes_schema = CafeSchema(many=True)


# POST CAFE: api/cafes
@app.route("/api/cafes", methods=['POST'])
def add_cafe():
    name = request.json['name']
    location = request.json['location']
    map_url = request.json['map_url']
    img_url = request.json['img_url']
    has_sockets = request.json['has_sockets']
    has_wifi = request.json['has_wifi']
    seats = request.json['seats']
    coffee_price = request.json['coffee_price']

    new_cafe = Cafes(name=name.title(),location=location.title(),map_url=map_url,img_url=img_url,has_sockets=has_sockets,
                     has_wifi=has_wifi,seats=seats,coffee_price=coffee_price)
    db.session.add(new_cafe)
    db.session.commit()
    return cafe_schema.jsonify(new_cafe)


# GET ALL: api/cafes
@app.route("/api/cafes", methods =['GET'])
def get_all_cafes():
    all_cafes = db.session.query(Cafes).all()
    return cafes_schema.jsonify(all_cafes)


#GET ONE: api/cafe/id
@app.route("/api/cafes/<cafe_id>", methods =['GET'])
def get_cafe(cafe_id):
    cafe = Cafes.query.get(cafe_id)
    return cafe_schema.jsonify(cafe)


# PUT CAFE: api/cafe/id
@app.route("/api/cafes/<cafe_id>", methods=['PUT'])
def edit_cafe(cafe_id):
    edited_cafe = Cafes.query.get(cafe_id)
    edited_cafe.name = request.json['name'].title()
    edited_cafe.location = request.json['location'].title()
    edited_cafe.map_url = request.json['map_url']
    edited_cafe.img_url = request.json['img_url']
    edited_cafe.has_sockets = request.json['has_sockets']
    edited_cafe.has_wifi = request.json['has_wifi']
    edited_cafe.seats = request.json['seats']
    edited_cafe.coffee_price = request.json['coffee_price']

    db.session.add(edited_cafe)
    db.session.commit()
    return cafe_schema.jsonify(edited_cafe)


# DELETE CAFE: api/cafe/id
@app.route("/api/cafes/<cafe_id>", methods =['DELETE'])
def delete_cafe(cafe_id):
    cafe = Cafes.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return {"message":"Cafe Deleted"}


# SEARCH CAFE: api/search?location
@app.route("/api/cafes/search")
def search_cafe():
    requested_location = request.args.get('loc')
    cafes = db.session.query(Cafes).filter_by(location=requested_location.title()).all()
    if cafes:
        return cafes_schema.jsonify(cafes)
    else:
        return {"error": {"Not Found": "Sorry, we don't have a cafe at that location."}}


if __name__ == "__main__":
    app.run()
