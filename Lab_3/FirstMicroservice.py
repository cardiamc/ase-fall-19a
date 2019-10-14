from flask import Flask, jsonify, request
from werkzeug.routing import BaseConverter, ValidationError

_USERS = {'1':'Fred', '2':'Barney', '3':'Wilma'}
_IDS = {val : id for id, val in _USERS.items()}

class RegisteredUser(BaseConverter):
    def to_python(self, value):
        if value in _USERS:
            return _USERS[value]
        raise ValidationError()

    def to_url(self, value):
        return _IDS[value]

app = Flask(__name__)
app.url_map.converters['registered'] = RegisteredUser

@app.route('/api', methods=['POST', 'GET', 'DELETE'])
def my_microservice():
    print('request ')
    print(request)
    response = jsonify({'Hello': 'World'})
    print('response ')
    print(response)
    print('response.data ')
    print(response.data)
    return response

# typo : varible_name
@app.route('/api/person/<registered:name>')
def person(name):
    response = jsonify({'Hello': name})
    return response

if __name__ == '__main__':
    print('URL MAP')
    print(app.url_map)
    app.run()