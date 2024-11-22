from dotenv import load_dotenv
import os

from langchain_community.llms import Ollama
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from github_issues_requests import fetch_github_issues
from vector_store_operations import connect_to_vector_db,load_data_to_vector_db,test_similarity_search
from rag_tools import rag_retriever_tool,note_tool


# Load environment variables
print("\n🔧 Loading environment variables...")
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')

# Initialize vector store and load GitHub issues
print("\n🔄 Initializing system components...")
try:
    # Ask user if they want to update the issues
    while True:
        update_choice = input("\n📝 Do you want to fetch new issues from GitHub? (yes/no): ").lower()
        if update_choice in ['yes', 'no']:
            break
        print("Please enter 'yes' or 'no'")
    
    if update_choice == 'yes':
        # Delete existing collection if it exists
        print("🗑️ Cleaning up existing vector store collection...")
        try:
            vector_store.delete_collection()
            print("✅ Existing collection deleted successfully!")
        except Exception as e:
            print(f"ℹ️ No existing collection to delete: {str(e)}")

        # Fetch GitHub issues
        print("\n📥 Fetching GitHub issues...")
        issuesData = fetch_github_issues(owner="langflow-ai", repo="langflow",token=github_token)
        if issuesData:
            print(f"✅ Successfully fetched {len(issuesData)} GitHub issues!")
            
            # Load issues into vector store
            vector_store = load_data_to_vector_db(issuesData)
            print("✅ Issues loaded into vector store!")
        else:
            print("⚠️ No issues fetched from GitHub")
    else:
        print("📌 Using existing issues from vector store...")
        # Connect to vector store
        vector_store = connect_to_vector_db()

except Exception as e:
    print(f"❌ Error during initialization: {str(e)}")
    raise

# Initialize Ollama LLM
print("\n🤖 Initializing Ollama LLM...")
llama3_llm=Ollama(model="llama3.1:latest")
print("✅ LLM initialized successfully!")

# Create tools for the agent
print("\n🔧 Setting up agent tools...")
git_rag_retriever_tool = rag_retriever_tool(vector_store)
tools = [git_rag_retriever_tool, note_tool]
print("✅ Agent tools configured!")

# Create a prompt template for ReAct agent
print("\n📝 Configuring agent prompt template...")
prompt = PromptTemplate.from_template("""You are a helpful AI assistant that helps users find information about GitHub issues.

You have access to the following tools:

{tools}


Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}""")

# Create the ReAct agent
print("\n🤖 Creating ReAct agent...")
agent = create_react_agent(llama3_llm, tools, prompt)

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
print("✅ Agent ready to process queries!")

print("\n🎉 System initialization complete! Ready to handle GitHub issue queries.")

test_similarity_search(vector_store)

# Interactive loop
while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    try:
        result = agent_executor.invoke({"input": question})
        print(result["output"])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
