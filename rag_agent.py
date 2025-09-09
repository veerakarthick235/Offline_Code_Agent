# rag_agent.py

import chromadb
import ollama
from typing import List, Generator

from config import DB_PATH, DB_COLLECTION_NAME, EMBEDDING_MODEL, LLM_MODEL

class RAGAgent:
    """
    An agent that uses Retrieval-Augmented Generation to answer questions about a codebase.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_collection(name=DB_COLLECTION_NAME)

    def _retrieve_context(self, query: str, n_results: int = 5) -> List[str]:
        """Retrieves relevant code chunks from the database."""
        query_embedding = ollama.embeddings(
            model=EMBEDDING_MODEL,
            prompt=query
        )["embedding"]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results["documents"][0]

    def _generate_streaming_response(self, prompt: str) -> Generator[str, None, None]:
        """Generates a streaming response from the LLM."""
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        
        for chunk in response:
            yield chunk['message']['content']

    def stream_ask(self, query: str) -> Generator[str, None, None]:
        """Handles a general query and streams the response."""
        print(f"🧠 Thinking about: {query}")
        context = self._retrieve_context(query)
        
        prompt_template = """
        You are an expert pair programmer and software architect.
        Your task is to answer a question about a codebase using the provided context.
        Be concise, accurate, and provide code examples when helpful. Format your response using Markdown.

        Here is the relevant context from the codebase:
        ---
        {context}
        ---

        Here is the user's question:
        "{query}"

        Your answer:
        """
        prompt = prompt_template.format(query=query, context="\n\n---\n\n".join(context))
        yield from self._generate_streaming_response(prompt)

    def stream_write_test(self, identifier: str) -> Generator[str, None, None]:
        """Generates a unit test for a specific function or class and streams the response."""
        print(f"🧪 Writing a test for: {identifier}")
        context = self._retrieve_context(f"the source code for the function or class named {identifier}", n_results=3)

        prompt_template = """
        You are an expert software developer specializing in testing.
        Your task is to write a simple, effective unit test for the provided code snippet using the pytest framework.
        The test should be self-contained in a single code block. Explain your test briefly after the code.

        Here is the source code to test:
        ---
        {context}
        ---

        Write a pytest unit test for the function or class '{identifier}'.

        Your response:
        """
        prompt = prompt_template.format(identifier=identifier, context="\n\n---\n\n".join(context))
        yield from self._generate_streaming_response(prompt)

    # --- Keep the old methods for CLI use if desired ---
    def ask(self, query: str):
        """Non-streaming version for CLI."""
        full_response = ""
        for chunk in self.stream_ask(query):
            print(chunk, end='', flush=True)
            full_response += chunk
        print()
        return full_response

    def write_test(self, identifier: str):
        """Non-streaming version for CLI."""
        full_response = ""
        for chunk in self.stream_write_test(identifier):
            print(chunk, end='', flush=True)
            full_response += chunk
        print()
        return full_response