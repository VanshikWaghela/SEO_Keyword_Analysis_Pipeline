from sqlalchemy import create_engine, text
import pandas as pd
import time
import numpy as np

def analyze_keyword_data():
    try:
        engine = create_engine('postgresql://postgres:postgres@postgres-db:5432/seo_db')
        print("Connecting to database...")
        
        # Basic Stats Query
        basic_stats_query = """
        SELECT 
            COUNT(*) as total_keywords,
            COUNT(DISTINCT category) as unique_categories,
            COUNT(DISTINCT region) as unique_regions,
            COUNT(DISTINCT language) as unique_languages,
            COUNT(DISTINCT search_intent) as unique_intents,
            ROUND(CAST(AVG(CAST(search_volume AS numeric)) AS numeric), 2) as avg_search_volume,
            ROUND(CAST(AVG(CAST(ctr AS numeric)) AS numeric), 2) as avg_ctr,
            ROUND(CAST(AVG(CAST(conversion_rate AS numeric)) AS numeric), 2) as avg_conversion_rate
        FROM tax_keyword_analysis;
        """
        
        # Category Performance Query
        category_query = """
        SELECT 
            category,
            COUNT(*) as keyword_count,
            ROUND(CAST(AVG(CAST(search_volume AS numeric)) AS numeric), 2) as avg_volume,
            ROUND(CAST(AVG(CAST(ctr AS numeric)) AS numeric), 2) as avg_ctr,
            ROUND(CAST(AVG(CAST(conversion_rate AS numeric)) AS numeric), 2) as avg_conversion
        FROM tax_keyword_analysis
        GROUP BY category
        ORDER BY avg_volume DESC;
        """
        
        # Regional Performance Query
        regional_query = """
        SELECT 
            region,
            language,
            COUNT(*) as keyword_count,
            ROUND(CAST(AVG(CAST(search_volume AS numeric)) AS numeric), 2) as avg_volume,
            ROUND(CAST(AVG(CAST(ctr AS numeric)) AS numeric), 2) as avg_ctr
        FROM tax_keyword_analysis
        GROUP BY region, language
        ORDER BY avg_volume DESC;
        """
        
        # Search Intent Analysis Query
        intent_query = """
        SELECT 
            search_intent,
            COUNT(*) as keyword_count,
            ROUND(CAST(AVG(CAST(conversion_rate AS numeric)) AS numeric), 2) as avg_conversion,
            ROUND(CAST(AVG(CAST(ctr AS numeric)) AS numeric), 2) as avg_ctr
        FROM tax_keyword_analysis
        GROUP BY search_intent
        ORDER BY avg_conversion DESC;
        """
        
        # Top Keywords Query
        top_keywords_query = """
        SELECT 
            keyword_name,
            category,
            region,
            search_intent,
            search_volume,
            CAST(CAST(ctr AS numeric) AS numeric(10,2)) as ctr,
            CAST(CAST(conversion_rate AS numeric) AS numeric(10,2)) as conversion_rate,
            CAST(CAST(keyword_difficulty AS numeric) AS numeric(10,2)) as difficulty
        FROM tax_keyword_analysis
        ORDER BY CAST(search_volume AS numeric) DESC
        LIMIT 10;
        """
        
        # Language Performance Query
        language_query = """
        SELECT 
            language,
            COUNT(*) as keyword_count,
            ROUND(CAST(AVG(CAST(search_volume AS numeric)) AS numeric), 2) as avg_volume,
            ROUND(CAST(AVG(CAST(ctr AS numeric)) AS numeric), 2) as avg_ctr
        FROM tax_keyword_analysis
        GROUP BY language
        ORDER BY avg_volume DESC;
        """

        
        # Execute queries and print results with better formatting
        print("\n=== Basic Statistics ===")
        basic_stats = pd.read_sql(basic_stats_query, engine)
        print(basic_stats.to_string(index=False))
        
        print("\n=== Category Performance ===")
        category_stats = pd.read_sql(category_query, engine)
        print(category_stats.to_string(index=False))
        
        print("\n=== Regional Performance ===")
        regional_stats = pd.read_sql(regional_query, engine)
        print(regional_stats.to_string(index=False))
        
        print("\n=== Search Intent Analysis ===")
        intent_stats = pd.read_sql(intent_query, engine)
        print(intent_stats.to_string(index=False))
        
        print("\n=== Top Keywords ===")
        top_keywords = pd.read_sql(top_keywords_query, engine)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(top_keywords.to_string(index=False))
        
        print("\n=== Language Performance ===")
        language_stats = pd.read_sql(language_query, engine)
        print(language_stats.to_string(index=False))
        
        
        
        # Summary Statistics
        print("\n=== Summary Statistics ===")
        summary_stats = {
            'Total Keywords': basic_stats['total_keywords'].iloc[0],
            'Average CTR': f"{basic_stats['avg_ctr'].iloc[0]}%",
            'Average Conversion Rate': f"{basic_stats['avg_conversion_rate'].iloc[0]}%",
            'Top Categories': category_stats['category'].head(3).tolist(),
            'Top Regions': regional_stats['region'].head(3).tolist(),
            'Best Performing Languages': language_stats['language'].head(3).tolist()
        }
        print("\nKey Insights:")
        for key, value in summary_stats.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Detailed error information:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    while True:
        analyze_keyword_data()
        print("\nWaiting 10 seconds before next analysis...")
        time.sleep(10)