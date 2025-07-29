from flask import Flask, jsonify, request
from pydantic import ValidationError

from dtos import PowRequest, FibRequest, FactRequest, CalculatorResponse
from calculator_service import CalculatorService
from m2_calculator.cache import PowCache, FibCache, FactCache
from shared.telemetry import init_telemetry
from calc_logger import logger


calculator_app = Flask(__name__)
init_telemetry(calculator_app,
               service_name='calculator',
               trace_file='calculator_traces.jsonl')
calculator_service = CalculatorService()


pow_cache: PowCache = PowCache()
fib_cache: FibCache = FibCache()
fact_cache: FactCache = FactCache()


@calculator_app.route('/calculator/pow', methods=['POST'])
async def pow_operation():
    logger.info('Pow endpoint has been called')

    try:
        logger.info('Validating JSON request')

        data = PowRequest.model_validate(request.get_json())
    except ValidationError:
        logger.error('Invalid JSON request')

        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if pow_cache.pow_request is not None:
        if (pow_cache.pow_request.base == data.base
                and pow_cache.pow_request.exponent == data.exponent):
            logger.info('The result has been taken from the cache')
            return jsonify(pow_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_power(data)

    pow_cache.pow_request = data
    pow_cache.result = response.result

    logger.info('Endpoint pow ran successfully')

    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/fibonacci', methods=['POST'])
async def fibonacci():
    logger.info('Fibonacci endpoint has been called')

    try:
        logger.info('Validating JSON request')

        data = FibRequest.model_validate(request.get_json())
    except ValidationError:
        logger.error('Invalid JSON request format')

        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if fib_cache.fib_request is not None:
        if fib_cache.fib_request.number == data.number:
            logger.info('The result has been taken from the cache')
            return jsonify(fib_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_fibonacci(data)

    fib_cache.fib_request = data
    fib_cache.result = response.result

    logger.info('Endpoint fibonacci ran successfully')

    return jsonify(response.model_dump()), 200


@calculator_app.route('/calculator/factorial', methods=['POST'])
async def factorial():
    logger.info('Factorial endpoint has been called')

    try:
        logger.info('Validating JSON request')

        data = FactRequest.model_validate(request.get_json())
    except ValidationError:
        logger.error('Invalid JSON request format')

        return jsonify(CalculatorResponse(
            message="JSON validation failed",
            result=-1
        ).model_dump()), 400

    if fact_cache.fact_request is not None:
        if fact_cache.fact_request.n == data.n:
            logger.info('The result has been taken from the cache')
            return jsonify(fact_cache.to_response().model_dump()), 200

    response = await calculator_service.compute_factorial(data)

    fact_cache.fact_request = data
    fact_cache.result = response.result

    logger.info('Endpoint factorial ran successfully')

    return jsonify(response.model_dump()), 200


if __name__ == '__main__':
    logger.info('Started service calculator')

    calculator_app.run(port=5002)
