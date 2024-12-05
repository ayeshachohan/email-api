import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Path to the email folder
EMAIL_FOLDER = os.path.join(os.path.dirname(__file__), 'email_folder')

@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        # Get query parameters
        limit = int(request.args.get('limit', 10))  # Default to 10 emails
        start_index = int(request.args.get('start', 0))  # Optional start index
        
        # List all JSON files in the email folder
        email_files = [f for f in os.listdir(EMAIL_FOLDER) if f.endswith('.json')]
        
        # Sort files to ensure consistent order
        email_files.sort()
        
        # Apply start index and limit
        email_files = email_files[start_index:start_index + limit]
        
        # Read and parse email files
        emails = []
        for filename in email_files:
            file_path = os.path.join(EMAIL_FOLDER, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    email_data = json.load(file)
                    emails.append({
                        'filename': filename,
                        'data': email_data
                    })
            except json.JSONDecodeError:
                # Skip files that can't be parsed
                print(f"Error parsing {filename}")
                continue
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        
        return jsonify({
            'total_emails': len(emails),
            'emails': emails
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)