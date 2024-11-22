from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.vectorstores.pgvector import PGVector
from dotenv import load_dotenv
import os


def connect_to_vector_db():
    """
    Establishes connection to the vector database using PGVector.
    Uses Ollama embeddings with mxbai-embed-large model.
    Returns a configured vector store instance.
    """
    try:
        print("\n🔄 Initializing vector database connection...")
        # Load environment variables
        load_dotenv()
        
        # Get connection string from environment
        CONNECTION_STRING = os.getenv('DATABASE_URL')
        if not CONNECTION_STRING:
            raise ValueError("DATABASE_URL environment variable not found")
            
        print("🔧 Configuring Ollama embeddings...")
        # Initialize embeddings with specific model
        ollama_embeddings = OllamaEmbeddings(
            model="mxbai-embed-large:latest",
        )
        
        print("🔌 Connecting to PostgreSQL vector store...")
        # Create and return vector store instance
        vector_store = PGVector(
            connection_string=CONNECTION_STRING,
            embedding_function=ollama_embeddings,
            collection_name="github_issues"
        )
        print("✅ Vector store connection established successfully!")
        return vector_store
    except Exception as e:
        print(f"❌ Error connecting to vector store: {str(e)}")
        raise


def load_data_to_vector_db(githubIssuesData):
    """
    Loads GitHub issues data into the vector database.
    Args:
        githubIssuesData: List of GitHub issues to be stored
    Returns:
        Configured vector store with loaded data
    """
    try:
        print("\n📥 Loading GitHub issues into vector database...")
        # Load environment variables and get connection string
        load_dotenv()
        CONNECTION_STRING = os.getenv('DATABASE_URL')
        
        # Initialize embeddings
        ollama_embeddings = OllamaEmbeddings(
            model="mxbai-embed-large:latest"
        )
        
        # Create vector store from documents
        vector_store = PGVector.from_documents(
            documents=githubIssuesData,
            embedding=ollama_embeddings,
            collection_name="github_issues",
            connection_string=CONNECTION_STRING,
        )
        print(f"✅ Successfully loaded {len(githubIssuesData)} issues into vector store!")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading data to vector store: {str(e)}")
        raise


def test_similarity_search(vector_store, query="What are the issues related to Langflow crashing?", k=2):
    """
    Performs a semantic similarity search on stored GitHub issues.
    Args:
        vector_store: Initialized PGVector store instance
        query: Search query string
        k: Number of results to return (default: 2)
    Returns:
        List of similar documents with their scores
    """
    try:
        print(f"\n🔍 Performing similarity search for query: '{query}'")
        print(f"📊 Retrieving top {k} results...")
        
        # Perform similarity search
        results = vector_store.similarity_search_with_score(query, k=k)
        
        # Print results in a formatted way
        print("\n📝 Search Results:")
        for doc, score in results:
            print("\n-------------------")
            print(f"Score: {score:.4f}")
            print(f"Title: {doc.metadata.get('title', 'N/A')}")
            print(f"URL: {doc.metadata.get('url', 'N/A')}")
            print(f"State: {doc.metadata.get('state', 'N/A')}")
            print(f"Created: {doc.metadata.get('created_at', 'N/A')}")
            print("Content Preview:", doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)
        
        return results
    except Exception as e:
        print(f"❌ Error during similarity search: {str(e)}")
        raise
