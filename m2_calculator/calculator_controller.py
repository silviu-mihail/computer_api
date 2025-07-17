from flask import Flask, jsonify


calculator_app = Flask(__name__)


@calculator_app.route('/calculator/test', methods=['GET'])
def controller_test():
    return jsonify({
        'service': 'Calculator',
        'data': "Computation done"
    }), 200


if __name__ == '__main__':
    calculator_app.run(port=5002)
