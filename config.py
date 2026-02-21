LLM_MODEL = "tinyllama"
EMBEDDING_MODEL = "nomic-embed-text"


# Vector Database configuration
DB_PATH = "./chroma_db"
DB_COLLECTION_NAME = "codebase_collection"


# You can find more languages at: https://github.com/tree-sitter/tree-sitter/blob/master/docs/supported-languages.md
LANGUAGE_GRAMMAR_PATH = "build/my-languages.so"
SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go"
}


SUPPORTED_EXTENSIONS = tuple(SUPPORTED_LANGUAGES.keys())
