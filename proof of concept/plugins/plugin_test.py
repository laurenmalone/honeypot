class Plugin:

    PORT = "8080"

    def __init__(self):
        print("plugin Test init")

    def run(self, passed_socket):
        print("plugin running")

    def get_port(self):
        return self.PORT