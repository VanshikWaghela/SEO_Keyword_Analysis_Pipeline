import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Example data
data = [
    ['26aa60ed-7cb7-454f-b71d-7403c39cf5c2', 'Keyword_29', 'Finance', 'South America', 'Spanish', 'Navigational', 5335, 2.32, 0.0214, 53350, 1141, 0.096, 0.299, 96, 'Medium', 15, 782, 840, 394, 132, 477, 892, 570, 856, 546, 854, 935, 398],
    ['1cfb5ea3-79ad-49e2-ae64-edbc80f88048', 'Keyword_47', 'Finance', 'Australia', 'English', 'Navigational', 4481, 8.17, 0.0145, 44810, 649, 0.0448, 0.639, 25, 'Medium', 16, 719, 803, 406, 86, 449, 882, 577, 876, 490, 893, 958, 388],
    # ... Add more rows as needed ...
]

columns = [
    "Keyword ID", "Keyword Name", "Category", "Region", "Language", "Search Intent",
    "Search Volume", "CPC (Cost Per Click)", "CTR (Click-Through Rate)", "Impressions",
    "Clicks", "Conversion Rate", "Bounce Rate", "Keyword Difficulty", "Competition Level",
    "Competitor Rank", "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023",
    "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023"
]

df = pd.DataFrame(data, columns=columns)

@app.route('/keyword/<string:keyword_name>')
def keyword_details(keyword_name):
    keyword_data = df[df['Keyword Name'].str.contains(keyword_name, case=False, na=False)]
    if keyword_data.empty:
        return jsonify({"error": f"No data found for '{keyword_name}'"}), 404

    # Fetch the category of the keyword
    category = keyword_data.iloc[0]["Category"]

    # Find other keywords in the same category (excluding the main keyword)
    suggested_keywords = df[df['Category'] == category]["Keyword Name"].tolist()
    suggested_keywords.remove(keyword_name) if keyword_name in suggested_keywords else None

    response_data = keyword_data.iloc[0].to_dict()
    response_data["suggestions"] = suggested_keywords[:5]  # Limit to 5 suggestions
    return jsonify(response_data)




@app.route('/charts/<string:keyword_name>/trends')
def keyword_trend_chart(keyword_name):
    chart_path = f"{keyword_name}_trend_chart.png"  # Define chart file path

    # Check if the chart already exists
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')

    # Fetch data for the chart
    keyword_data = df[df['Keyword Name'] == keyword_name]
    if keyword_data.empty:
        return jsonify({"error": "Keyword not found"}), 404

    # Extract data for the trend chart
    months = columns[16:]  # Monthly columns
    values = keyword_data.iloc[0, 16:].values.astype(int)

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



@app.route('/charts/<string:keyword_name>/cpc_vs_clicks')
def cpc_vs_clicks_chart(keyword_name):
    keyword_data = df[df['Keyword Name'] == keyword_name]
    if keyword_data.empty:
        return jsonify({"error": "Keyword not found"}), 404
    
    cpc = keyword_data["CPC (Cost Per Click)"].values[0]
    clicks = keyword_data["Clicks"].values[0]

    # Debugging: Print CPC and Clicks
    print(f"CPC: {cpc}, Clicks: {clicks}")

    plt.figure(figsize=(8, 6))
    plt.bar(['CPC', 'Clicks'], [cpc, clicks], color=['blue', 'orange'])
    plt.title(f"CPC vs Clicks for {keyword_name}")
    plt.ylabel("Values")
    
    chart_path = f"{keyword_name}_cpc_vs_clicks_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Debugging: Check if the file exists
    if os.path.exists(chart_path):
        print(f"Chart saved at: {chart_path}")
        return send_file(chart_path, mimetype='image/png')
    else:
        print("Error: Chart file not found")
        return jsonify({"error": "Chart file not found"}), 500

if __name__ == "__main__":
    app.run(debug=True)
