import os
import chromadb
from tree_sitter import Parser
from tree_sitter_languages import get_language
from typing import List, Dict, Any

from config import (
    DB_PATH,
    DB_COLLECTION_NAME,
    EMBEDDING_MODEL,
    SUPPORTED_LANGUAGES,
    SUPPORTED_EXTENSIONS
)
import ollama

class CodeIndexer:
    """
    Handles parsing, chunking, and indexing of a codebase using pre-compiled tree-sitter grammars.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(name=DB_COLLECTION_NAME)

    def _get_parser_and_language(self, file_extension: str) -> tuple[Parser, Any] | tuple[None, None]:
        """Gets a parser and language object for a given file extension."""
        lang_name = SUPPORTED_LANGUAGES.get(file_extension)
        if not lang_name:
            return None, None
        
        language = get_language(lang_name)
        parser = Parser()
        parser.set_language(language)
        return parser, language

    def _extract_chunks(self, code: str, parser: Parser, language: Any) -> List[Dict[str, Any]]:
        """Extracts functions and classes as chunks using tree-sitter."""
        tree = parser.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        chunks = []
        
        query_string = """
        (function_definition) @func
        (class_definition) @class
        """
        query = language.query(query_string)
        captures = query.captures(root_node)
        
        for node, name in captures:
            chunk_type = name
            identifier_node = node.child_by_field_name('name')
            identifier = identifier_node.text.decode('utf8') if identifier_node else "unnamed"
            
            chunks.append({
                "type": chunk_type,
                "identifier": identifier,
                "content": node.text.decode('utf8'),
            })
            
        if not chunks:
            chunks.append({"type": "file", "identifier": "whole_file", "content": code})
            
        return chunks

    def index_directory(self, path: str):
        """Recursively indexes a directory."""
        print(f"🚀 Starting to index directory: {path}")
        documents, metadatas, ids = [], [], []
        doc_id = 0

        for root, _, files in os.walk(path):
            for file in files:
                if not file.endswith(SUPPORTED_EXTENSIONS):
                    continue

                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1]
                parser, language = self._get_parser_and_language(file_extension)

                if not parser:
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    chunks = self._extract_chunks(code, parser, language)
                    
                    for chunk in chunks:
                        if chunk["content"] and not chunk["content"].isspace():
                            documents.append(chunk["content"])
                            metadatas.append({
                                "file_path": file_path,
                                "type": chunk["type"],
                                "identifier": chunk["identifier"]
                            })
                            ids.append(f"doc_{doc_id}")
                            doc_id += 1

                except Exception as e:
                    print(f"⚠️ Could not process {file_path}: {e}")
        
        if not documents:
            print("No documents found to index.")
            return

        print(f"Found {len(documents)} code chunks. Generating embeddings...")
        
        embeddings = []
        for i, doc in enumerate(documents):
            if (i + 1) % 50 == 0:
                print(f"  - Embedding document {i+1}/{len(documents)}")
            embedding = ollama.embeddings(model=EMBEDDING_MODEL, prompt=doc)["embedding"]
            embeddings.append(embedding)

        print("Adding documents to the vector database...")
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("✅ Indexing complete!")
        

