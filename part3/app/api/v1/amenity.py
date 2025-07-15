from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Modèle pour les données d'entrée
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nom de l\'équipement (amenity)')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin only')
    def post(self):
        """Ajouter un équipement (Admin uniquement)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Seul un administrateur peut créer une commodité'}, 403

        data = api.payload
        new_amenity = facade.create_amenity(data)
        return new_amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Lister tous les équipements disponibles"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Obtenir les détails d'un équipement"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {"error": "Amenity not found"}, 404

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Forbidden - Admin only')
    def put(self, amenity_id):
        """Modifier un équipement existant (Admin uniquement)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Seul un administrateur peut modifier une commodité'}, 403

        data = api.payload
        updated = facade.update_amenity(amenity_id, data)
        if updated:
            return updated.to_dict(), 200
        return {"error": "Amenity not found"}, 404

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Forbidden - Admin only')
    def delete(self, amenity_id):
        """Supprimer un équipement (Admin uniquement)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Seul un administrateur peut supprimer une commodité'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        facade.delete_amenity(amenity_id)
        return {"message": "Amenity supprimée avec succès"}, 200