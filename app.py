from flask import Flask, render_template, request, Response, jsonify
from rag_agent import RAGAgent
import json

app = Flask(__name__)
agent = RAGAgent()

@app.route('/')
def index():
    return render_template('index.html')

def stream_helper(generator):
    """Helper to stream data to the client."""
    for chunk in generator:
        yield f"data: {json.dumps({'content': chunk})}\n\n"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    return Response(stream_helper(agent.stream_chat(data.get('query'))), mimetype='text/event-stream')

@app.route('/refactor', methods=['POST'])
def refactor():
    data = request.json
    return Response(stream_helper(agent.stream_refactor(data.get('identifier'))), mimetype='text/event-stream')

@app.route('/bughunt', methods=['POST'])
def bughunt():
    data = request.json
    return Response(stream_helper(agent.stream_bug_hunt(data.get('identifier'))), mimetype='text/event-stream')

@app.route('/test', methods=['POST'])
def test():
    data = request.json
    return Response(stream_helper(agent.stream_write_test(data.get('identifier'))), mimetype='text/event-stream')

@app.route('/clear', methods=['POST'])
def clear():
    agent.clear_history()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
