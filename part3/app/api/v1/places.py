from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

amenty_model = api.model('placeamenity', {
    'id': fields.String(description='amenty ID'),
    'name': fields.String(description='amenty name')  
})

user_model = api.model('placeuser',{
    'id': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String()  
})

review_model = api.model('placereview',{
    'id': fields.String(),
    'text': fields.String(),
    'rating': fields.String(),
    'user': fields.String()
})

place_input_model = api.model('placeinput', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'amenities': fields.List(fields.String, description='List of Amenity IDs')
})

place_model = api.inherit('Place', place_input_model, {
    'id': fields.String(),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenty_model)),
    'reviews': fields.List(fields.Nested(review_model))
})

@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Public: List all places"""
        places = facade.get_all_places()
        return [p for p in places], 200

    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def post(self):
        """Authenticated: Create a new place"""
        data = api.payload
        user_identity = get_jwt_identity()

        data['owner_id'] = user_identity['id']
        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place found')
    @api.response(404, 'Not found')
    def get(self, place_id):
        """Public: Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @api.expect(place_input_model)
    @api.response(200, 'Updated')
    @api.response(404, 'Not found')
    @api.response(403, 'Not authorized')
    @jwt_required()
    def put(self, place_id):
        """Admin or Owner: Update a place"""
        user_identity = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        
        # Vérification rôle admin ou owner
        if place['owner']['id'] != user_identity['id'] and user_identity.get('role') != 'admin':
            return {'error': 'You do not have permission to modify this place'}, 403

        updated_place = facade.update_place(place_id, api.payload)
        return updated_place, 200

    @api.response(204, 'Deleted')
    @api.response(404, 'Not found')
    @api.response(403, 'Not authorized')
    @jwt_required()
    def delete(self, place_id):
        """Admin or Owner: Delete a place"""
        user_identity = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        
        # Vérification rôle admin ou owner
        if place['owner']['id'] != user_identity['id'] and user_identity.get('role') != 'admin':
            return {'error': 'You do not have permission to delete this place'}, 403

        facade.delete_place(place_id)
        return '', 204