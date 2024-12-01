from connect import connect_to_db

# Function to calculate the average revenue
def collect_average_revenue():
    db = connect_to_db()
    tickets = db['shop']  # MongoDB collection
    total_rev = 0
    count = 0

    # Iterate through each document (ticket) in the collection
    for ticket in tickets.find({}, {'total': 1}):
        total_rev += ticket.get('total', 0)  # Correct usage of .get() on each document
        count += 1

    return total_rev / count if count > 0 else 0
