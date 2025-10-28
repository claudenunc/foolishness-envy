# N8N Agent Builder with RAG Memory

An advanced AI agent builder that uses n8n API for workflow automation and RAG (Retrieval Augmented Generation) for intelligent memory management.

## Features

- **N8N Integration**: Full API integration with n8n for workflow automation
- **RAG Memory System**: Semantic memory using vector embeddings for context-aware responses
- **Agent Builder**: Create and manage multiple AI agents with different capabilities
- **Workflow Templates**: Pre-built workflow templates for common use cases
- **Vector Database Support**: ChromaDB, Pinecone, Weaviate, and Qdrant
- **Multi-Model Support**: Works with OpenAI GPT, Anthropic Claude, and more

## Project Structure

```
foolishness-envy/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── n8n_client.py            # N8N API client
│   ├── rag_memory.py            # RAG memory system
│   └── agent_builder.py         # Agent builder and manager
├── templates/
│   └── workflows/               # N8N workflow templates
│       ├── basic_chat_agent.json
│       ├── data_processing_agent.json
│       └── research_agent.json
├── examples/
│   ├── basic_usage.py           # Basic usage examples
│   └── workflow_integration.py  # Workflow integration examples
├── scripts/
│   └── setup.py                 # Setup script
├── config.json                  # Application configuration
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies (optional)
├── API_KEY_SETUP.md            # Detailed API key setup guide
└── README.md                    # This file
```

## Quick Start

### 1. Prerequisites

- Python 3.8+
- n8n instance (self-hosted or cloud)
- OpenAI API key
- Git

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/claudenunc/foolishness-envy.git
cd foolishness-envy

# Install dependencies
pip install -r requirements.txt

# Run setup
python scripts/setup.py
```

### 3. Configure API Keys

**IMPORTANT:** See [API_KEY_SETUP.md](API_KEY_SETUP.md) for detailed instructions.

Quick setup:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

Minimum required:
```bash
N8N_API_KEY=your_n8n_api_key_here
N8N_BASE_URL=https://your-n8n-instance.com
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run Examples

```bash
# Basic usage
python examples/basic_usage.py

# Workflow integration
python examples/workflow_integration.py
```

## Usage

### Creating an Agent

```python
from src.agent_builder import AgentBuilder

# Initialize builder
builder = AgentBuilder()

# Create an agent
agent = builder.create_agent(
    name="Customer Support",
    description="Helpful customer support agent",
    initial_instructions="You are a friendly customer support agent."
)
```

### Adding Knowledge to Agent Memory

```python
# Add memory
builder.add_agent_memory(
    agent_name="Customer Support",
    content="Our refund policy allows returns within 30 days.",
    metadata={"category": "policy"},
    importance=0.9
)
```

### Searching Agent Memory

```python
# Search memory
results = builder.search_agent_memory(
    agent_name="Customer Support",
    query="What is the refund policy?",
    top_k=5
)

for result in results:
    print(result['content'])
```

### Working with N8N Workflows

```python
from src.n8n_client import N8NClient

# Initialize client
client = N8NClient()

# List workflows
workflows = client.list_workflows()

# Execute workflow
result = client.execute_workflow(
    workflow_id="123",
    data={"query": "Hello, world!"}
)
```

### Creating Agent with Workflow

```python
import json

# Load workflow template
with open("templates/workflows/basic_chat_agent.json") as f:
    template = json.load(f)

# Create agent with workflow
agent = builder.create_agent(
    name="Smart Assistant",
    description="AI assistant with workflow",
    workflow_template=template
)

# Activate workflow
builder.n8n_client.activate_workflow(agent.workflow_id)
```

## RAG Memory System

The RAG (Retrieval Augmented Generation) system provides semantic memory using vector embeddings:

### How It Works

1. **Content Embedding**: Text is converted to vector embeddings using OpenAI
2. **Vector Storage**: Embeddings stored in vector database (ChromaDB, Pinecone, etc.)
3. **Semantic Search**: Query embeddings matched against stored vectors
4. **Context Retrieval**: Relevant memories retrieved based on similarity
5. **Augmented Generation**: Retrieved context used to enhance AI responses

### Configuration

Edit `config.json` to customize RAG settings:

```json
{
  "rag_settings": {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "top_k_results": 5,
    "similarity_threshold": 0.7,
    "embedding_dimensions": 1536
  }
}
```

### Vector Database Options

