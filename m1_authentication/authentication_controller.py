from flask import Flask, jsonify


authenticator_app = Flask(__name__)


@authenticator_app.route('/authenticator/test', methods=['GET'])
def controller_test():
    return jsonify({
        'service': 'Authenticator',
        'data': 'Login successful'
    }), 200


if __name__ == '__main__':
    authenticator_app.run(port = 5001)
