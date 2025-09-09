# Offline Code Agent 🤖

An offline, AI-powered pair programmer that analyzes and answers questions about any codebase. Built for the **OpenAI Open Model Hackathon**.

This project is a powerful **local agent** that runs entirely on your machine, using local AI models via **Ollama** to provide deep insights into a codebase without ever needing an internet connection. It's designed to help developers quickly understand, debug, and enhance complex projects.

---

## 🚀 Features
- **Offline First**: Works completely without an internet connection after initial setup.
- **Web-Based UI**: A clean and simple web interface to interact with the agent.
- **Codebase Q&A**: Ask complex questions about the architecture, functionality, or logic of any indexed codebase.
- **Agentic Actions**: Automatically generate pytest unit tests for any function or class.
- **Syntax-Aware Indexing**: Uses **tree-sitter** to intelligently parse code, understanding functions and classes for more accurate context retrieval.
- **Local AI Powered**: Leverages local LLMs through Ollama, ensuring your code remains private.

---

## 🎬 Demo
Below is a brief demonstration of the web interface in action.


**Full Demo Video**: https://youtu.be/lB4BdRKYk-E?si=R_4GR6o_zV6qhtaq

---

## 🛠️ Setup and Installation

Follow these steps to get the **Offline Code Agent** running on your local machine.

### 1. Clone the Repository
```bash
git clone [Your GitHub Repository URL]
cd code-agent
```

### 2. Set Up the Environment

**Install Ollama**: Download and install Ollama from [ollama.com](https://ollama.com).

**Download AI Models**: Open your terminal and pull the required models.
```bash
# For reasoning and code generation
ollama pull codellama:13b

# For creating text embeddings
ollama pull nomic-embed-text
```

**Create Python Virtual Environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

---

## 👨‍💻 How to Use

Using the agent is a **two-step process**: first you index a codebase, then you run the web app to ask questions.

### Step 1: Index a Codebase
You must first "teach" the agent about a codebase. Point it to a local folder containing the source code you want to analyze. This command needs to be run only once per codebase.

```bash
python main.py index /path/to/your/codebase
```

**Example**:
```bash
# Download the Flask codebase
git clone https://github.com/pallets/flask.git

# Index it
python main.py index ./flask
```

### Step 2: Run the Web App
Once indexing is complete, start the Flask web server.

```bash
python main.py run
```

Now, open your browser and navigate to:  
👉 **http://127.0.0.1:5001** to start interacting with your agent.

---

## 🏆 Hackathon Submission

This project is submitted to the **OpenAI Open Model Hackathon** under the following category:

- **Category**: Best Local Agent
- **Explanation**: This project is a prime example of a useful, agentic application that operates with no internet access. It goes beyond simple Q&A by performing actions like generating unit tests based on its understanding of the code, acting as a true local assistant for developers in secure or offline environments.

---

## 💻 Technology Stack

- **Backend**: Python, Flask
- **AI/LLM**: Ollama (codellama:13b, nomic-embed-text)
- **Vector Database**: ChromaDB
- **Code Parsing**: py-tree-sitter
- **Frontend**: HTML, CSS, JavaScript
- **CLI**: Typer

---


