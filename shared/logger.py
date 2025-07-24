import logging
import redis
import json
from logging.handlers import RotatingFileHandler


class RedisLogHandler(logging.Handler):
    def __init__(self, redis_host="localhost", redis_port=6379, channel="log-stream"):
        super().__init__()
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.channel = channel

    def emit(self, record):
        try:
            log_data = {
                "level": record.levelname,
                "message": record.getMessage(),
                "time": self.formatTime(record),
                "module": record.module,
                "service": record.name
            }
            self.redis.publish(self.channel, json.dumps(log_data))
        except Exception as e:
            print(f"[!] Redis log publish failed: {e}")


def setup_logger(service_name: str, log_file="service.log") -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        json.dumps({
            "service": service_name,
            "level": "%(levelname)s",
            "message": "%(message)s",
            "time": "%(asctime)s",
            "module": "%(module)s"
        })
    )

    # File log
    file_handler = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Redis log
    redis_handler = RedisLogHandler()
    redis_handler.setFormatter(formatter)
    logger.addHandler(redis_handler)

    return logger