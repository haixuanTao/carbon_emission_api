from flask import Blueprint, current_app
from flask_restful import Api

from instagram_carbon_emission.extensions import apispec
from instagram_carbon_emission.api.resources import UserResource, UserList
from instagram_carbon_emission.api.resources.user import UserSchema

from instagram_carbon_emission.api.resources.search import Search


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(Search, '/search/<string:user_id>')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
