
from connect import connect_to_db
from collections import defaultdict
from datetime import datetime

def collect_sales_by_day_and_month():
    db = connect_to_db() # connection to database 
    tickets = db['shop']
    
    sales_by_day = defaultdict(int)  # for sales by day
    sales_by_month = defaultdict(int)  # for sales by month
    for ticket in tickets.find():
        ticket_date = ticket.get('date')
        if ticket_date:
            # Format de la date
            date_obj = datetime.strptime(ticket_date, '%Y-%m-%d %H:%M:%S')
            
            # 1. Sales by day
            day = date_obj.strftime('%Y-%m-%d')
            sales_by_day[day] += 1
            
            # 2. Sales by month
            month = date_obj.strftime('%Y-%m')
            sales_by_month[month] += 1

    return sales_by_day, sales_by_month
