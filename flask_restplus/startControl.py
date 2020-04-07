# coding=utf8

'''
version: March 23, 2020 10:05 AM
Last revision: April 07, 2020 11:37 AM

Author : Chao-Hsuan Ke
'''

'''
Reference

https://www.lagou.com/lgeduarticle/34790.html
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/
https://www.twblogs.net/a/5c2861cfbd9eee16b3dbddf3
https://github.com/noirbizarre/flask-restplus/issues/772

'''

import os, sys
import datetime
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json


from flask import Flask, Blueprint
from flask_restplus import Resource, Api, Namespace
from service import ChatbotService, StatusService, DataService, SelfTestService
from model.DTO import ChinaNewsDto, DeltaDeclarationDTO, GovernmentDeclarationDTO, GoogleNewsDTO
from bson.objectid import ObjectId
from unit import globals as golvar
from unit import responseText as resTxt

from flasgger import Swagger, swag_from


app = Flask(__name__)
api_blueprint = Blueprint('api', 'api', url_prefix='/api')

api = Api(app, prefix="/v1", title="APIs", description="ChatBot APIs.")
ns0 = Namespace("analytics", description="analytics")
ns1 = Namespace("response", description="response")
ns2 = Namespace("chat", description="chat status")
ns3 = Namespace("db", description="Data Query")
ns4 = Namespace("api", description="Data Query")
ns5 = Namespace("Query", description="Data Query")
ns6 = Namespace("Test", description="APIs test")
api.add_namespace(ns0)
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
api.add_namespace(ns5)
api.add_namespace(ns6)
app.register_blueprint(api_blueprint)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

