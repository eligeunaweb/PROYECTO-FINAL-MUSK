from src.sale import Sale

class SalesCollection:
    def __init__(self, sales):
        self.sales = sales  # lista de objetos Sale

    def sales_by_client(self, client_id):
        return [sale for sale in self.sales if sale.client_id == client_id]

    def total_amount_by_client(self, client_id):
        ventas = self.sales_by_client(client_id)
        return sum(sale.amount for sale in ventas)

    def total_amount_by_category(self, category):
        return sum(sale.amount for sale in self.sales if sale.category == category)

    def average_sale_by_client(self, client_id):
        ventas = self.sales_by_client(client_id)
        if len(ventas) == 0:
            return 0
        return self.total_amount_by_client(client_id) / len(ventas)