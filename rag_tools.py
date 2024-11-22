from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import tool

def rag_retriever_tool(vector_store):
    """
    Creates a retriever tool for searching GitHub issues using vector store.
    
    Args:
        vector_store: Initialized vector store containing GitHub issues
    Returns:
        LangChain tool for semantic search over GitHub issues
    """
    print("\n🔧 Creating GitHub issues retriever tool...")
    # Configure retriever with k=3 for top 3 results
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create and return the retriever tool
    retriever_tool = create_retriever_tool(
        retriever,
        "github_search",
        "Search for information about github issues. For any questions about github issues, you must use this tool!",
    )
    print("✅ GitHub issues retriever tool created successfully!")
    return retriever_tool


@tool
def note_tool(note):
    """
    Saves a note to a local file for future reference.
    
    Args:
        note: Text content to save
    Returns:
        Confirmation message
    """
    try:
        print("\n📝 Saving note to file...")
        with open("notes.txt", "a") as f:
            f.write(f"\n---\n{note}\n")
        print("✅ Note saved successfully!")
        return "Note has been saved successfully!"
    except Exception as e:
        print(f"❌ Error saving note: {str(e)}")
        return f"Failed to save note: {str(e)}"