'''
intent
'''
@ns0.route('/input/<string:userName>/<string:query>')
class intent(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'userName': {'description': 'user name',  'type': 'string', 'required': True, 'default': 'my name'},
               'query': {'description': 'query', 'type': 'string', 'required': True, 'default': '口罩可以重複使用嗎'}
    })
    def post(self, userName, query):
        ## Intent
        response = ChatbotService.get_IntentRequestId(userName, query)
        data = {}
        Query_requestId = None
        Query_country = None
        data['userName'] = userName
        if len(response.get('tags')[0])>0:
            data['country'] = response.get('tags')[0].get('locations')[0]
            Query_country = response.get('tags')[0].get('locations')[0]
        else:
            data['country'] = ''
            Query_country = query
        data['requestId'] = response.get('responseId')
        Query_requestId = int(response.get('responseId'))

        if response.get('responseId') == 0:
            typeStr = golvar.govType
        elif response.get('responseId') == 1:
            typeStr = golvar.deltaType
        elif response.get('responseId') == 2:
            typeStr = golvar.deltaType
        elif response.get('responseId') == 3:
            typeStr = golvar.QAType
        elif response.get('responseId') == 4:
            typeStr = golvar.RumorsType
        elif response.get('responseId') == 5:
            typeStr = golvar.EpidemicType
        elif response.get('responseId') == 6:
            typeStr = golvar.TravelAlertType
        elif response.get('responseId') == 7:
            typeStr = golvar.SelfTestType
        elif response.get('responseId') == 8:
            typeStr = golvar.GoogleNewsType

        '''
        Entry
        '''
        data = {}
        data['userName'] = userName


        '''
        check whether has past data (in DB)
        '''
        statusresponse = StatusService.get_Status(userName)
        #print('statusresponse', statusresponse, statusresponse.get('requestId'))
        requestCheck = False


        if Query_requestId == 0 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
            requestCheck = True

        print(Query_requestId, Query_country, userName, query, requestCheck, statusresponse)
        if requestCheck == True:
            if statusresponse is None:
                ## add status
                StatusService.add_status(userName, Query_requestId, typeStr, 1, '', False)
                if (Query_requestId == 0) or (Query_requestId == 2):
                    if Query_country == golvar.Loc_Taiwan or golvar.Loc_Taiwan1 or golvar.Loc_Taiwan2 or golvar.Loc_Taiwan3 or golvar.Loc_Taiwan4 or golvar.Loc_Taiwan5:
                        ## Taiwan Government declaration
                        responseItems = DataService.get_GovernmentDeclaration(golvar.responseNumLimit)
                        data['type'] = golvar.govType
                        if len(responseItems) > 0:
                            data['status'] = True
                        else:
                            data['status'] = False
                        Items = []
                        count = 0
                        for item in responseItems:
                            Items.append(responseItems[item])
                            count += 1
                        data['items'] = Items
                        ## delete status
                        StatusService.delete_Status(userName)
                    elif Query_country == golvar.Loc_China or golvar.Loc_China1 or golvar.Loc_China2 or golvar.Loc_China3 or golvar.Loc_China4:
                        ## China News
                        responseItems = DataService.get_ChinaNews(golvar.responseNumLimit)
                        data['type'] = golvar.pubNewsType
                        if len(responseItems) > 0:
                            data['status'] = True
                        else:
                            data['status'] = False
                        Items = []
                        count = 0
                        for item in responseItems:
                            Items.append(responseItems[item])
                            count += 1
                        data['items'] = Items
                        ## delete status
                        StatusService.delete_Status(userName)
                    else:
                        data['status'] = False
                        data['repeatNotics'] = resTxt.ResponseAllNewsType
                elif Query_requestId == 3:
                    data['status'] = False
                    data['repeatNotics'] = resTxt.ResponseMedicalQAType
                elif Query_requestId == 4:
                    data['status'] = False
                    data['repeatNotics'] = resTxt.ResponseRumorsType
                elif Query_requestId == 5:
                    data['type'] = golvar.EpidemicType
                    responseItems = DataService.get_EpidemicDashboard(userName, Query_country)
                    Items = []
                    for item in responseItems:
                        Items.append(responseItems[item])
                    if len(responseItems['items']) > 0:
                        data['status'] = True
                        data['items'] = Items
                        ## delete status
                        StatusService.delete_Status(userName)
                    else:
                        #data['items'] = None
                        data['repeatNotics'] = resTxt.ResponseCountry
                elif Query_requestId == 6:
                    data['type'] = golvar.TravelAlertType
                    ## travel_alert
                    responseItems = DataService.get_TravelAlert(userName, Query_country)
                    Items = []
                    for item in responseItems:
                        Items.append(responseItems[item])
                    #if len(responseItems['items']) > 0:
                    if len(responseItems) > 0:
                        data['status'] = True
                        data['items'] = Items
                        ## delete status
                        StatusService.delete_Status(userName)
                    else:
                        #data['items'] = None
                        data['repeatNotics'] = resTxt.ResponseCountry
                elif Query_requestId == 7:
                    data['type'] = golvar.SelfTestType
                    responseItems = SelfTestService.chatstartResponse()
                    Items = []
                    for item in responseItems:
                        Items.append(responseItems[item])
                    if len(Items) > 0:
                        data['status'] = True
                        data['items'] = Items
                    else:
                        data['items'] = None
                    ## delete status
                    #StatusService.delete_Status(userName)       ## should been removed
                elif Query_requestId == 8:
                    data['type'] = golvar.GoogleNewsType
                    responseItems = DataService.get_GoogleNews(Query_country, golvar.responseNumLimit)
                    Items = []
                    for item in responseItems:
                        Items.append(responseItems[item])
                    if len(Items) > 0:
                        data['status'] = True
                        data['items'] = Items
                    else:
                        data['items'] = None
                    ## delete status
                    StatusService.delete_Status(userName)
                else:
                    data['status'] = False
                    data['repeatNotics'] = resTxt.repeatResponseType
            else:
                if statusresponse['count'] == 1:
                    if (Query_requestId == 0) or (Query_requestId == 2):
                        if Query_country == golvar.Loc_Taiwan or golvar.Loc_Taiwan1 or golvar.Loc_Taiwan2 or golvar.Loc_Taiwan3 or golvar.Loc_Taiwan4 or golvar.Loc_Taiwan5:
                            ## Taiwan Government declaration
                            responseItems = DataService.get_GovernmentDeclaration(golvar.responseNumLimit)
                            data['type'] = golvar.govType
                            if len(responseItems['items']) > 0:
                                data['status'] = True
                            else:
                                data['status'] = False
                            Items = []
                            count = 0
                            for item in responseItems:
                                Items.append(responseItems[item])
                                count += 1
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        elif Query_country == golvar.Loc_China or golvar.Loc_China1 or golvar.Loc_China2 or golvar.Loc_China3 or golvar.Loc_China4:
                            ## China News
                            responseItems = DataService.get_ChinaNews(golvar.responseNumLimit)
                            data['type'] = golvar.pubNewsType
                            Items = []
                            if len(responseItems['items']) > 0:
                                data['status'] = True
                                for item in responseItems:
                                    Items.append(responseItems[item])
                                data['items'] = Items
                                ## delete status
                                StatusService.delete_Status(userName)
                            else:
                                data['status'] = False
                                data['repeatNotics'] = resTxt.ResponseAllNewsType
                    elif Query_requestId == 3:
                        data['type'] = golvar.QAType
                        responseItems = ChatbotService.get_Response(userName, Query_country, Query_requestId, golvar.responseNumLimit, query)
                        Items = []
                        if len(responseItems['items']) > 0:
                            data['statue'] = True
                            for item in responseItems:
                                Items.append(responseItems[item])
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        else:
                            data['statue'] = False
                            data['repeatNotics'] = resTxt.ResponseMedicalQAType
                        #print(len(responseItems['items']))
                    elif Query_requestId == 4:
                        data['type'] = golvar.RumorsType
                        responseItems = ChatbotService.get_Response(userName, Query_country, Query_requestId, golvar.responseNumLimit, query)
                        Items = []
                        if len(responseItems['items']) > 0:
                            data['statue'] = True
                            for item in responseItems:
                                Items.append(responseItems[item])
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        else:
                            data['statue'] = False
                            data['repeatNotics'] = resTxt.ResponseRumorsType
                    elif Query_requestId == 5:
                        data['type'] = golvar.EpidemicType
                        #DataService.get_EpidemicDashboard(userName, Query_country)
                        responseItems = ChatbotService.get_Response(userName, Query_country, Query_requestId, golvar.responseNumLimit, query)
                        Items = []
                        if len(responseItems['items']) > 0:
                            data['statue'] = True
                            for item in responseItems:
                                Items.append(responseItems[item])
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        else:
                            data['statue'] = False
                            data['repeatNotics'] = resTxt.ResponseCountry
                    elif Query_requestId == 6:
                        data['type'] = golvar.TravelAlertType
                        responseItems = ChatbotService.get_Response(userName, Query_country, Query_requestId, golvar.responseNumLimit, query)
                        Items = []
                        if len(responseItems['items']) > 0:
                            data['statue'] = True
                            for item in responseItems:
                                Items.append(responseItems[item])
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        else:
                            data['statue'] = False
                            data['repeatNotics'] = resTxt.ResponseCountry
                    elif Query_requestId == 7:
                        data['type'] = golvar.SelfTestType

                    elif Query_requestId == 8:
                        data['type'] = golvar.GoogleNewsType
                        responseItems = ChatbotService.get_Response(userName, Query_country, Query_requestId, golvar.responseNumLimit, query)
                        Items = []
                        if len(responseItems['items']) > 0:
                            data['statue'] = True
                            for item in responseItems:
                                Items.append(responseItems[item])
                            data['items'] = Items
                            ## delete status
                            StatusService.delete_Status(userName)
                        else:
                            data['statue'] = False
                            data['repeatNotics'] = resTxt.repeatResponseType

        #response = ChatbotService.get_Response(userName, data['country'], data['requestId'], golvar.responseNumLimit, query)
        return data
        #return response


