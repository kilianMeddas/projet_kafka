from connect import connect_to_db
from collections import defaultdict
from datetime import datetime

def revenue_day_month():
    db = connect_to_db()
    tickets = db['shop']
    
    revenue_by_day = defaultdict(float)  # Revenue by day
    revenue_by_month = defaultdict(float)  # Revenue by month

    for ticket in tickets.find():
        ticket_date = ticket.get('date')
        total_revenue = ticket.get('total', 0)  # Collect total revenue
        
        if ticket_date:
            
            date_obj = datetime.strptime(ticket_date, '%Y-%m-%d %H:%M:%S')
            
            # 1. Calculate revenue by day
            day = date_obj.strftime('%Y-%m-%d')
            revenue_by_day[day] += total_revenue
            
            # 2. Calculate revenue by month
            month = date_obj.strftime('%Y-%m')
            revenue_by_month[month] += total_revenue

    return revenue_by_day, revenue_by_month
