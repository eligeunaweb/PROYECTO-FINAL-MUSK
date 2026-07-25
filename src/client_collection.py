from client import Client

class ClientCollection:
    def __init__(self, clients):
        self.clients = clients  # lista de objetos Client

    def get_client_by_id(self, id):
        for client in self.clients:
            if client.client_id == id:
                return client
        return None

    def clients_by_country(self, country):
        return [client for client in self.clients if client.country == country]