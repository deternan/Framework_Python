
from flask_restplus import Namespace, fields


class CDCnewsDto:
    id = Namespace('id', description='object id')
    type = Namespace('type', description='content type')
    body = Namespace('body', description='content')
    sourceUrl = Namespace('sourceUrl', description='source URL')
    timestamp = Namespace('timestamp', description='timestamp')
    infoSource = Namespace('infoSource', description='content source')

