from dtos import PowRequest, FibRequest, FactRequest, CalculatorResponse


class PowCache:
    def __init__(self, pow_request: PowRequest = None, result: int = -1):
        self.pow_request: PowRequest = pow_request
        self.result = result

    def to_response(self):
        return CalculatorResponse(
            message=f"Cached response: pow({self.pow_request.base}, {self.pow_request.exponent})",
            result=self.result
        )


class FibCache:
    def __init__(self, fib_request: FibRequest = None, result: int = -1):
        self.fib_request = fib_request
        self.result = result

    def to_response(self):
        return CalculatorResponse(
            message=f'Cached response: fib({self.fib_request.number})',
            result=self.result
        )


class FactCache:
    def __init__(self, fact_request: FactRequest = None, result: int = -1):
        self.fact_request = fact_request
        self.result = result

    def to_response(self):
        return CalculatorResponse(
            message=f'Cached response: fact({self.fact_request.n})',
            result=self.result
        )