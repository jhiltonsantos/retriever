from app.tools.list_documents import list_documents
from app.tools.summarize_chunks import summarize_chunks
from app.tools.vector_search import vector_search

TOOLS = [vector_search, list_documents, summarize_chunks]
