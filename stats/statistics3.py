from connect import connect_to_db

def collect_revenue_by_product():
    db = connect_to_db() # Connet to database
    tickets = db['shop'] # Collection
    revenue_by_product = {}

    for ticket in tickets.find():
        for article in ticket.get('articles', []):
            product = article.get('Product')
            price = article.get('price')
            quantity = article.get('quantity')
            revenue = price * quantity  # Revenue of this article

            if product in revenue_by_product:
                revenue_by_product[product] += revenue
            else:
                revenue_by_product[product] = revenue

    return revenue_by_product
