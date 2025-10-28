# Quick Start Guide

Get up and running with N8N Agent Builder in 5 minutes!

## Step 1: Copy the Environment File

```bash
cp .env.example .env
```

## Step 2: Add Your n8n API Key

Open the `.env` file in your favorite editor:

```bash
nano .env
# or
vim .env
# or
code .env
```

Add your n8n API key:

```bash
N8N_API_KEY=your_n8n_api_key_here
N8N_BASE_URL=https://your-n8n-instance.com
```

### How to Get Your n8n API Key

1. Log into your n8n instance (self-hosted or cloud)
2. Click on your profile icon (top right)
3. Go to **Settings** → **API**
4. Click **"Create API Key"**
5. Copy the generated key
6. Paste it into your `.env` file

### n8n Instance URL

- **Self-hosted**: Usually `http://localhost:5678` or your server URL
- **n8n Cloud**: `https://[your-workspace].app.n8n.cloud`

## Step 3: Add Your OpenAI API Key (for AI features)

Get your OpenAI API key from: https://platform.openai.com/api-keys

Add it to `.env`:

```bash
OPENAI_API_KEY=sk-...your_key_here
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Run the Setup

```bash
python scripts/setup.py
```

## Step 6: Test It Out

```bash
python examples/basic_usage.py
```

## That's It!

You're ready to build AI agents with n8n and RAG memory!

## Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **Configure advanced settings**: [API_KEY_SETUP.md](API_KEY_SETUP.md)
3. **Try workflow integration**: `python examples/workflow_integration.py`
4. **Create your first agent**:

```python
from src.agent_builder import AgentBuilder

builder = AgentBuilder()
agent = builder.create_agent(
    name="My First Agent",
    description="A helpful AI assistant",
    initial_instructions="You are a friendly assistant."
)

# Add knowledge
builder.add_agent_memory(
    agent_name="My First Agent",
    content="Important information for the agent to remember",
    importance=1.0
)
```

## Troubleshooting

### "N8N_API_KEY not provided"
- Make sure you copied `.env.example` to `.env`
- Make sure you added your actual API key (not the placeholder)
- No quotes needed around the key

### "Connection refused" to n8n
- Make sure your n8n instance is running
- Check the N8N_BASE_URL is correct
- For self-hosted, verify the port (usually 5678)

### "Module not found"
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## Need Help?

- Full documentation: [README.md](README.md)
- API key setup: [API_KEY_SETUP.md](API_KEY_SETUP.md)
- n8n docs: https://docs.n8n.io

Happy building!
