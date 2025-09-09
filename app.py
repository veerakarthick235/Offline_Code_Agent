# app.py

from flask import Flask, render_template, request, Response
from rag_agent import RAGAgent
import json

app = Flask(__name__)
agent = RAGAgent()

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handles the 'ask' action from the UI."""
    data = request.json
    query = data.get('query')
    if not query:
        return Response(json.dumps({'error': 'Query cannot be empty.'}), status=400, mimetype='application/json')

    def stream():
        for chunk in agent.stream_ask(query):
            # SSE format: "data: {json_string}\n\n"
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    
    return Response(stream(), mimetype='text/event-stream')

@app.route('/test', methods=['POST'])
def test():
    """Handles the 'write_test' action from the UI."""
    data = request.json
    identifier = data.get('identifier')
    if not identifier:
        return Response(json.dumps({'error': 'Identifier cannot be empty.'}), status=400, mimetype='application/json')

    def stream():
        for chunk in agent.stream_write_test(identifier):
            # SSE format: "data: {json_string}\n\n"
            yield f"data: {json.dumps({'content': chunk})}\n\n"

    return Response(stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Note: The 'main.py' file's 'run' command will execute this.
    app.run(debug=True, port=5001)
