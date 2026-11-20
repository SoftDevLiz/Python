# -----------------------------
# Menu items (expanded to 4 items)
# -----------------------------
menu = ['bagels', 'donuts', 'muffins', 'croissants']


# -----------------------------
# Stock dictionary
# Each item maps to how many are available
# -----------------------------
stock = {
    'bagels': 20,
    'donuts': 35,
    'muffins': 15,
    'croissants': 10
}


# -----------------------------
# Price dictionary
# Each item maps to its price per unit
# -----------------------------
price = {
    'bagels': 45,
    'donuts': 65,
    'muffins': 40,
    'croissants': 90
}


# -----------------------------
# Calculate total stock value
# -----------------------------
total_stock_value = 0

for item in menu:

    # Calculate value for each item (stock × price)
    total_item_value = stock[item] * price[item]

    # Add to running total
    total_stock_value += total_item_value


# -----------------------------
# Output final total value of all stock
# -----------------------------
print(f"\nCurrent total stock value: {total_stock_value}")