'''
chat-bot-api-controller 
GET /analytics/welcome
'''
@ns0.route('/welcome')
class welcome(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    })
    def get(self):
        data = {}
        data['responseText'] = golvar.welcomeText
        return data

'''
response (Entry)
GET /response/input
'''
@ns1.route('/input/<string:userName>/<string:country>/<string:query>/<int:requestId>')
class intent(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'userName': {'description': 'user name',  'type': 'string', 'required': True, 'default': 'my name'},
               'country': {'description': 'country', 'type': 'string', 'required': True, 'default': '美國'},
               'query': {'description': 'query', 'type': 'string', 'required': True, 'default': '美國的疫情如何'},
               'requestId': {'description': 'request Id', 'required': True, 'default': '0'}
    })
    def post(self, userName, country, query, requestId):
        #response = ChatbotService.get_IntentRequestId(userName, query)
        data = {}
        #data['responseText'] = golvar.welcomeText

        #if requestId == 0:



        return data



'''
chat-status-api-controller 
status
'''
@ns2.route('/status/add/<string:name>/<string:typeStr>/<int:requestId>/<int:count>', methods=['POST'])
class statusInsert(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True},
               'typeStr': {'description': 'data type',  'type': 'string', 'required': True, 'default': 'status'},
               'requestId': {'description': 'requestId', 'default': '0'},
               'count': {'description': 'count', 'default': '0'}
    })
    def post(self, name, typeStr, requestId, count):
        data = {}
        data['userName'] = name
        data['typeStr'] = typeStr
        data['requestId'] = requestId
        data['count'] = count
        data['timestamp'] = datetime.datetime.utcnow()
        response = StatusService.add_status(data)
        return response

@ns2.route('/status/check/<string:name>', methods=['POST'])
class statusCheck(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True}
    })
    def post(self, name):
        data = StatusService.get_Status(name)
        responseData = {}
        responseData['id'] = str(data.statusDto.id)
        responseData['userName'] = data.statusDto.userName
        responseData['type'] = data.statusDto.type
        responseData['requestId'] = data.statusDto.requestId
        responseData['count'] = data.statusDto.count
        responseData['timestamp'] = str(data.statusDto.timestamp.utcnow())
        return responseData

@ns2.route('/status/delete/<string:name>', methods=['POST'])
class statusDelete(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True}
    })
    def post(self, name):
        response = StatusService.delete_Status(name)
        return response


'''
data-query-controller
'''
'''
POST /db/public/China/news
'''
@ns3.route('/public/China/news/<string:country>/<int:responseNum>', methods=['POST'])
class ChinaNews(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '中國'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.pubNewsType
        responseItems = DataService.get_ChinaNews(country, responseNum)
        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Item = responseItems[item]
            Item = ChinaNewsDto
            Items.append(responseItems[item])
            #print(count, item, responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
POST /db/delta/declaration
'''
@ns3.route('/delta/declaration/<string:country>/<int:responseNum>', methods=['POST'])
class deltadeclaration(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '台灣'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.deltaType
        responseItems = DataService.get_DeltaDeclaration(country, responseNum)

        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Item = responseItems[item]
            Item = DeltaDeclarationDTO
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
POST /db/government/Taiwan/declaration  collection_governmentdeclaration
'''
@ns3.route('/government/Taiwan/declaration/<string:country>/<int:responseNum>', methods=['POST'])
class governmentdeclaration(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '台灣'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.govType
        responseItems = DataService.get_GovernmentDeclaration(country, responseNum)

        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
API request
'''
'''
POST /api/rumors/
rumors API query
'''
@ns4.route('/rumors/<string:name>/<string:query>', methods=['POST'])
class queryRumors(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True},
               'query': {'description': 'query',  'type': 'string', 'required': True, 'default': '口罩可以重複使用嗎'}
    })
    def post(self, name, query):
        data = {}
        data['userName'] = name
        data['type'] = golvar.RumorsType
        data['query'] = query

        url = 'http://10.136.154.13:5568/analytics/ir?'
        postQuery = {'userName': name,
                     'type': golvar.RumorsType,
                     'query' : query
                     }
        print(postQuery)
        #x = requests.post(url, postQuery)
        x = requests.get(url, postQuery)
        #print(x)
        return x.json()

'''
POST /api/rumors/
rumors API query
'''
@ns4.route('/google/news/<string:country>/<int:responseNum>', methods=['POST'])
class getGoogleNews(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'country': {'description': 'country',  'type': 'string', 'required': True, 'default': '台灣'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        #data['userName'] = name
        #data['country'] = country
        data['type'] = golvar.GoogleNewsType
        responseItems = DataService.get_GoogleNews(country, responseNum)
        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data


'''
CDC news
'''
@ns5.route('/db/query/newsCDC/<string:id>')
class dbQuery(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'id': 'the task identifier'
    })
    def get(self, id):
        data = ChatbotService.get_CDC_new(id)
        ## transfer to JSON
        responseData = {}
        responseData['id'] = str(data.CDCnewsDto.id)
        jsonstr = data.CDCnewsDto.body
        responseData['text'] = jsonstr
        return responseData



'''
GET and POST 
'''
@ns6.route('/<int:id>/<string:name>')
class HelloWorld(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'id': 'the task identifier',
        'name': 'the user name'
    })
    def get(self, id):
        return {
            'status': 'you get a request.',
            'id': id
        }

    def post(self, id, name):
        return {
            'status': 'you post a request.',
            'id': id,
            'name': name
        }


'''
Main
'''
if __name__ == '__main__':
    app.run(debug=True)
