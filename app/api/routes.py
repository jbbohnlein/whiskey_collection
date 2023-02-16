from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

# practice
# @api.route('/getdata')
# def getdata():
#     return {'Whiskey': 'Yes'}

# Create a new whiskey
@api.route('/shelf', methods = ['POST'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def create_whiskey(current_user_token):
    name = request.json['name']     # json works in key-value pairs, so we're setting the value of 'name' = name
    distiller = request.json['distiller']
    type = request.json['type']
    country = request.json['country']
    user_token = current_user_token.token  

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(name, distiller, type, country, user_token = user_token )  # Contact() comes from models.py. Looks similar but the ID will get written for us
                                                            # ^ This overwrites the default from the Contact() class 
    db.session.add(whiskey)    # adding / staging it to the database
    db.session.commit()         # committing it to the database

    response = contact_schema.dump(whiskey)    # contact_schema is also from models.py which instantiates a class (we didn't write this but brought it in from marshmallow)
    return jsonify(response)

# Delete a whiskey from the shelf
@api.route('/shelf/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = contact_schema.dump(whiskey)
    return jsonify(response)

# Return the whole shelf
@api.route('/shelf', methods = ['GET'])
@token_required
def get_shelf(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user).all()  # This brings back all the contacts in our database
    response = contacts_schema.dump(whiskeys)
    return jsonify(response)

# Return a single whiskey using its ID
@api.route('/shelf/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = contact_schema.dump(whiskey)
    return jsonify(response)

#Update a Whiskey
@api.route('shelf/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.name = request.json['name']     # json works in key-value pairs, so we're setting the value of 'name' = name
    whiskey.distiller = request.json['distiller']
    whiskey.type = request.json['type']
    whiskey.country = request.json['country']
    whiskey.user_token = current_user_token.token 

    db.session.commit()
    response = contact_schema.dump(whiskey)
    return jsonify(response)




