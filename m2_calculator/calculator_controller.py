from flask import Flask, jsonify, request
from pydantic import ValidationError

from dtos import PowRequest, FibRequest, FactRequest, CalculatorResponse
from calculator_service import CalculatorService
from m2_calculator.cache import PowCache, FibCache, FactCache

calculator_app = Flask(__name__)
calculator_service = CalculatorService()

pow_cache: PowCache = PowCache()
fib_cache: FibCache = FibCache()
fact_cache: FactCache = FactCache()

@calculator_app.route('/calculator/pow', methods=['POST'])
async def pow_operation():
    global pow_cache

    try:
        data = PowRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if pow_cache.pow_request is not None:
        if pow_cache.pow_request.base == data.base and pow_cache.pow_request.exponent == data.exponent:
            return jsonify(pow_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_power(data)

    pow_cache.pow_request = data
    pow_cache.result = response.result

    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/fibonacci', methods=['POST'])
async def fibonacci():
    global fib_cache

    try:
        data = FibRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if fib_cache.fib_request is not None:
        if fib_cache.fib_request.number == data.number:
            return jsonify(fib_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_fibonacci(data)

    fib_cache.fib_request = data
    fib_cache.result = response.result

    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/factorial', methods=['POST'])
async def factorial():
    global fact_cache

    try:
        data = FactRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if fact_cache.fact_request is not None:
        if fact_cache.fact_request.n == data.n:
            return jsonify(fact_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_factorial(data)

    fact_cache.fact_request = data
    fact_cache.result = response.result

    return jsonify(response.model_dump()), 200


if __name__ == '__main__':
    calculator_app.run(port=5002)
