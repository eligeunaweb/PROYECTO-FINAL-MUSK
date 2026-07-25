import json
import pandas as pd
from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from src.functional_utils import filter_sales_by_category, filter_sales_by_client, get_amounts

# Leer clientes desde JSON
with open("../data/clients.json", "r") as f:
    clients_data = json.load(f)

# Crear objetos Client
clients = [Client(c["client_id"], c["name"], c["country"], c["signup_date"]) for c in clients_data]

# Leer ventas desde CSV con Pandas
df = pd.read_csv("../data/sales.csv")

# Crear objetos Sale
sales = [Sale(row["sale_id"], row["client_id"], row["product"], row["category"], row["amount"], row["date"]) for _, row in df.iterrows()]

# Crear colecciones
client_col = ClientCollection(clients)
sales_col = SalesCollection(sales)

# Cálculo 1 - Total de clientes
total_clients = len(clients)

# Cálculo 2 - Total de ventas
total_sales = len(sales)

print("Total clientes:", total_clients)
print("Total ventas:", total_sales)

# Cálculo 3 - Total ingresos por cliente
clients_info = []
for client in clients:
    total_spent = sales_col.total_amount_by_client(client.client_id)
    sale_count = len(sales_col.sales_by_client(client.client_id))
    average_sale = sales_col.average_sale_by_client(client.client_id)
    clients_info.append({
        "client_id": client.client_id,
        "name": client.name,
        "total_spent": round(total_spent, 2),
        "sale_count": sale_count,
        "average_sale": round(average_sale, 2)
    })

print("Clientes info:", clients_info)

# Cálculo 6 - Cliente con mayor gasto por país
top_client_by_country = {}
countries = set(client.country for client in clients)

for country in countries:
    clients_in_country = client_col.clients_by_country(country)
    top_client = max(clients_in_country, key=lambda c: sales_col.total_amount_by_client(c.client_id))
    top_client_by_country[country] = top_client.name

print("Top cliente por país:", top_client_by_country)

# Cálculo 7 - Total de ventas por categoría con Pandas
sales_by_category = df.groupby("category")["amount"].sum().round(2).to_dict()

print("Ventas por categoría:", sales_by_category)

# Cálculo 8 - Cliente con más ventas en una categoría
def top_client_in_category(category):
    filtered = filter_sales_by_category(sales, category)
    if not filtered:
        return None
    client_counts = {}
    for sale in filtered:
        client_counts[sale.client_id] = client_counts.get(sale.client_id, 0) + 1
    top_id = max(client_counts, key=lambda k: client_counts[k])
    return client_col.get_client_by_id(top_id).name

top_in_electronics = top_client_in_category("Electronics")
print("Top cliente en Electronics:", top_in_electronics)

# Cálculo 9 - Clientes que superan gasto mínimo de 500€
umbral = 500
high_spending_clients = []
for client in clients:
    total = sales_col.total_amount_by_client(client.client_id)
    if total > umbral:
        high_spending_clients.append(client.name)

print("Clientes con gasto > 500€:", high_spending_clients)

# Cálculo 10 - Ventas acumuladas mes a mes
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("month")["amount"].sum().round(2).to_dict()

print("Ventas mensuales:", monthly_sales)

# Cálculo 10 - Ventas acumuladas mes a mes
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("month")["amount"].sum().round(2).to_dict()

print("Ventas mensuales:", monthly_sales)

# Generar informe JSON final
informe = {
    "summary": {
        "total_clients": total_clients,
        "total_sales": total_sales,
        "total_revenue": round(df["amount"].sum(), 2)
    },
    "clients": clients_info,
    "top_client_by_country": top_client_by_country,
    "sales_by_category": sales_by_category,
    "high_spending_clients": high_spending_clients,
    "monthly_sales": monthly_sales
}

# Guardar el JSON
with open("../data/report.json", "w") as f:
    json.dump(informe, f, indent=4)

print("Informe generado correctamente en ../data/report.json")
