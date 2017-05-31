class Info:
    def __init__(self, client_id, server):
        self.__client_id = client_id
        self.__value = 0
        self.__increment_value = 1
        self.__server = server
        self.__client_status = 'stoped'

    def get_value(self):
        return self.__value

    def get_client_id(self):
        return self.__client_id

    def get_increment_value(self):
        return self.__increment_value

    def get_server(self):
        return self.__server

    def client_status(self):
        return self.__client_status

    def update_value(self, new_value):
        if (new_value >= 100000):
            self.__value = new_value-100000
        else:
            self.__value = new_value

    def update_increment_value(self, new_increment_value):
        self.__increment_value = new_increment_value

    def update_client_status(self, new_status):
        self.__client_status = new_status
