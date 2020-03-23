# coding=utf8

'''
version: March 23, 2020 10:05 AM
Last revision: March 23, 2020 05:25 PM

Author : Chao-Hsuan Ke
'''

'''
Reference

https://www.lagou.com/lgeduarticle/34790.html
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

'''

import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from flask import Flask
from flask_restplus import Resource, Api, model
from flask import request
from model import UserDto
from service import user_service


app = Flask(__name__)
api = Api(app, prefix="/v1", title="Users", description="Users CURD api.")

_user = UserDto.UserDto

@api.route('/hello')
class UserApi(Resource):
    def get(self):
        return {
            'hello': 'world',
            'user': '1'}


'''
User query testing
'''
@api.route('/query/user/<string:email>/<string:name>')
class UserQuery(Resource):
    @api.doc('Query a user')
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'email': 'the user email',
        'name': 'the user name'
    })
    def post(self, email, name):
        data = {}
        data['email'] = email
        data['name'] = name
        returnData = user_service.get_return_new_user(data)
        #print(user_service.get_return_new_user(data))
        print('id', returnData.UserDto.id)
        print('items.user.name', returnData.UserDto.user.name)
        print('items.user.email', returnData.UserDto.user.email)
        return data
        # return {
        #     'email': email,
        #     'name': name
        # }


'''
GET and POST 
'''
@api.route('/<int:id>/<string:name>')
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




if __name__ == '__main__':
    app.run()