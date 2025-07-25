from repos.calculator_repos import (
    PowerRepository,
    FibonacciRepository,
    FactorialRepository
)
from dtos import (
    PowRequest,
    FibRequest,
    FactRequest,
    CalculatorResponse)
from calc_logger import logger


class CalculatorService:
    def __init__(self):
        self._power_repository = PowerRepository()
        self._fib_repository = FibonacciRepository()
        self._fact_repository = FactorialRepository()

    async def compute_power(self, data: PowRequest) -> CalculatorResponse:
        logger.info('Pow service called')

        existing = await self._power_repository.get_result(
            data.base,
            data.exponent
        )
        if existing:
            logger.info('The result of the pow operation '
                        'was found in the database')
            return CalculatorResponse(
                message=f"Retrieved from database: "
                        f"pow({data.base}, {data.exponent})",
                result=existing.result
            )

        logger.info('Computing the result - pow')
        result = self._calculate_power(data.base, data.exponent)

        logger.info('Inserting result into the database - pow')
        await self._power_repository.insert(data.base, data.exponent, result)

        logger.info('Service pow ran successfully')
        return CalculatorResponse(
            message=f"Computed and stored: pow({data.base}, {data.exponent})",
            result=result
        )

    async def compute_factorial(self, data: FactRequest) -> CalculatorResponse:
        logger.info('Factorial service called')

        existing = await self._fact_repository.get_result(data.n)
        if existing:
            logger.info('The result of the factorial '
                        'operation was found in the database')
            return CalculatorResponse(
                message=f"Retrieved from database: fact({data.n})",
                result=existing.result
            )

        logger.info("Computing the result - factorial")
        result = self._calculate_factorial(data.n)

        logger.info('Inserting result into database - factorial')
        await self._fact_repository.insert(data.n, result)

        logger.info('Service factorial ran successfully')
        return CalculatorResponse(
            message=f"Computed and stored: fact({data.n})",
            result=result
        )

    async def compute_fibonacci(self, data: FibRequest) -> CalculatorResponse:
        logger.info('Fibonacci service called')

        existing = await self._fib_repository.get_result(data.number)
        if existing:
            logger.info('The result of the fibonacci operation '
                        'was found in the database')
            return CalculatorResponse(
                message=f"Retrieved from database: fib({data.number})",
                result=existing.result
            )

        logger.info('Computing the result - fibonacci')
        result = self._calculate_fibonacci(data.number)

        logger.info('Inserting result into the database - fibonacci')
        await self._fib_repository.insert(data.number, result)

        logger.info('Service fibonacci ran successfully')
        return CalculatorResponse(
            message=f"Computed and stored: fib({data.number})",
            result=result
        )

    def _calculate_power(self, base: int, exponent: int) -> int:
        if exponent == 0:
            return 1

        temp = self._calculate_power(base, exponent // 2)

        if exponent % 2 == 0:
            return temp * temp
        else:
            return base * temp * temp

    @staticmethod
    def _calculate_factorial(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def _calculate_fibonacci(number: int) -> int:
        if number == 0:
            return 0
        elif number == 1:
            return 1

        a, b = 0, 1
        for _ in range(2, number + 1):
            a, b = b, a + b
        return b
