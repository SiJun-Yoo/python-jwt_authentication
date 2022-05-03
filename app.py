from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = 'SIJUNYOO'

client = MongoClient('localhost', 27017)
db = client.sijun

userId = "dbtlwns"
userPassword = hashlib.sha256("1234".encode('utf-8')).hexdigest()
userData = {
    'id':userId,
    'password':userPassword
}
db.users.insert_one(userData)

@app.route('/user/login', methods=['POST'])
def login():
    json = request.get_json();
    id = json['id']
    password = json['password']
    encryptedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user = db.users.find_one({'id':id,'password':encryptedPassword})

    if user is not None:
        payload = {
            'id': user['id'],
            'exp': datetime.utcnow()+timedelta(seconds=10)
        }
        token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
        return jsonify({
            'status':200,
            'token':token,
            'msg':'로그인 완료'
        })
    else:
        return jsonify({
            'status': 401,
            'msg': '아이디/비밀번호가 다름'
        })

@app.route('/user/info',methods=['GET'])
def getUserInfo():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        return payload['id']
    except jwt.ExpiredSignatureError:
        return "만료"
    except jwt.exceptions.DecodeError:
        return "잘못된 토큰"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)