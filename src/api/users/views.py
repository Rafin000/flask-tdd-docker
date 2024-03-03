from flask import Blueprint, request
from src import db
from src.api.users.crud import add_user, delete_user, get_all_users, get_user_by_email, get_user_by_id, update_user
from src.api.users.models import User
from flask_restx import Resource, Api, fields , Namespace

# users_blueprint = Blueprint('users', __name__)
# api = Api(users_blueprint)


users_namespace = Namespace("users") 


# user = api.model('User', {
#     'id': fields.Integer(readOnly=True),
#     'username': fields.String(required=True),
#     'email': fields.String(required=True),
#     'created_date': fields.DateTime,
# })

user = users_namespace.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})


class UsersList(Resource):
    @users_namespace.expect(user, validate=True)
    def post(self):
        """Creates a new user."""
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}

        user = get_user_by_email(email)  # updated
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        add_user(username, email)  # new

        response_object['message'] = f'{email} was added!'
        return response_object, 201
    

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users.""" 
        return get_all_users(), 200  # updated

class Users(Resource):

    @users_namespace.marshal_with(user)
    @users_namespace.response(200, "Success") 
    @users_namespace.response(404, "User <user_id> does not exist")  # new
    @users_namespace.marshal_with(user)
    def get(self, user_id):
        """Returns a single user."""  
        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200
    


    @users_namespace.expect(user, validate=True)
    def put(self, user_id):
        """Updates a user."""  
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):  # updated
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(user, username, email)  # new

        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200



    def delete(self, user_id):
        """"Deletes a user."""  
        response_object = {}
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        delete_user(user)

        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200
    

# api.add_resource(UsersList, '/users')
# api.add_resource(Users, '/users/<int:user_id>')
    
users_namespace.add_resource(UsersList, "")  
users_namespace.add_resource(Users, "/<int:user_id>")