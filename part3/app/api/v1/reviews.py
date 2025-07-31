from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
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
        """Authenticated: Create a review"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        place = facade.get_place(data['place_id'])

        if not place:
            return {'error': 'Place not found'}, 404

        # Vérifier si l'utilisateur est le propriétaire du lieu
        if place['owner']['id'] == current_user_id:
            return {'error': 'You cannot review your own place.'}, 400

        # Vérifier si l'utilisateur a déjà évalué ce lieu
        if facade.has_user_reviewed_place(current_user_id, data['place_id']):
            return {'error': 'You have already reviewed this place.'}, 400

        data['user_id'] = current_user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Public: List all reviews"""
        reviews = [r.to_dict() for r in facade.get_all_reviews()]
        return reviews, 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Public: Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_input_model, validate=True)
    def put(self, review_id):
        """Authenticated: Update own review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """Authenticated: Delete own review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {}, 204