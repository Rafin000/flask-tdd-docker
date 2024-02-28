
from flask import Blueprint, request , jsonify
from flask_restx import Resource, Api, fields
from src import db
from src.api.models import User


users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)


user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})

class UsersList(Resource):
    @api.marshal_with(user)
    def get(self, user_id=None):
        if user_id is not None:
            user = User.query.filter_by(id=user_id).first()
            # return {
            #     'username': user.username,
            #     'email': user.email,
            #     'active': user.active
            # }, 200

            """
            if we use Marshalling then the User Model Object get auto transformed
            for dict. and then JSON
            """
            if not user:
                api.abort(404, f"User {user_id} does not exist")
            return user, 200

        else:
            users = User.query.all()
            user_list = []
            for user in users:
                user_dict = {
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
                user_list.append(user_dict)
            return user_list, 200
        

    @api.expect(user, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        
        # if len(data)==0:
        #     return {'message': 'Input payload validation failed'}, 400
        
        # if 'email' not in data or 'username' not in data:
        #     return {'message': 'Input payload validation failed'}, 400
        
        if User.query.filter_by(email=email).first():
             return {'message' : 'Sorry. That email already exists.'}, 400

        
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return {
            'message' : f'{email} was added!'
        }, 201
    
    
api.add_resource(UsersList, '/users', '/users/<int:user_id>', endpoint='get_user')