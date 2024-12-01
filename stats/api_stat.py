from flask import Flask, jsonify
from statistics import collect_total_revenue
from statistics2 import collect_average_revenue
from statistics3 import collect_revenue_by_product
from statistics4 import collect_sales_by_day_and_month
from statistics5 import revenue_day_month

app = Flask(__name__)

@app.route("/stats", methods=["GET"])
def get_all_stats():
    try:
        revenue = collect_total_revenue()  # Get total revenue
        average = collect_average_revenue()  # Get average revenue
        revenue_by_product = collect_revenue_by_product() #Get revenue by product
        sales = collect_sales_by_day_and_month() #get the sales by day and month
        revenue_dM = revenue_day_month()
        stats = {
            "total revenue": revenue,
            "average revenue": average,
            "revenue by product": revenue_by_product,
            "sales by day and month": sales,
            "revenue by day and month": {
                "by day": dict(revenue_dM[0]),
                "by month": dict(revenue_dM[1])
            }
        }

        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
