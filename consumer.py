from kafka import KafkaConsumer
import json
from sqlalchemy import create_engine, text
from datetime import datetime

def create_database_connection():
    try:
        engine = create_engine('postgresql://postgres:postgres@postgres-db:5432/seo_db')
        print("Database connection established!")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def create_table(engine):
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tax_keyword_analysis (
            keyword_id VARCHAR PRIMARY KEY,
            keyword_name VARCHAR,
            category VARCHAR,
            region VARCHAR,
            language VARCHAR,
            search_intent VARCHAR,
            search_volume INTEGER,
            cpc FLOAT,
            ctr FLOAT,
            impressions INTEGER,
            clicks INTEGER,
            conversion_rate FLOAT,
            bounce_rate FLOAT,
            keyword_difficulty FLOAT,
            competition_level VARCHAR,
            competitor_rank INTEGER,
            jan_2023 INTEGER,
            feb_2023 INTEGER,
            mar_2023 INTEGER,
            apr_2023 INTEGER,
            may_2023 INTEGER,
            jun_2023 INTEGER,
            jul_2023 INTEGER,
            aug_2023 INTEGER,
            sep_2023 INTEGER,
            oct_2023 INTEGER,
            nov_2023 INTEGER,
            dec_2023 INTEGER,
            processing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            roi FLOAT GENERATED ALWAYS AS (
                (search_volume * cpc * (ctr/100) * (conversion_rate/100)) / 
                NULLIF(keyword_difficulty, 0)
            ) STORED,
            performance_score FLOAT GENERATED ALWAYS AS (
                (ctr * conversion_rate) / NULLIF(bounce_rate, 0)
            ) STORED
        )
        """
        with engine.begin() as conn:
            conn.execute(text(create_table_sql))
        print("Table created/verified successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
        raise

def insert_data(engine, data):
    try:
        insert_sql = """
        INSERT INTO tax_keyword_analysis (
            keyword_id, keyword_name, category, region, language, 
            search_intent, search_volume, cpc, ctr, impressions,
            clicks, conversion_rate, bounce_rate, keyword_difficulty,
            competition_level, competitor_rank, 
            jan_2023, feb_2023, mar_2023, apr_2023, may_2023,
            jun_2023, jul_2023, aug_2023, sep_2023, oct_2023,
            nov_2023, dec_2023, processing_time
        )
        VALUES (
            :keyword_id, :keyword_name, :category, :region, :language,
            :search_intent, :search_volume, :cpc, :ctr, :impressions,
            :clicks, :conversion_rate, :bounce_rate, :keyword_difficulty,
            :competition_level, :competitor_rank,
            :jan_2023, :feb_2023, :mar_2023, :apr_2023, :may_2023,
            :jun_2023, :jul_2023, :aug_2023, :sep_2023, :oct_2023,
            :nov_2023, :dec_2023, :processing_time
        )
        ON CONFLICT (keyword_id) DO UPDATE SET
            processing_time = EXCLUDED.processing_time
        """
        
        data['processing_time'] = datetime.now()
        
        with engine.begin() as conn:
            conn.execute(text(insert_sql), data)
        print(f"Data inserted for keyword: {data['keyword_name']}")
    except Exception as e:
        print(f"Error inserting data: {e}")
        print(f"Problematic data: {data}")
        raise

def start_consumer():
    try:
        engine = create_database_connection()
        create_table(engine)
        
        consumer = KafkaConsumer(
            'tax_keyword_data',
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='tax_keyword_consumer_group'
        )
        
        print("Started consuming messages...")
        
        for message in consumer:
            try:
                data = message.value
                print(f"\nReceived message: {data}")
                insert_data(engine, data)
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

    except Exception as e:
        print(f"Consumer error: {e}")

if __name__ == "__main__":
    start_consumer()