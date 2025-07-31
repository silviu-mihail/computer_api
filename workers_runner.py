import time
import multiprocessing
from shared.log_worker import start_service_log_worker


def main():
    service_names = [
        "gateway",
        "authenticator",
        "calculator"
    ]

    worker_processes = []

    try:
        for service in service_names:
            print(f"Starting log worker for service: {service}")
            p = multiprocessing.Process(target=start_service_log_worker, args=(service,))
            p.start()
            worker_processes.append(p)
            time.sleep(1)

        print("All log workers started. Press Ctrl+C to stop.")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping all log workers...")
        for p in worker_processes:
            p.terminate()
            p.join()
        print("All workers stopped.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
