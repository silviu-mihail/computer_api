from flask import Flask, jsonify


calculator_app = Flask(__name__)


@calculator_app.route('/calculator/pow', methods=['POST'])
def pow_operation():
    return jsonify({
        'service': 'Calculator',
        'message': "Pow operation"
    }), 200

@calculator_app.route('/calculator/fibonacci', methods=['POST'])
def fibonacci():
    return jsonify({
        'service': 'Calculator',
        'message': "Fibonacci"
    }), 200

@calculator_app.route('/calculator/factorial', methods=['POST'])
def factorial():
    return jsonify({
        'service': 'Calculator',
        'message': "Factorial"
    }), 200


if __name__ == '__main__':
    calculator_app.run(port=5002)
