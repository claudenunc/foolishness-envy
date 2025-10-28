# How to Import Workflows into n8n

This guide shows you how to import the pre-built AI agent workflows into your n8n instance.

## Available Workflows

### 1. **Simple_AI_Chatbot.json**
Basic chatbot using GPT-3.5-turbo
- Simple webhook → OpenAI → Response
- Great for testing
- Low cost (uses GPT-3.5)

### 2. **AI_Chat_Agent_RAG.json**
Chat agent with RAG memory support
- Webhook trigger
- Context injection
- Memory storage
- GPT-4 powered

### 3. **Advanced_AI_Agent_Memory.json**
Full-featured agent with memory search
- Dynamic memory retrieval
- Conditional context loading
- Conversation tracking
- Production-ready

---

## Method 1: Import via n8n UI (Recommended)

### Step 1: Open n8n
```
http://localhost:5678
```

### Step 2: Import Workflow

1. Click the **"+"** button (top right) or go to **Workflows** menu
2. Click **"Import from File"** or **"Import from URL"**
3. Choose one of these files:
   - `workflows/Simple_AI_Chatbot.json`
   - `workflows/AI_Chat_Agent_RAG.json`
   - `workflows/Advanced_AI_Agent_Memory.json`

### Step 3: Configure OpenAI Credentials

After importing, you need to add your OpenAI API key:

1. Click on any **"OpenAI"** node in the workflow
2. Click **"Create New Credential"** (if needed)
3. Enter your OpenAI API key
4. Click **"Save"**

### Step 4: Activate Workflow

1. Toggle the **"Active"** switch (top right)
2. The workflow is now live!

### Step 5: Get Webhook URL

1. Click on the **"Webhook"** node
2. Copy the **"Production URL"** or **"Test URL"**
3. Use this URL to send requests

---

## Method 2: Import via n8n API

If you prefer automation:

```bash
# Using curl
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflows/AI_Chat_Agent_RAG.json

# Using Python
import requests
import json

with open('workflows/AI_Chat_Agent_RAG.json', 'r') as f:
    workflow = json.load(f)

response = requests.post(
    'http://localhost:5678/api/v1/workflows',
    headers={
        'X-N8N-API-KEY': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json=workflow
)

print(f"Workflow created with ID: {response.json()['id']}")
```

---

## Testing the Workflows

### Test Simple Chatbot

```bash
curl -X POST http://localhost:5678/webhook/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### Test AI Chat Agent with Context

```bash
curl -X POST http://localhost:5678/webhook/ai-chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is n8n?",
    "context": "n8n is a workflow automation tool that allows you to connect different services."
  }'
```

### Test Advanced Agent

```bash
curl -X POST http://localhost:5678/webhook/smart-agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about RAG",
    "conversationId": "user123",
    "includeContext": true,
    "maxMemories": 5
  }'
```

---

## Workflow Details

### Simple AI Chatbot

**Nodes:**
- Webhook (POST /chatbot)
- OpenAI (GPT-3.5-turbo)
- Respond

**Input:**
```json
{
  "message": "Your question here"
}
```

**Output:**
```json
{
  "response": "AI response",
  "timestamp": "2025-10-28T..."
}
```

### AI Chat Agent RAG

**Nodes:**
- Webhook (POST /ai-chat)
- Extract Input
- Build Prompt with Context
- OpenAI Chat (GPT-4)
- Format Response
- Store in Memory
- Respond

**Input:**
```json
{
  "message": "Your question",
  "context": "Optional context from memory",
  "conversationId": "optional-id"
}
```

**Output:**
```json
{
  "success": true,
  "conversationId": "user-id",
  "query": "Your question",
  "response": "AI response with context",
  "timestamp": "2025-10-28T...",
  "model": "gpt-4",
  "metadata": {
    "hasContext": true
  }
}
```

### Advanced AI Agent

**Nodes:**
- Webhook Trigger
- Parse Request
- Need Context? (conditional)
- Search Memory (RAG simulation)
- Skip Memory (alternative path)
- Merge
- Build AI Prompt
- OpenAI GPT-4
- Format Output
- Send Response
- Save to Memory

**Input:**
```json
{
  "query": "Your question",
  "conversationId": "user123",
  "agentName": "Smart Assistant",
  "maxMemories": 5,
  "includeContext": true
}
```

**Output:**
```json
{
  "success": true,
  "agent": "Smart Assistant",
  "conversationId": "user123",
  "query": "Your question",
  "response": "AI response with memory context",
  "metadata": {
    "timestamp": "2025-10-28T...",
    "model": "gpt-4",
    "memoriesUsed": 3,
    "hasContext": true,
    "contextLength": 245,
    "responseLength": 180
  }
}
```

---

## Customization Tips

### Change AI Model

In any OpenAI node, change the `model` parameter:
- `gpt-4` - Most capable, higher cost
- `gpt-4-turbo-preview` - Faster GPT-4
- `gpt-3.5-turbo` - Fast and economical

### Adjust Temperature

Lower = more focused, Higher = more creative
- `0.3` - Factual, consistent
- `0.7` - Balanced (default)
- `0.9` - Creative, varied

### Add More Context

In the "Build Prompt" nodes, modify the system prompt:
```javascript
let systemPrompt = `You are a specialized assistant for [YOUR DOMAIN].

Your expertise includes:
- Topic 1
- Topic 2
- Topic 3

Additional context: ${context}`;
```

### Connect to Real Vector Database

Replace the "Search Memory" node with actual database queries:

```javascript
// Example: Connect to Pinecone
const { Pinecone } = require('@pinecone-database/pinecone');

const pinecone = new Pinecone({
  apiKey: 'YOUR_PINECONE_KEY'
});

const index = pinecone.index('your-index');
const results = await index.query({
  vector: queryEmbedding,
  topK: 5
});

return results;
```

---

## Troubleshooting

### "Workflow not found"
- Make sure you imported the file correctly
- Check the workflow list in n8n UI

### "OpenAI credentials missing"
- Click on OpenAI node
- Add your API key
- Save the workflow

### "Webhook not responding"
- Make sure workflow is **Active**
- Use the correct webhook URL
- Check n8n execution logs

### "Context Error: node not found"
- This happens if you rename nodes
- Make sure node names match the references in Code nodes

---

## Next Steps

1. **Import** one of the workflows
2. **Configure** OpenAI credentials
3. **Activate** the workflow
4. **Test** with curl or Postman
5. **Customize** for your needs
6. **Connect** to real RAG memory (Python scripts)

## Integration with Python RAG System

To connect these workflows with the RAG memory system:

```python
from src.agent_builder import AgentBuilder

builder = AgentBuilder()

# Get context from RAG
results = builder.search_agent_memory(
    agent_name="Smart Assistant",
    query="user query",
    top_k=5
)

# Format context
context = "\n".join([r['content'] for r in results])

# Call n8n webhook with context
import requests
response = requests.post(
    'http://localhost:5678/webhook/ai-chat',
    json={
        "message": "user query",
        "context": context
    }
)

print(response.json())
```

---

**Ready to go! Import a workflow and start chatting with your AI agent!** 🚀
