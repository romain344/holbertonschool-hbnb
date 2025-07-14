from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'place_id': fields.String(required=True)
})

review_output_model = api.model('Review', {
    'id': fields.String(),
    'text': fields.String(),
    'rating': fields.Integer(),
    'user_id': fields.String(),
    'place_id': fields.String()
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_input_model, validate=True)
    def post(self):
        current_user = get_jwt_identity()
        data = api.payload

        # Vérifier que l'utilisateur n'évalue pas son propre lieu
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        if place['owner']['id'] == current_user['id']:
            return {'error': 'Vous ne pouvez pas évaluer votre propre lieu'}, 400

        # Vérifier que l'utilisateur n'a pas déjà évalué ce lieu
        existing_review = facade.get_review_by_user_and_place(current_user['id'], data['place_id'])
        if existing_review:
            return {'error': 'Vous avez déjà évalué ce lieu'}, 400

        # Créer l'avis avec user_id injecté
        data['user_id'] = current_user['id']

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        reviews = [r.to_dict() for r in facade.get_all_reviews()]
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_input_model, validate=True)
    def put(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Admin ou Owner
        if review.user_id != current_user['id'] and current_user.get('role') != 'admin':
            return {'error': 'Action non autorisée'}, 403

        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Admin ou Owner
        if review.user_id != current_user['id'] and current_user.get('role') != 'admin':
            return {'error': 'Action non autorisée'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review supprimée avec succès'}, 200