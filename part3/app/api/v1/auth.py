from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

# permet de faire la creationt de auth
api = Namespace('auth', descrption='Aithentication operations')

# validation d'entree pour email et password
login_model = api.model('login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class login(Resource):
    @api.expect(login_model)
    def post(self):
        crendentials = api.payload

        # recupere l'email 
        user = facade.get_user_by_email(crendentials['email'])

        # verifie que le password ou le user et valide
        if not user or not user.verify_password(crendentials['password']):
            return{'error': 'invalid credentails'}, 401
        
        # creation du token avec id et admin
        access_token = create_access_token(identity={
            'id': str(user.id),
            'id_admin': user.is_admin
        })

        # retourn du token aux client
        return {'access_token': access_token}