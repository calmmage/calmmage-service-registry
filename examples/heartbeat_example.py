import time

from loguru import logger

from calmmage_services_registry.heartbeat import start_heartbeat_thread, is_heartbeat_env_initialized


class App:
    def __init__(self):
        if is_heartbeat_env_initialized():
            self.heartbeat_thread = start_heartbeat_thread()
        else:
            logger.warning("Heartbeat environment is not initialized. Skipping heartbeat.")
            self.heartbeat_thread = None

    def run(self):
        print("App is running...")
        while True:
            # Simulating some work
            time.sleep(5)
            print("App is still running...")


if __name__ == "__main__":
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print("App is shutting down...")
