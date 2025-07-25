from shared.logger import setup_logger

logger = setup_logger(
    service_name='authenticator',
    log_file='authenticator_log.jsonl'
)
