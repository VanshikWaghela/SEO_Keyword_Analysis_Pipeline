from kafka import KafkaProducer
import json
import pandas as pd
import time

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def get_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=json_serializer,
            batch_size=16384,
            buffer_memory=33554432
        )
        print("Successfully connected to Kafka!")
        return producer
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        raise

def produce_messages():
    try:
        print("Reading CSV file in chunks...")
        chunk_size = 1000
        chunk_number = 0
        
        for chunk in pd.read_csv('/app/data/final_dataset.csv', chunksize=chunk_size):
            chunk_number += 1
            print(f"Processing chunk {chunk_number}")
            
            producer = get_kafka_producer()
            
            for index, row in chunk.iterrows():
                try:
                    data = {
                        'keyword_id': str(row['Keyword ID']),
                        'keyword_name': str(row['Keyword Name']),
                        'category': str(row['Category']),
                        'region': str(row['Region']),
                        'language': str(row['Language']),
                        'search_intent': str(row['Search Intent']),
                        'search_volume': int(row['Search Volume']) if pd.notna(row['Search Volume']) else 0,
                        'cpc': float(row['CPC (Cost Per Click)']) if pd.notna(row['CPC (Cost Per Click)']) else 0.0,
                        'ctr': float(row['CTR (Click-Through Rate)']) if pd.notna(row['CTR (Click-Through Rate)']) else 0.0,
                        'impressions': int(row['Impressions']) if pd.notna(row['Impressions']) else 0,
                        'clicks': int(row['Clicks']) if pd.notna(row['Clicks']) else 0,
                        'conversion_rate': float(row['Conversion Rate']) if pd.notna(row['Conversion Rate']) else 0.0,
                        'bounce_rate': float(row['Bounce Rate']) if pd.notna(row['Bounce Rate']) else 0.0,
                        'keyword_difficulty': float(row['Keyword Difficulty']) if pd.notna(row['Keyword Difficulty']) else 0.0,
                        'competition_level': str(row['Competition Level']),
                        'competitor_rank': int(row['Competitor Rank']) if pd.notna(row['Competitor Rank']) else 0,
                        'jan_2023': int(row['Jan 2023']) if pd.notna(row['Jan 2023']) else 0,
                        'feb_2023': int(row['Feb 2023']) if pd.notna(row['Feb 2023']) else 0,
                        'mar_2023': int(row['Mar 2023']) if pd.notna(row['Mar 2023']) else 0,
                        'apr_2023': int(row['Apr 2023']) if pd.notna(row['Apr 2023']) else 0,
                        'may_2023': int(row['May 2023']) if pd.notna(row['May 2023']) else 0,
                        'jun_2023': int(row['Jun 2023']) if pd.notna(row['Jun 2023']) else 0,
                        'jul_2023': int(row['Jul 2023']) if pd.notna(row['Jul 2023']) else 0,
                        'aug_2023': int(row['Aug 2023']) if pd.notna(row['Aug 2023']) else 0,
                        'sep_2023': int(row['Sep 2023']) if pd.notna(row['Sep 2023']) else 0,
                        'oct_2023': int(row['Oct 2023']) if pd.notna(row['Oct 2023']) else 0,
                        'nov_2023': int(row['Nov 2023']) if pd.notna(row['Nov 2023']) else 0,
                        'dec_2023': int(row['Dec 2023']) if pd.notna(row['Dec 2023']) else 0
                    }
                    producer.send('tax_keyword_data', value=data)
                    
                    if index % 100 == 0:
                        print(f"Processed {index} rows in chunk {chunk_number}")
                        
                except Exception as e:
                    print(f"Error processing row {index} in chunk {chunk_number}: {e}")
                    continue
            
            producer.flush()
            print(f"Completed chunk {chunk_number}")
            time.sleep(1)
            
    except FileNotFoundError:
        print("Error: final_dataset.csv file not found in /app/data/ directory")
    except Exception as e:
        print(f"Error in produce_messages: {str(e)}")
        print("Detailed error:")
        import traceback
        traceback.print_exc()

def main():
    while True:
        try:
            produce_messages()
            print("Completed processing all chunks. Waiting before next run...")
            time.sleep(30)
        except KeyboardInterrupt:
            print("Stopping producer...")
            break
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()