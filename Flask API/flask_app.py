import os
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from sqlalchemy import create_engine, text
import traceback
from sqlalchemy.engine import Row
matplotlib.use('Agg')
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
            keyword_data = [dict(row._mapping) for row in result][0]
            
            # Fetch category and suggested keywords
            category = keyword_data["category"]
            suggestions = connection.execute(text("""
                SELECT keyword_name FROM tax_keyword_analysis
                WHERE category = :category AND keyword_name != :keyword_name
                LIMIT 5
            """), {"category": category, "keyword_name": keyword_name}).fetchall()

            keyword_data["suggestions"] = [row._mapping["keyword_name"] for row in suggestions]
            
            # Update search volume
            updated_search_volume = keyword_data["search_volume"] + 1
            connection.execute(text("""
                UPDATE tax_keyword_analysis
                SET search_volume = :updated_search_volume
                WHERE keyword_name = :keyword_name
            """), {"updated_search_volume": updated_search_volume, "keyword_name": keyword_name})
            connection.commit()
            return jsonify(keyword_data)
    except Exception as e:
        error_message = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": "Internal Server Error", "details": error_message}), 500
    
@app.route('/charts/<string:keyword_name>/trends')
def keyword_trend_chart(keyword_name):
    # Define chart directory and file path
    chart_dir = 'charts'  # The directory where charts will be saved
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)  # Create the directory if it doesn't exist
    print(f"Chart directory checked/created: {chart_dir}")

    chart_path = os.path.join(chart_dir, f"{keyword_name}_trend_chart.png")  # Full path to save the chart
    print(f"Chart path set to: {chart_path}")

    # Check if the chart already exists
    if os.path.exists(chart_path):
        print(f"Chart already exists for {keyword_name}, sending the existing chart.")
        return send_file(chart_path, mimetype='image/png')

    try:
        # Fetch monthly trend data from the database
        print(f"Fetching data for keyword: {keyword_name}")
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT * FROM tax_keyword_analysis WHERE keyword_name = :keyword_name
            """), {"keyword_name": keyword_name}).fetchone()

            if not result:
                print(f"Keyword not found: {keyword_name}")
                return jsonify({"error": "Keyword not found"}), 404

            print(f"Data fetched for {keyword_name}: {result}")

            months = [
                "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023",
                "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023"
            ]
            
            # Extracting the values from the fetched result
            # Assuming that the months data starts from index 12 to 23 (based on the given tuple structure)
            values = result[12:24]  # Adjust according to your database schema

            # Check if values are empty or invalid
            if not values or len(values) != len(months):
                print(f"Invalid data for all months for keyword: {keyword_name}")
                return jsonify({"error": "Invalid data for all months"}), 400

            # Debugging output to the terminal
            print(f"Months: {months}")
            print(f"Values: {values}")

            # Generate and save the chart
            print(f"Generating chart for {keyword_name}")
            plt.figure(figsize=(12, 6))
            plt.plot(months, values, marker='o', label=f"Trend for {keyword_name}")
            plt.title(f"Monthly Trend for {keyword_name}")
            plt.xlabel("Months")
            plt.ylabel("Search Volume")
            plt.grid(True)
            plt.xticks(rotation=45)  # Rotate month labels for better readability
            plt.legend()

            try:
                plt.savefig(chart_path)
                print(f"Chart saved to {chart_path}")
            except Exception as e:
                print(f"Error saving chart for {keyword_name}: {str(e)}")
                return jsonify({"error": "Failed to save chart"}), 500

            plt.close()  # Close the plot to free up memory
            print(f"Chart closed after saving.")

            # Check if the file was saved
            if not os.path.exists(chart_path):
                print(f"Chart file was not saved for {keyword_name}")
                return jsonify({"error": "Failed to save chart"}), 500

            print(f"Chart generated and saved for {keyword_name}")
            # Return the chart as a response
            return send_file(chart_path, mimetype='image/png')

    except Exception as e:
        # Print unexpected errors and send the error response
        print(f"Unexpected error occurred while generating chart for {keyword_name}: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
    
@app.route('/charts/<string:keyword_name>/cpc_vs_clicks/')
@app.route('/charts/<string:keyword_name>/')
def cpc_vs_clicks_chart(keyword_name):
    print(f"Fetching CPC vs Clicks chart for keyword: {keyword_name}")

    try:
        with engine.connect() as connection:
            print("Checking/creating chart directory.")
            os.makedirs("charts", exist_ok=True)

            # Query for monthly search volumes explicitly
            query = """
                SELECT 
                    jan_2023 AS January,
                    feb_2023 AS February,
                    mar_2023 AS March,
                    apr_2023 AS April,
                    may_2023 AS May,
                    jun_2023 AS June,
                    jul_2023 AS July,
                    aug_2023 AS August,
                    sep_2023 AS September,
                    oct_2023 AS October,
                    nov_2023 AS November,
                    dec_2023 AS December
                FROM tax_keyword_analysis
                WHERE keyword_name = :keyword_name
            """
            print("Executing query...")
            result = connection.execute(text(query), {"keyword_name": keyword_name}).fetchone()

            if not result:
                print("Query returned no data.")
                return jsonify({"error": "No data found for keyword in 2023"}), 404

            print(f"Query result: {result}")

            # Map result to months
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            search_volume = [value or 0 for value in result]  # Use 0 if data is None

            print(f"Monthly search volume: {search_volume}")

            # Create bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(months, search_volume, color='skyblue', edgecolor='black')

            # Add labels and title
            plt.title(f"Monthly Search Volume for {keyword_name} (2023)")
            plt.xlabel("Month")
            plt.ylabel("Search Volume")
            plt.xticks(rotation=45)

            # Define chart path
            chart_path = f"charts/{keyword_name}_search_volume_chart.png"
            print(f"Chart path: {chart_path}")

            # Save chart
            print("Saving the chart...")
            plt.savefig(chart_path)
            plt.close()
            print("Chart saved and closed.")

            # Return chart
            if os.path.exists(chart_path):
                print("Chart file exists. Sending response...")
                return send_file(chart_path, mimetype='image/png')
            else:
                print(f"Chart file not found at: {chart_path}")
                return jsonify({"error": "Chart file not found"}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
