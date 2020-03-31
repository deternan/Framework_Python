
from flask_restplus import Namespace


class DeltaDeclarationDTO:
    id = Namespace('id', description='object id')
    rank = Namespace('rank', description='Rank')
    type = Namespace('type', description='content type')
    title = Namespace('title', description='content title')
    body = Namespace('body', description='content')
    infoSource = Namespace('infoSource', description='content source')
    sourceUrl = Namespace('sourceUrl', description='source URL')
    pubDate = Namespace('pubDate', description='published Data')
    tag = Namespace('tag', description='tags')
    continent = Namespace('continent', description='continent')
    country = Namespace('country', description='country')
    city = Namespace('city', description='city')
    timestamp = Namespace('timestamp', description='timestamp')


