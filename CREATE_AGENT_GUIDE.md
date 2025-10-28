# How to Create Your First AI Agent

Since n8n is running on your Windows machine, you need to run the agent creation script **locally** where n8n is accessible.

## Quick Start (Windows)

### Option 1: Using PowerShell Script (Easiest)

```powershell
# In PowerShell, navigate to the project directory
cd C:\path\to\foolishness-envy

# Run the PowerShell script
.\create_agent.ps1
```

This script will:
- ✅ Check if n8n is running
- ✅ Verify Python is installed
- ✅ Install required dependencies
- ✅ Create your AI agent with workflow
- ✅ Add knowledge to the agent's memory

### Option 2: Using Python Directly

```powershell
# Make sure you're in the project directory
cd C:\path\to\foolishness-envy

# Install dependencies
pip install python-dotenv requests openai chromadb langchain langchain-openai

# Run the script
python create_agent_local.py
```

## Prerequisites

Before running the script, make sure:

1. ✅ **n8n is running**
   - Your Docker container should be running
   - Access http://localhost:5678 in your browser

2. ✅ **`.env` file is configured**
   - Should contain your API keys
   - Already configured with your keys!

3. ✅ **Python 3.8+ is installed**
   - Check with: `python --version`

## What the Script Does

The script will create an AI agent that includes:

### 1. n8n Workflow
- Creates a workflow in your n8n instance
- Sets up webhook trigger
- Configures OpenAI node for AI responses
- Links to RAG memory system

### 2. Agent Configuration
- **Name**: "Smart Assistant"
- **Description**: Intelligent AI assistant with RAG memory
- **Memory Collection**: Dedicated vector database

### 3. Knowledge Base
The agent comes pre-loaded with knowledge about:
- Its own identity and capabilities
- n8n workflow automation
- RAG (Retrieval Augmented Generation)
- Python programming
- System architecture

### 4. RAG Memory System
- Semantic search using vector embeddings
- Context-aware responses
- Long-term conversation memory

## After Creation

Once the agent is created, you can:

### 1. View in n8n
```
http://localhost:5678
```
Look for workflow: **"Smart Assistant Workflow"**

### 2. Test the Agent

#### From Python:
```python
from src.agent_builder import AgentBuilder

builder = AgentBuilder()

# Search agent's memory
results = builder.search_agent_memory(
    agent_name="Smart Assistant",
    query="What can you tell me about n8n?"
)

for result in results:
    print(result['content'])
```

#### From n8n:
1. Open the workflow in n8n
2. Click "Execute Workflow"
3. Or use the webhook URL to send requests

### 3. Add More Knowledge

```python
from src.agent_builder import AgentBuilder

builder = AgentBuilder()

# Add new knowledge
builder.add_agent_memory(
    agent_name="Smart Assistant",
    content="Your custom knowledge here",
    metadata={"category": "custom"},
    importance=0.9
)
```

## Troubleshooting

### "Cannot connect to n8n"
- Make sure Docker container is running
- Check: `docker ps | grep n8n`
- Restart if needed: `docker restart n8n`

### "N8N_API_KEY not found"
- Make sure `.env` file exists
- Check it contains: `N8N_API_KEY=your_key_here`

### "OpenAI API error"
- Verify OPENAI_API_KEY in `.env`
- Check API key is valid at https://platform.openai.com/api-keys

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`
- Or run: `pip install python-dotenv requests openai chromadb langchain`

## What Happens Behind the Scenes

1. **Script connects to n8n API**
   - Uses your N8N_API_KEY
   - Connects to http://localhost:5678

2. **Creates workflow from template**
   - Loads `templates/workflows/basic_chat_agent.json`
   - Posts to n8n API
   - Gets back workflow ID

3. **Initializes RAG memory**
   - Creates vector collection
   - Uses ChromaDB locally (no cloud needed)

4. **Adds knowledge base**
   - Converts text to embeddings using OpenAI
   - Stores in vector database
   - Enables semantic search

5. **Activates workflow**
   - Makes workflow live in n8n
   - Ready to receive requests

## Next Steps

After creating your agent:

1. **Explore the n8n workflow**
   - Open http://localhost:5678
   - View the workflow nodes
   - Customize as needed

2. **Test the memory system**
   - Run: `python examples/basic_usage.py`
   - Try different queries

3. **Add custom knowledge**
   - Use `builder.add_agent_memory()`
   - Build your knowledge base

4. **Create more agents**
   - Modify the script
   - Create specialized agents
   - Different workflows for different tasks

5. **Integrate with your apps**
   - Use the webhook URL
   - Call from other services
   - Build automation workflows

## Example: Custom Agent

```python
from src.agent_builder import AgentBuilder
import json

builder = AgentBuilder()

# Load a different template
with open("templates/workflows/research_agent.json") as f:
    template = json.load(f)

# Create specialized agent
researcher = builder.create_agent(
    name="Research Assistant",
    description="Specialized in research and analysis",
    workflow_template=template,
    initial_instructions="You are a research assistant specializing in finding and analyzing information."
)

# Add domain-specific knowledge
builder.add_agent_memory(
    agent_name="Research Assistant",
    content="I specialize in academic research, data analysis, and information synthesis.",
    importance=1.0
)

print(f"Created: {researcher.name}")
print(f"Workflow: {researcher.workflow_id}")
```

## Support

If you encounter issues:

1. Check n8n logs in Docker
2. Review `.env` file configuration
3. Verify all API keys are valid
4. Check Python dependencies are installed

For more help:
- Read: [README.md](README.md)
- Review: [API_KEY_SETUP.md](API_KEY_SETUP.md)
- Check: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

**Ready to create your agent? Run the script and let's go!** 🚀
