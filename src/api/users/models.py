import os 
from src import db
from flask_admin.contrib.sqla import ModelView  # new
from sqlalchemy.sql import func

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class UsersAdminView(ModelView):
    column_searchable_list = ('username', 'email',)
    column_editable_list = ('username', 'email', 'created_date',)
    column_filters = ('username', 'email',)
    column_sortable_list = ('username', 'email', 'active', 'created_date',)
    column_default_sort = ('created_date', True)

# new
if os.getenv("FLASK_ENV") == "development":
    from src import admin
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(UsersAdminView(User, db.session))

