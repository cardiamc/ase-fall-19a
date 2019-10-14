from flask import Flask, jsonify, request
from teams import teams

app = Flask(__name__)
app.register_blueprint(teams)

if __name__ == '__main__':
    app.run(debug=True)