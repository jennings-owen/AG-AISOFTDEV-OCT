def calculate_total(items, discount_percent=0):
    """Calculates the total cost of a shopping cart with an optional discount.""" 
    total = sum(item['price'] * item['quantity'] for item in items)
    if discount_percent > 0:
        # Correctly apply the discount to the total price
        total = total - (total * (discount_percent / 100))
    return total