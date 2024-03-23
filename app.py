from flask import Flask, request, jsonify, render_template
import wikipedia
import requests
import re

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyA5YocXmTntv_LoGm_3ecZbHL-lIz7kmOY'
SEARCH_ENGINE_ID = 'b45dc313d50ac4cef'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_result', methods=['POST'])
def get_search_result():
    user_query = request.json.get('user_query') 
    if not user_query:
        return jsonify({'error': 'Please enter a query.'}), 400

    try:
        wiki_search_result = wikipedia.summary(user_query)
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        wiki_search_result = 'Sorry, If no result is obtained, please consider the result above.'

    try:
        google_search_result = google_search(user_query)
    except Exception as e:
        google_search_result = f'Error fetching results : {str(e)}'

    return jsonify({'wikipedia_result': wiki_search_result, 'google_result': google_search_result})

def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    data = response.json()
    search_results = []
    if 'items' in data:
        for item in data['items']:
            snippet = item.get('snippet', '')
            if not contains_date(snippet):
                search_results.append(snippet)
    return search_results

def contains_date(text):
    date_regex = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s\d{1,2},?\s\d{4})\b'
    return re.search(date_regex, text) is not None

if __name__ == '__main__':
    app.run(debug=True)
