
from flask_restplus import Namespace


class statusDto:
    id = Namespace('id', description='object id')
    userName = Namespace('userName', description='user name')
    type = Namespace('type', description='content type')
    requestId = Namespace('requestId', description='requiredId')
    count = Namespace('count', description='count')
    timestamp = Namespace('timestamp', description='timestamp')


