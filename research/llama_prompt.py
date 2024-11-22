from langchain.prompts import PromptTemplate

# Custom prompt template for llama3
LLAMA_PROMPT = """You are a helpful AI assistant that helps users find information about GitHub issues. You have access to tools that can help you retrieve and analyze GitHub issues.

TOOLS:
------
You have access to the following tools:

{tools}

TASK:
-----
Use the above tools to help answer the user's question. Follow these rules:
1. First understand what information you need to answer the question
2. Use the appropriate tool to get that information
3. Provide a clear and concise answer based on the information retrieved

USER QUESTION:
-------------
{input}

YOUR RESPONSE:
-------------
Let me help you with that.

{agent_scratchpad}"""

def get_llama_prompt():
    """Returns a prompt template suitable for llama3"""
    return PromptTemplate.from_template(LLAMA_PROMPT)
