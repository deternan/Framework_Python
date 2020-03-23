# coding=utf8

'''
version: March 23, 2020 10:05 AM
Last revision: March 23, 2020 05:20 PM

Author : Chao-Hsuan Ke
'''


from model import UserDto

def get_return_new_user(data):
    #userName = UserDto.query.filter_by(email=data['name']).first()
    data.__getitem__('name')
    print('userName', data.__getitem__('name'))
    UserDto.UserDto.user.name = data.__getitem__('name')
    UserDto.UserDto.user.email = data.__getitem__('email')
    UserDto.UserDto.id = "123456";
    _userData = UserDto
    return _userData


    # user = UserDto.query.filter_by(email=data['email']).first()
    # if not user:
    #     new_user = UserDto(
    #         email=data['email'],
    #         username=data['username'],
    #         registered_on=datetime.datetime.utcnow()
    #     )
    #     ##save_changes(new_user)
    #     response_object = {
    #         'status': 'success',
    #         'message': 'Successfully registered.'
    #     }
    #     return response_object, 201
    # else:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'User already exists. Please Log in.',
    #     }
    #     return response_object, 409


# def get_all_users():
#     return UserDto.query.all()
#
#
# def get_a_user(public_id):
#     return UserDto.query.filter_by(public_id=public_id).first()

