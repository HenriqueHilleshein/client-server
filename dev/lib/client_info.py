class Info:
    def __init__(self,client_id,server):
        self.client_id = client_id
        self.value = 0
        self.increase_value = 1
        self.server=server

    def get_value(self):
        return self.value

    def get_client_id(self):
        return self.client_id

    def get_increase_value(self):
        return self.increase_value

    def get_server(self):
        return self.server

    def update_value(self,new_value):
        if (new_value>=100000):
            self.value = new_value-100000
        else:
            self.value = new_value

    def update_increase_value(self,new_increase_value):
        self.increase_value = new_increase_value


