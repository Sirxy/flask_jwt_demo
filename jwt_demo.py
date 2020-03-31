import functools
from flask import redirect, url_for


# def login_required(view):
# 	@functools.wraps(view)
# 	def wrapped_view(**kwargs):
# 		if 'user_info' not in g:
# 			# return redirect(url_for('sys.user_login'))
# 			return jsonify('用户没有登录，请登录')
# 		if g.user_info is None:
# 			return jsonify({'data': '用户没有登录'})
# 		return view(**kwargs)
# 	return wrapped_view





# import timeit
#
# print(timeit.timeit(stmt= 'list(i**2 for i in normal_list)', setup = 'normal_list=range(10000)', number=10))
#
# print(timeit.repeat(stmt= 'list(i**2 for i in normal_list)', setup = 'normal_list=range(10000)', repeat=2, number=10))

list1 = [1, 2]
list1.extend([45, 6])


import jwt
import datetime
from flask import current_app

JWT_SECRET = ""


def generate_jwt(payload, timeout=60, JWT_SECRET=None):
	""" 生成token
	:param payload: dict 载荷
	:param timeout:  有效期 默认60分钟
	:param JWT_SECRET: 密钥
	:return: token
	"""
	_payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)}
	_payload.update(payload)

	headers = {
		'typ': 'jwt',
		'alg': 'HS256'
	}

	if not JWT_SECRET:
		JWT_SECRET = current_app.config['JWT_SECRET']
	token = jwt.encode(_payload, key=JWT_SECRET, algorithm='HS256', headers=headers).decode('utf-8')
	return token


def verify_jwt(token, JWT_SECRET=None):
	""" 检验token
	:param token: token
	:param JWT_SECRET: 密钥
	:return: dict: payload
	"""
	result = {'status': False, 'data': None}
	if not JWT_SECRET:
		JWT_SECRET = current_app.config['JWT_SECRET']
	try:
		payload = jwt.decode(token, JWT_SECRET, True)
		result['status'] = True
		result['data'] = payload
	except jwt.exceptions.ExpiredSignatureError:
		result['data'] = {}
		result['message'] = "token已失效"
		result['code'] = "403"
	except jwt.DecodeError:
		result['error'] = 'token认证失败'
	except jwt.InvalidTokenError:
		result['data'] = {}
		result['message'] = "非法的token"
		result['code'] = "401 "
	return result


if __name__ == '__main__':
	token = generate_jwt({'uid': '123'}, 600, JWT_SECRET='secretkey')
	print(token)  # eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODU2Nzc4MDcsInVpZCI6IjEyMyJ9.R0AbMkp7FbVPGVVzJ2Hu20O2jSgjJRYcTU0cKKR1Dmo
	payload = verify_jwt(token, JWT_SECRET='secretkey')
	print(payload)  # {'status': True, 'data': {'exp': 1585677807, 'uid': '123'}}









































