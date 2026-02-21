# 🤖 Offline Code Agent v2.0

**The Privacy-First AI Pair Programmer**

------------------------------------------------------------------------

## 🌟 The Problem

In modern enterprise environments, data privacy is a massive concern.
Developers often want to use AI tools like ChatGPT, but pasting
proprietary company code into cloud-based LLMs poses a **critical
security risk**.

------------------------------------------------------------------------

## 💡 The Solution

**Offline Code Agent** is a full-stack, RAG-powered (Retrieval-Augmented
Generation) application that runs **100% locally**.\
It uses a vector database to understand your entire codebase and
provides an AI assistant that can:

-   Answer architectural questions\
-   Detect bugs and vulnerabilities\
-   Generate unit tests\
-   Refactor code intelligently

All **without a single byte of data leaving your machine**.

------------------------------------------------------------------------

## 🔥 Key Features

### 💬 Chat with Memory

Ask high-level questions about your codebase. The agent maintains
conversational context for natural follow-ups.

### 🪄 Smart Refactor

Automatically improves code readability, structure, and performance
based on Clean Code principles.

### 🐞 Bug Hunter

Performs static analysis to detect: - Logic errors\
- Security risks (XSS, Directory Traversal, Injection patterns)\
- Code smells

### 🧪 Unit Test Generator

Creates robust `pytest` test suites with edge-case coverage, reducing
manual testing effort.

### ⚡ High Performance

Optimized for local inference using lightweight LLMs such as: - Phi-3\
- Llama 3\
- TinyLlama

------------------------------------------------------------------------

## 🛠️ Technical Stack

  Layer          Technology
  -------------- -----------------------------------
  Backend        Flask (Python)
  LLM Runtime    Ollama (Local Models)
  Vector DB      ChromaDB (Persistent)
  Code Parsing   Tree-sitter (AST-based)
  Frontend       HTML5, CSS3, Vanilla JS (Dark UI)
  Architecture   RAG + Local Inference

------------------------------------------------------------------------

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   Ollama running locally

------------------------------------------------------------------------

### Installation

#### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/veerakarthick235/Offline_Code_Agent.git
cd Offline_Code_Agent
```

#### 2️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

#### 3️⃣ Index Your Codebase

``` bash
python main.py index "/path/to/your/codebase"
```

#### 4️⃣ Launch the Dashboard

``` bash
python app.py
```

Open the UI at:

👉 http://127.0.0.1:5001

------------------------------------------------------------------------

## 🔐 Why This Matters

-   🛡️ **Data Privacy:** Zero cloud dependency\
-   🏢 **Enterprise Ready:** Safe for proprietary code\
-   ⚙️ **Developer Productivity:** Faster debugging, refactoring, and
    testing\
-   🧠 **AI Engineering Skills:** Demonstrates RAG, local LLMs, AST
    parsing, and vector search

------------------------------------------------------------------------

## 👨‍💻 About the Developer

**Veera Karthick**\
3rd-Year B.Tech -- Artificial Intelligence & Data Science\
Shree Venkateshwara Hi-Tech Engineering College

I build **privacy-first AI systems** focused on real-world developer
productivity and secure local inference.

-   🌐 Portfolio: https://veerakarthick.in/\
-   💻 GitHub: https://github.com/veerakarthick235\
-   🔗 LinkedIn: https://www.linkedin.com/in/karthickkumar-s-b04a10348/

------------------------------------------------------------------------

## 📄 License

Distributed under the **MIT License**.\
See `LICENSE` for more information.
