import redis
import json
import time


def start_service_log_worker(
        service_name: str,
        redis_host='localhost',
        redis_port=6379,
        log_file=None
):
    stream_name = f'log-{service_name}'
    consumer_group = f'{service_name}-worker'
    consumer_name = f'{service_name}-worker-1'
    log_file = log_file or f'{service_name}_log.jsonl'

    r = redis.Redis(host=redis_host, port=redis_port, db=0)

    try:
        r.xgroup_create(stream_name, consumer_group, id='0-0', mkstream=True)
    except redis.exceptions.ResponseError as e:
        if 'BUSYGROUP' not in str(e):
            raise

    print(f'[*] Worker started for service: {service_name}, '
          f'writing to: {log_file}')

    while True:
        try:
            entries = r.xreadgroup(
                groupname=consumer_group,
                consumername=consumer_name,
                streams={stream_name: '>'},
                count=10,
                block=5_000
            )

            for stream, messages in entries:
                for msg_id, data in messages:
                    decoded_data = {k.decode(): v.decode()
                                    for k, v in data.items()}

                    with open(log_file, 'a') as file:
                        file.write(json.dumps(decoded_data) + '\n')

                    r.xack(stream_name, consumer_group, msg_id)
        except Exception as e:
            print(f'[!] Worker error for {service_name}: {e}')
            time.sleep(5)
