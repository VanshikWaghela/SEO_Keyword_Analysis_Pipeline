from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
import traceback

app = Flask(__name__)
CORS(app)

# Database connection (replace with your PostgreSQL credentials)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/seo_db")
engine = create_engine(DATABASE_URL)

@app.route('/api/keyword', methods=['POST'])
def handle_keyword():
    try:
        data = request.get_json()
        keyword = data.get('keyword')

        if not keyword:
            return jsonify({'error': 'Keyword is missing'}), 400

        with engine.connect() as connection:
            # Start a transaction block
            with connection.begin():
                # Check if the keyword exists
                result = connection.execute(text("""
                    SELECT keyword_id, search_volume
                    FROM tax_keyword_analysis
                    WHERE keyword_name = :keyword
                """), {"keyword": keyword}).fetchone()

                if result:
                    print(f"Keyword found: {keyword}, Current search volume: {result[1]}")

                    # If keyword exists, increment the search volume
                    keyword_id = result[0]  # first column: keyword_id
                    search_volume = result[1]  # second column: search_volume
                    updated_search_volume = search_volume + 1

                    print(f"Updating search volume for {keyword} from {search_volume} to {updated_search_volume}")

                    connection.execute(text("""
                        UPDATE tax_keyword_analysis
                        SET search_volume = :updated_search_volume
                        WHERE keyword_id = :keyword_id
                    """), {"updated_search_volume": updated_search_volume, "keyword_id": keyword_id})

                    # Commit the transaction to save changes
                    connection.commit()

                    # Fetch the updated search volume
                    updated_result = connection.execute(text("""
                        SELECT search_volume
                        FROM tax_keyword_analysis
                        WHERE keyword_id = :keyword_id
                    """), {"keyword_id": keyword_id}).fetchone()

                    if updated_result:
                        return jsonify({'message': f'Search Volume for "{keyword}" updated to {updated_result[0]}'}), 200
                    else:
                        return jsonify({'error': 'Error fetching updated search volume'}), 500

                else:
                    return jsonify({'message': f'Keyword "{keyword}" does not exist in the database.'}), 404

    except Exception as e:
        # Log detailed error message for debugging
        error_message = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_message)  # Log to console (you can also log to a file or external service)
        return jsonify({'error': 'Internal Server Error', 'details': error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)