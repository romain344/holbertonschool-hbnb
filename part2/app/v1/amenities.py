from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from uuid import UUID

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json()
        if not data:
            api.abort(400, "No input data provided")

        try:
            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            api.abort(400, str(e))

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        result = [{'id': a.id, 'name': a.name} for a in amenities]
        return result, 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            UUID(amenity_id)
        except ValueError:
            api.abort(404, "Amenity not found")

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")

        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            UUID(amenity_id)
        except ValueError:
            api.abort(404, "Amenity not found")

        data = request.get_json()
        if not data:
            api.abort(400, "No input data provided")

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            api.abort(400, str(e))

        if not updated_amenity:
            api.abort(404, "Amenity not found")

        return {"message": "Amenity updated successfully"}, 200
