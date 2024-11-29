# SEO Keyword Analysis Pipeline

## Overview
The **SEO Keyword Analysis Pipeline** is a comprehensive data processing pipeline designed to analyze and visualize keyword performance for SEO optimization. It integrates multiple components like data ingestion, processing, and visualization, enabling real-time insights and decision-making.

## Features
- **Data Ingestion:** Uses Kafka for real-time keyword data ingestion.
- **Data Processing:** Leverages Apache Spark for scalable and efficient processing.
- **Visualization:** Grafana dashboards provide real-time insights into keyword performance metrics.
- **Flask API:** A lightweight API to serve processed data and visualize charts.
- **Browser Extension:** Captures user interactions and feeds data into the pipeline.

## Project Structure
### Key Components
- **`Flask API/`:**
  - Contains Flask-based backend files to handle requests and visualize data.
  - Files: `app.py`, `flask_app.py`, `index.html`, `analyze_data.py`.

- **`extension/`:**
  - A browser extension for capturing and transmitting user interactions.

- **`docker-compose.yml`:**
  - Configures and manages the project’s Docker containers.

- **`grafana/`:**
  - Provisioning files for Grafana dashboards and PostgreSQL as a data source.

- **`producer.py` & `consumer.py`:**
  - Kafka producer and consumer scripts for real-time data ingestion.


## Prerequisites
1. **Docker**  
   Ensure Docker is installed and running.
2. **Python 3.12.4**  
   Install Python along with the dependencies in `requirements.txt`.
3. **Kafka & Spark**  
   Required for data ingestion and processing.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/SEO_Keyword_Analysis_Pipeline.git
   cd SEO_Keyword_Analysis_Pipeline
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Run the Flask API:
   ```bash
   cd Flask\ API
   python flask_app.py
   ```

4. Access the Grafana dashboard at:
   ```
   http://localhost:3000
   ```

## Usage
### Flask API
- API endpoints serve processed keyword data.
- Visualizations such as bar charts and heatmaps are generated dynamically.

### Browser Extension
- Collects user input to collect the keyword and sends it to the pipeline.
- Also show you the analysis of the keyword on your browser.

### Grafana Dashboard
- Displays keyword performance metrics like:
  - **Search Volume**
  - **CTR (%)**
  - **Conversion Rate**
  - **Performance Score**

## Future Improvements
- Enhance keyword scoring algorithms.
- Add more visualizations for better insights.
- Extend browser extension functionality.
