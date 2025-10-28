# API Key Setup Guide

This guide will help you configure all the necessary API keys for the N8N Agent Builder with RAG Memory system.

## Required API Keys

### 1. N8N API Key (REQUIRED)

**Where to get it:**
1. Log into your n8n instance
2. Go to Settings → API
3. Click "Create API Key"
4. Copy the generated key

**How to add it:**
```bash
# In your .env file
N8N_API_KEY=your_n8n_api_key_here
N8N_BASE_URL=https://your-n8n-instance.com
```

### 2. OpenAI API Key (REQUIRED for AI features)

**Where to get it:**
1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key immediately (it won't be shown again)

**How to add it:**
```bash
# In your .env file
OPENAI_API_KEY=sk-...your_openai_key_here
```

**Pricing:** Pay-as-you-go. Typical costs:
- GPT-4: $0.03 per 1K tokens (input), $0.06 per 1K tokens (output)
- GPT-3.5-turbo: $0.001 per 1K tokens
- Embeddings: $0.0001 per 1K tokens

### 3. Vector Database (REQUIRED for RAG Memory)

Choose ONE of the following:

#### Option A: ChromaDB (Recommended for local development)
**Setup:**
- No API key needed
- Runs locally
- Free and open source

**Configuration:**
```bash
# Already configured by default
# Uses local storage in ./chroma_db directory
```

#### Option B: Pinecone (Recommended for production)
**Where to get it:**
1. Go to https://www.pinecone.io
2. Sign up for free account
3. Create a new index
4. Copy your API key from the dashboard

**Configuration:**
```bash
# In your .env file
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=your_environment_name
PINECONE_INDEX_NAME=agent-memory
```

**Pricing:**
- Free tier: 1 index, up to 100K vectors
- Paid plans start at $70/month

#### Option C: Weaviate
**Setup:**
1. Go to https://console.weaviate.cloud
2. Create a free cluster
3. Get your API key and URL

**Configuration:**
```bash
# In your .env file
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your_weaviate_key_here
```

### 4. Anthropic API Key (OPTIONAL - for Claude AI)

**Where to get it:**
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key

**Configuration:**
```bash
# In your .env file
ANTHROPIC_API_KEY=sk-ant-...your_anthropic_key_here
```

## Quick Setup Process

### Step 1: Copy the example file
```bash
cp .env.example .env
```

### Step 2: Edit the .env file
```bash
# Use your preferred editor
nano .env
# or
vim .env
# or open in VSCode
code .env
```

### Step 3: Add your keys
Replace the placeholder values with your actual API keys:

```bash
# Minimum required configuration
N8N_API_KEY=your_actual_n8n_key_here
N8N_BASE_URL=https://your-n8n-instance.com
OPENAI_API_KEY=your_actual_openai_key_here

# ChromaDB will work automatically for local development
# No additional keys needed for ChromaDB
```

### Step 4: Verify setup
```bash
python scripts/setup.py
```

## Security Best Practices

1. **Never commit .env file to git**
   - Already included in .gitignore
   - Double-check before pushing code

2. **Use environment variables in production**
   ```bash
   export N8N_API_KEY=your_key
   export OPENAI_API_KEY=your_key
   ```

3. **Rotate keys regularly**
   - Change keys every 90 days
   - Immediately rotate if compromised

4. **Use separate keys for dev/staging/prod**
   - Create different API keys for each environment
   - Use different n8n instances

5. **Set spending limits**
   - OpenAI: Set monthly spending limits in dashboard
   - Pinecone: Use free tier for testing

## Troubleshooting

### "Invalid API key" error
- Check for extra spaces or quotes in .env file
- Verify the key is active in the provider's dashboard
- Try regenerating the key

### "Connection refused" error
- Check N8N_BASE_URL is correct
- Verify n8n instance is running
- Check firewall/network settings

### "Rate limit exceeded" error
- You've hit the API provider's rate limit
- Wait before retrying
- Consider upgrading your plan

### "Module not found" error
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment if using one

## Getting Help

If you encounter issues:

1. Check the API provider's documentation
2. Verify all keys are correctly formatted
3. Review the example files in `examples/` directory
4. Check the logs in `logs/` directory

## Cost Management

To minimize costs while testing:

1. **OpenAI:**
   - Use GPT-3.5-turbo instead of GPT-4 for testing
   - Set `max_tokens` limits in config.json
   - Monitor usage in OpenAI dashboard

2. **Vector Database:**
   - Use ChromaDB locally (free)
   - Switch to Pinecone only for production

3. **n8n:**
   - Self-host for free (unlimited)
   - Or use n8n cloud free tier

## Next Steps

After setting up your API keys:

1. Run the setup script:
   ```bash
   python scripts/setup.py
   ```

2. Try the basic examples:
   ```bash
   python examples/basic_usage.py
   ```

3. Test workflow integration:
   ```bash
   python examples/workflow_integration.py
   ```

4. Start building your agents!

---

**Note:** Keep this file secure and never share your actual API keys!
