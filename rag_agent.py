import chromadb
import ollama
from typing import List, Generator, Dict

from config import DB_PATH, DB_COLLECTION_NAME, EMBEDDING_MODEL, LLM_MODEL

class RAGAgent:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(name=DB_COLLECTION_NAME)
        self.history: List[Dict[str, str]] = [] # Conversational Memory

    def _retrieve_context(self, query: str, n_results: int = 5) -> List[str]:
        """Retrieves relevant code chunks from the database."""
        try:
            query_embedding = ollama.embeddings(
                model=EMBEDDING_MODEL,
                prompt=query
            )["embedding"]

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            if not results["documents"] or not results["documents"][0]:
                return []
                
            return results["documents"][0]
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []

    def _generate_streaming_response(self, prompt: str, save_to_history: bool = True) -> Generator[str, None, None]:
        """Generates a streaming response and updates history."""
        messages = self.history + [{'role': 'user', 'content': prompt}]
        
        # Keep history manageable (last 10 messages)
        if len(messages) > 10:
            messages = messages[-10:]

        response = ollama.chat(
            model=LLM_MODEL,
            messages=messages,
            stream=True
        )
        
        full_response = ""
        for chunk in response:
            content = chunk['message']['content']
            full_response += content
            yield content
            
        if save_to_history:
            self.history.append({'role': 'user', 'content': prompt})
            self.history.append({'role': 'assistant', 'content': full_response})

    def stream_chat(self, query: str) -> Generator[str, None, None]:
        """General Q&A with memory."""
        context = self._retrieve_context(query)
        context_str = "\n\n---\n\n".join(context) if context else "No specific code found."
        
        prompt = f"""
        You are an expert pair programmer. Use the context below to answer the user's question.
        If the context isn't relevant, answer based on your general knowledge but mention that.
        
        Context from codebase:
        {context_str}
        
        User Question: {query}
        """
        yield from self._generate_streaming_response(prompt)

    def stream_refactor(self, identifier: str) -> Generator[str, None, None]:
        """Agentic Skill: Refactor Code."""
        context = self._retrieve_context(f"source code for {identifier}", n_results=1)
        code_snippet = context[0] if context else "Code not found."
        
        prompt = f"""
        TASK: Refactor the following code to improve readability, performance, and adherence to clean code principles.
        Explain your changes briefly at the end.
        
        CODE TO REFACTOR:
        ```
        {code_snippet}
        ```
        """
        # We don't save specialized tasks to general chat history to keep context clean
        yield from self._generate_streaming_response(prompt, save_to_history=False)

    def stream_bug_hunt(self, identifier: str) -> Generator[str, None, None]:
        """Agentic Skill: Bug Hunter."""
        context = self._retrieve_context(f"source code for {identifier}", n_results=1)
        code_snippet = context[0] if context else "Code not found."
        
        prompt = f"""
        TASK: Analyze the following code for potential bugs, security vulnerabilities, or logic errors.
        If no bugs are found, suggest defensive coding improvements.
        
        CODE TO ANALYZE:
        ```
        {code_snippet}
        ```
        """
        yield from self._generate_streaming_response(prompt, save_to_history=False)
    
    def stream_write_test(self, identifier: str) -> Generator[str, None, None]:
        """Agentic Skill: Write Unit Test."""
        context = self._retrieve_context(f"source code for {identifier}", n_results=1)
        code_snippet = context[0] if context else "Code not found."

        prompt = f"""
        TASK: Write a robust pytest unit test for this code. Cover edge cases if possible.
        
        CODE:
        ```
        {code_snippet}
        ```
        """
        yield from self._generate_streaming_response(prompt, save_to_history=False)
    
    def clear_history(self):
        self.history = []
