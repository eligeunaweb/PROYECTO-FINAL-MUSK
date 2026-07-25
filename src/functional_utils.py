def filter_sales_by_category(sales, category):
    return list(filter(lambda s: s.category == category, sales))

def filter_sales_by_client(sales, client_id):
    return list(filter(lambda s: s.client_id == client_id, sales))

def get_amounts(sales):
    return list(map(lambda s: s.amount, sales))