import logging
import redis
import json
from datetime import datetime, UTC


class RedisStreamLogHandler(logging.Handler):
    def __init__(self,
                 stream_name: str,
                 redis_host="localhost",
                 redis_port=6379):
        super().__init__()
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.stream_name = stream_name

    def emit(self, record):
        try:
            timestamp = self.formatter.formatTime(record) \
                if self.formatter else datetime.now(UTC)

            log_data = {
                "level": record.levelname,
                "message": record.getMessage(),
                "time": timestamp,
                "module": record.module,
                "service": record.name
            }
            self.redis.xadd(self.stream_name, log_data)
        except Exception as e:
            print(f"[!] Redis log publish failed: {e}")


def setup_logger(
        service_name: str,
        redis_host='localhost',
        redis_port=6379
) -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        json.dumps({
            "service": service_name,
            "level": "%(levelname)s",
            "message": "%(message)s",
            "time": "%(asctime)s",
            "module": "%(module)s"
        })
    )

    stream_name = f'log-{service_name}'
    redis_handler = RedisStreamLogHandler(
        stream_name,
        redis_host,
        redis_port
    )
    redis_handler.setFormatter(formatter)
    logger.addHandler(redis_handler)

    return logger
