from flask import Flask, jsonify, request
from pydantic import ValidationError

from dtos import PowRequest, FibRequest, FactRequest, CalculatorResponse
from calculator_service import CalculatorService

calculator_app = Flask(__name__)
calculator_service = CalculatorService()


@calculator_app.route('/calculator/pow', methods=['POST'])
async def pow_operation():
    try:
        data = PowRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    response = await calculator_service.compute_power(data)
    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/fibonacci', methods=['POST'])
async def fibonacci():
    try:
        data = FibRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    response = await calculator_service.compute_fibonacci(data)
    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/factorial', methods=['POST'])
async def factorial():
    try:
        data = FactRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    response = await calculator_service.compute_factorial(data)
    return jsonify(response.model_dump()), 200


if __name__ == '__main__':
    calculator_app.run(port=5002)
