class Plugin:

    PORT = "8080"
    ORM = {"table": {
        'tableName': "test_table1",
        "column": {
            "name": "ip",
            "type": "TEXT"
        }
    }}

    def __init__(self):
        print("plugin Test init")

    def run(self, passed_socket):
        print("plugin running")

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM