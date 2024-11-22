# GitInspector 🔍

GitInspector is an intelligent GitHub issue analysis tool that combines the power of RAG (Retrieval-Augmented Generation) with LLM capabilities to provide smart insights and answers about GitHub issues.

## 🌟 Features

- **Real-time GitHub Issue Fetching**: Fetch latest issues from any GitHub repository
- **Smart Vector Storage**: Efficiently stores and indexes issue data using vector embeddings
- **Interactive Issue Updates**: Choose when to update your local issue database
- **Intelligent Query Processing**: Uses RAG to provide context-aware responses about issues
- **LLM Integration**: Powered by Ollama for natural language understanding and generation

## 🛠️ Technologies Used

- **Python**: Core programming language
- **LangChain**: Framework for building LLM applications
- **Ollama**: Local LLM integration (llama3.1 model)
- **GitHub API**: For fetching repository issues
- **Vector Database**: For efficient storage and retrieval of issue data
- **dotenv**: For secure environment variable management

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (optional):
   ```bash
   export GITHUB_TOKEN=your_github_token
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## 💡 Usage

1. When you start the application, you'll be prompted to choose whether to fetch new issues
2. Choose 'yes' to update the database with fresh issues
3. Choose 'no' to use existing issues from the vector store
4. Use natural language queries to ask questions about the issues

## Demo Video

Check out this video to see the tool in action:<br>

https://github.com/user-attachments/assets/f0c63bb7-e4f0-4794-bc32-0aca896845db


## 🔧 Components

- `main.py`: Main application entry point
- `github_issues_requests.py`: GitHub API integration
- `vector_store_operations.py`: Vector database operations
- `rag_tools.py`: RAG implementation and tools

## 📝 Note

Make sure you have proper GitHub API access and tokens configured for full functionality.

## 🤝 Contributing

Feel free to contribute to this project by submitting issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
