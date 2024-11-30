import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from exa_py import Exa
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Exa API
exa_api_key = os.getenv('EXA_API')
if not exa_api_key:
    raise ValueError('EXA_API key not found. Please set it in the .env file.')

exa = Exa(api_key=exa_api_key)

@app.route('/search', methods=['POST'])
def search_content():
    # Get data from the request
    data = request.json
    
    # Validate input
    domain = data.get('domain')
    query = data.get('query')
    
    if not domain:
        return jsonify({'error': 'Please enter a URL for the Social Media platform.'}), 400
    
    if not query:
        return jsonify({'error': 'Please enter a content to search.'}), 400
    
    try:
        # Perform Exa search
        response = exa.search(
            query,
            num_results=10,
            type='keyword',
            include_domains=[domain],
        )
        
        # Transform results to a format easy for frontend to consume
        results = [
            {
                'title': result.title,
                'url': result.url
            } for result in response.results
        ]
        
        return jsonify({
            'query': query,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()