
from flask_restplus import Namespace


class GoogleNewsDTO:
    rank = Namespace('rank', description='Rank')
    #type = Namespace('type', description='content type')
    title = Namespace('title', description='content title')
    description = Namespace('description', description='content')
    infoSource = Namespace('infoSource', description='content source')      # author
    sourceUrl = Namespace('sourceUrl', description='source URL')            # url
    pubDate = Namespace('pubDate', description='published Data')            # publishedAt
    #tag = Namespace('tag', description='tags')
    #continent = Namespace('continent', description='continent')
    #country = Namespace('country', description='country')
    #city = Namespace('city', description='city')
    #timestamp = Namespace('timestamp', description='timestamp')


