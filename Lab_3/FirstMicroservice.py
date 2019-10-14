from flask import Flask, jsonify, request

app = Flask(__name__)

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

if __name__ == '__main__':
    print('URL MAP')
    print(app.url_map)
    app.run()