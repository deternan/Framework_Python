
from flask_restplus import Namespace


class ChinaNewsDto:
    id = Namespace('id', description='object id')
    rank = Namespace('rank', description='Rank')
    type = Namespace('type', description='content type')
    title = Namespace('title', description='content title')
    body = Namespace('body', description='content')
    infoSource = Namespace('infoSource', description='content source')
    sourceUrl = Namespace('sourceUrl', description='source URL')
    pubDate = Namespace('pubDate', description='published Data')
    continent = Namespace('continent', description='continent')
    country = Namespace('country', description='country')
    timestamp = Namespace('timestamp', description='timestamp')