- **ChromaDB** (Default): Local, no API key needed
- **Pinecone**: Cloud-based, scalable
- **Weaviate**: Open-source, self-hosted or cloud
- **Qdrant**: High-performance, self-hosted or cloud

## N8N Workflow Templates

### Basic Chat Agent
Simple conversational agent with memory retrieval.

**Features:**
- Webhook trigger
- Context injection from RAG memory
- OpenAI integration
- JSON response

### Data Processing Agent
Agent for analyzing and processing data.

**Features:**
- Input validation
- Data transformation
- AI analysis
- Formatted output

### Research Agent
Research agent with web search capabilities.

**Features:**
- Query extraction
- Research planning
- Results synthesis
- Comprehensive output

## Configuration

### Application Settings (config.json)

```json
{
  "agent_settings": {
    "max_iterations": 10,
    "timeout_seconds": 300,
    "retry_attempts": 3,
    "default_model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "n8n_settings": {
    "workflow_check_interval": 5,
    "max_concurrent_workflows": 5,
    "webhook_timeout": 30
  },
  "memory_settings": {
    "max_conversation_history": 50,
    "memory_decay_factor": 0.95,
    "importance_threshold": 0.5
  }
}
```

### Environment Variables (.env)

See [API_KEY_SETUP.md](API_KEY_SETUP.md) for complete details.

## Advanced Features

### Custom Workflow Creation

```python
# Create custom workflow
workflow_data = {
    "name": "My Custom Workflow",
    "nodes": [...],
    "connections": {...}
}

workflow = client.create_workflow(workflow_data)
```

### Memory Importance Scoring

```python
# Add memory with importance score
builder.add_agent_memory(
    agent_name="My Agent",
    content="Critical information",
    importance=1.0  # High importance
)
```

### Metadata Filtering

```python
# Search with metadata filter
results = builder.search_agent_memory(
    agent_name="My Agent",
    query="search query",
    filter_metadata={"category": "technical"}
)
```

## Best Practices

1. **API Key Security**
   - Never commit .env file
   - Use environment variables in production
   - Rotate keys regularly

2. **Memory Management**
   - Use importance scores to prioritize memories
   - Clean up old/irrelevant memories periodically
   - Set appropriate chunk sizes

3. **Workflow Design**
   - Keep workflows modular
   - Use error handling nodes
   - Test workflows before activation

4. **Cost Optimization**
   - Use GPT-3.5-turbo for testing
   - Set token limits
   - Monitor API usage

## Troubleshooting

### Common Issues

1. **"Invalid API key"**
   - Check .env file format
   - Verify key is active
   - No extra spaces or quotes

2. **"Connection refused"**
   - Verify n8n instance is running
   - Check N8N_BASE_URL
   - Check network/firewall

3. **"Module not found"**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+)

4. **Memory search returns no results**
   - Verify embeddings are generated
   - Check similarity threshold
   - Ensure memories are added

See [API_KEY_SETUP.md](API_KEY_SETUP.md) for more troubleshooting tips.

## API Reference

### N8NClient

```python
client = N8NClient(api_key, base_url)
client.list_workflows()
client.get_workflow(workflow_id)
client.create_workflow(workflow_data)
client.execute_workflow(workflow_id, data)
client.activate_workflow(workflow_id)
```

### RAGMemory

```python
memory = RAGMemory(collection_name)
memory.add_memory(content, metadata, importance)
memory.search_memory(query, top_k, filter_metadata)
memory.get_memory(memory_id)
memory.delete_memory(memory_id)
```

### AgentBuilder

```python
builder = AgentBuilder()
builder.create_agent(name, description, workflow_template)
builder.get_agent(name)
builder.list_agents()
builder.run_agent(agent_name, input_data)
builder.add_agent_memory(agent_name, content, metadata)
builder.search_agent_memory(agent_name, query)
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:

1. Check the [API_KEY_SETUP.md](API_KEY_SETUP.md) guide
2. Review examples in `examples/` directory
3. Check n8n documentation: https://docs.n8n.io
4. Open an issue on GitHub

## Acknowledgments

- n8n for workflow automation platform
- OpenAI for language models and embeddings
- ChromaDB for vector database
- LangChain for AI framework components

---

**Built with Claude Code** - AI-powered development assistant

For more information about n8n: https://n8n.io
For OpenAI API: https://platform.openai.com
For ChromaDB: https://www.trychroma.com