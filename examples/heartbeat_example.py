import time

from calmmage_services_registry.heartbeat import start_heartbeat_thread


class App:
    def __init__(self):
        self.heartbeat_thread = start_heartbeat_thread(service_name="example_app", host="localhost", port=8002)

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
