class Client:
    def __init__(self, client_id):
        self.__client_id = client_id
        self.__value = 0
        self.__status = 'connected'

    def get_client_value(self):
        return self.__value

    def get_client_id(self):
        return self.__client_id

    def status(self):
        return self.__status

    def update_client_value(self, new_value):
        self.__value = new_value

    def update_status(self, new_status):
        self.__status = new_status
