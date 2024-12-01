# stats.py

from connect import connect_to_db

# Total des ventes
def collect_total_revenue():
    db = connect_to_db()
   
    tickets = db['shop']  # la collection
    total_revenue = 0

    # Additioner le 'total' de chaque ticket
    for ticket in tickets.find({}, {'total': 1}):
        total_revenue += ticket.get('total', 0)

    return total_revenue

