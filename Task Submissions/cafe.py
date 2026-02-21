menu = ['bagels', 'donuts']

stock = {
    'bagels': 20,
    'donuts': 35
}

price = {
    'bagels': 120,
    'donuts': 65,
}

total_stock_value = 0

for item in menu:
    total_item_value = stock[item] * price[item]
    total_stock_value += total_item_value

print(total_stock_value)