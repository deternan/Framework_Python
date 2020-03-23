
from flask_restplus import Namespace, fields


class UserDto:
    id = Namespace('id', description='user id')
    items = Namespace('user', description='user related operations (items)')
    user = items.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'name': fields.String(required=True, description='user username')
    })