import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from sqlalchemy import create_engine, text
import traceback

app = Flask(__name__)
CORS(app)

# Database connection (replace with your PostgreSQL credentials)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/seo_db")
engine = create_engine(DATABASE_URL)

@app.route('/keyword/<string:keyword_name>')
def keyword_details(keyword_name):
    try:
        with engine.connect() as connection:
            # Fetch the keyword data
            result = connection.execute(text("""
                SELECT * FROM tax_keyword_analysis WHERE keyword_name ILIKE :keyword_name
            """), {"keyword_name": f"%{keyword_name}%"}).fetchall()

            if not result:
                return jsonify({"error": f"No data found for '{keyword_name}'"}), 404
            
            # Convert the result to a dictionary
            keyword_data = [dict(row) for row in result][0]
            
            # Fetch category and suggested keywords
            category = keyword_data["category"]
            suggestions = connection.execute(text("""
                SELECT keyword_name FROM tax_keyword_analysis
                WHERE category = :category AND keyword_name != :keyword_name
                LIMIT 5
            """), {"category": category, "keyword_name": keyword_name}).fetchall()

            keyword_data["suggestions"] = [row["keyword_name"] for row in suggestions]
            
            # Update search volume
            updated_search_volume = keyword_data["search_volume"] + 1
            connection.execute(text("""
                UPDATE tax_keyword_analysis
                SET search_volume = :updated_search_volume
                WHERE keyword_name = :keyword_name
            """), {"updated_search_volume": updated_search_volume, "keyword_name": keyword_name})
            
            return jsonify(keyword_data)
    except Exception as e:
        error_message = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": "Internal Server Error", "details": error_message}), 500

@app.route('/charts/<string:keyword_name>/trends')
def keyword_trend_chart(keyword_name):
    chart_path = f"{keyword_name}_trend_chart.png"  # Define chart file path

    # Check if the chart already exists
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')

    try:
        # Fetch monthly trend data from the database
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT * FROM tax_keyword_analysis WHERE keyword_name = :keyword_name
            """), {"keyword_name": keyword_name}).fetchone()

            if not result:
                return jsonify({"error": "Keyword not found"}), 404

            months = [
                "jan_2023", "feb_2023", "mar_2023", "apr_2023", "may_2023", "jun_2023",
                "jul_2023", "aug_2023", "sep_2023", "oct_2023", "nov_2023", "dec_2023"
            ]
            values = [result[month] for month in months]

            # Generate and save the chart
            plt.figure(figsize=(12, 6))
            plt.plot(months, values, marker='o', label=f"Trend for {keyword_name}")
            plt.title(f"Monthly Trend for {keyword_name}")
            plt.xlabel("Months")
            plt.ylabel("Search Volume")
            plt.grid(True)
            plt.legend()
            plt.savefig(chart_path)
            plt.close()

            return send_file(chart_path, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
    
@app.route('/charts/<string:keyword_name>/cpc_vs_clicks')
def cpc_vs_clicks_chart(keyword_name):
    try:
        with engine.connect() as connection:
            # Fetch CPC and Clicks data
            result = connection.execute(text("""
                SELECT cpc, clicks FROM tax_keyword_analysis WHERE keyword_name = :keyword_name
            """), {"keyword_name": keyword_name}).fetchone()

            if not result:
                return jsonify({"error": "Keyword not found"}), 404

            cpc, clicks = result["cpc"], result["clicks"]

            plt.figure(figsize=(8, 6))
            plt.bar(['CPC', 'Clicks'], [cpc, clicks], color=['blue', 'orange'])
            plt.title(f"CPC vs Clicks for {keyword_name}")
            plt.ylabel("Values")

            chart_path = f"{keyword_name}_cpc_vs_clicks_chart.png"
            plt.savefig(chart_path)
            plt.close()

            if os.path.exists(chart_path):
                return send_file(chart_path, mimetype='image/png')
            else:
                return jsonify({"error": "Chart file not found"}), 500
    except Exception as e:
        error_message = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": "Internal Server Error", "details": error_message}), 500

if __name__ == "__main__":
    app.run(debug=True)
