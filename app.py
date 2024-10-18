from flask import Flask, render_template, request
import json
# Import the previously created functions for retrieving and processing papers
from research import research_papers

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    papers = []
    if request.method == 'POST':
        query = request.form.get('query')  # Get the query from the form
        if query:  # Check if the query is not empty
            papers = research_papers(query, max_results=5)  # Fetch research papers
    return render_template('index.html', papers=papers)


if __name__ == "__main__":
    app.run(debug=True)
