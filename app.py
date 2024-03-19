from flask import Flask, request, jsonify, render_template
import wikipedia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_result', methods=['POST'])
def get_search_result():
    user_query = request.json.get('user_query') 
    if not user_query:
        return jsonify({'result': 'Please enter a query.'}), 400

    try:
        search_result = wikipedia.summary(user_query)
        return jsonify({'result': search_result})
    except wikipedia.exceptions.PageError:
        return jsonify({'result': 'Sorry, no results found.'}), 404
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:3]) 
        return jsonify({'result': f'Multiple possible results found. Please be more specific. For example: {options}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
