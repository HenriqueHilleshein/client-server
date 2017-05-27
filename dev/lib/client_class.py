class Client:
    def __init__(self,client_id):
        self.client_id = client_id
        self.value = 0


    def get_client_value(self):
        return self.value

    def get_client_id(self):
        return self.client_id

    def update_client_value(self,new_value):
        self.value = new_value


