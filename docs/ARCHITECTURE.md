# Architecture Overview

This document explains the architecture of the N8N Agent Builder with RAG Memory system.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                  (Python API / Examples)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Agent Builder                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Agent Manager│  │Memory Manager│  │Workflow Mgr  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────┐ ┌────────────────┐ ┌──────────────┐
│  N8N API Client │ │  RAG Memory    │ │ LLM Provider │
│                 │ │   System       │ │ (OpenAI/etc) │
└────────┬────────┘ └────────┬───────┘ └──────┬───────┘
         │                   │                 │
         ▼                   ▼                 ▼
┌─────────────────┐ ┌────────────────┐ ┌──────────────┐
│  n8n Instance   │ │ Vector Database│ │ LLM API      │
│  (Workflows)    │ │ (ChromaDB/etc) │ │              │
└─────────────────┘ └────────────────┘ └──────────────┘
```

## Core Modules

### 1. N8N Client (`src/n8n_client.py`)

**Purpose**: Interface with n8n API for workflow management

**Key Functions**:
- `list_workflows()`: Get all workflows
- `create_workflow(data)`: Create new workflow
- `execute_workflow(id, data)`: Execute workflow with input
- `activate_workflow(id)`: Enable workflow
- `get_executions(id)`: Get execution history

**Technology**:
- Uses `requests` library for HTTP calls
- Implements n8n REST API v1
- Handles authentication via API key

**Flow**:
```
User Request → N8NClient → HTTP API Call → n8n Instance → Response
```

### 2. RAG Memory (`src/rag_memory.py`)

**Purpose**: Semantic memory storage and retrieval using vector embeddings

**Key Functions**:
- `add_memory(content, metadata, importance)`: Store memory
- `search_memory(query, top_k)`: Semantic search
- `get_conversation_context(query)`: Get relevant context

**Technology**:
- OpenAI embeddings API (text-embedding-ada-002)
- ChromaDB for vector storage (default)
- Support for Pinecone, Weaviate, Qdrant

**Flow**:
```
Text Input → Embedding Model → Vector → Vector DB
Query → Embedding → Similarity Search → Relevant Memories
```

**RAG Process**:
1. **Indexing**:
   - Split documents into chunks
   - Generate embeddings for each chunk
   - Store vectors in database with metadata

2. **Retrieval**:
   - Convert query to embedding
   - Find similar vectors (cosine similarity)
   - Return top-k most relevant chunks

3. **Generation**:
   - Inject retrieved context into prompt
   - Send to LLM for generation
   - Return contextually-aware response

### 3. Agent Builder (`src/agent_builder.py`)

**Purpose**: Create and manage AI agents with workflows and memory

**Key Components**:

#### Agent Class
- Represents an individual AI agent
- Links to n8n workflow
- Manages agent-specific memory collection

#### AgentBuilder Class
- Factory for creating agents
- Manages multiple agents
- Coordinates workflow execution with memory

**Key Functions**:
- `create_agent()`: Create new agent with workflow
- `run_agent()`: Execute agent with memory context
- `add_agent_memory()`: Add knowledge to agent
- `search_agent_memory()`: Search agent's knowledge

**Flow**:
```
1. Create Agent → Initialize Memory Collection → Create Workflow
2. Add Knowledge → Generate Embeddings → Store in Vector DB
3. Run Agent:
   - Query → Search Memory → Retrieve Context
   - Context + Input → Execute Workflow → LLM
   - Response → Store in Memory → Return
```

## Data Flow

### Creating an Agent

```
User Code
  ↓
AgentBuilder.create_agent()
  ↓
1. Initialize Agent object
  ↓
2. Create RAGMemory instance
  ↓
3. Create n8n workflow (optional)
  ↓
4. Store agent in registry
  ↓
Return Agent
```

### Running an Agent

```
User Query
  ↓
AgentBuilder.run_agent()
  ↓
1. Search agent memory (RAG)
   ↓
   Query → Embedding → Vector Search → Top-K Results
  ↓
2. Build context from memories
  ↓
3. Execute n8n workflow
   ↓
   Workflow Input: {query, context, metadata}
   ↓
   n8n → LLM Node → Process → Response
  ↓
4. Store interaction in memory
  ↓
Return Response
```

## Memory Architecture

### Memory Item Structure

```python
{
  "id": "mem_1234567890.123",
  "content": "Information to remember",
  "metadata": {
    "type": "knowledge",
    "category": "technical",
    "timestamp": "2025-01-15T10:30:00",
    "importance": 0.8
  },
  "embedding": [0.123, -0.456, ...],  # 1536 dimensions
}
```

### Vector Database Schema

**Collection**: One per agent
- Name: `agent_{agent_name}`
- Dimensions: 1536 (OpenAI embeddings)
- Distance metric: Cosine similarity

**Indexes**:
- Vector index for similarity search
- Metadata index for filtering

## Workflow Architecture

### Workflow Template Structure

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {...}
    },
    {
      "name": "OpenAI",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "operation": "text",
        "options": {
          "temperature": 0.7,
          "maxTokens": 1000
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "OpenAI", "type": "main", "index": 0}]]
    }
  }
}
```

### Workflow Execution Flow

```
1. Trigger (Webhook/Manual)
   ↓
2. Prepare Input
   - Extract query
   - Inject context from RAG
   ↓
3. Process Nodes
   - Function nodes for data transformation
   - LLM nodes for AI processing
   ↓
4. Format Output
   ↓
5. Return Response
```

## Integration Points

### 1. LLM Integration

**Supported Providers**:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Via n8n nodes: Many others

**Integration Method**:
- Direct API calls (via n8n nodes)
- LangChain integration
- Custom function nodes

### 2. Vector Database Integration

**Supported Databases**:
- ChromaDB (local)
- Pinecone (cloud)
- Weaviate (self-hosted/cloud)
- Qdrant (self-hosted/cloud)

**Selection Logic**:
- Default: ChromaDB (no config needed)
- Production: Pinecone/Weaviate (scalable)
- Custom: Any vector DB with Python client

### 3. n8n Integration

**API Endpoints Used**:
- GET `/api/v1/workflows` - List workflows
- POST `/api/v1/workflows` - Create workflow
- PATCH `/api/v1/workflows/:id` - Update workflow
- POST `/api/v1/workflows/:id/execute` - Execute
- GET `/api/v1/executions` - Get execution history

**Authentication**:
- API key in header: `X-N8N-API-KEY`
- Configured in `.env` file

## Configuration System

### Configuration Hierarchy

1. **Environment Variables** (`.env`)
   - API keys and secrets
   - Instance URLs
   - Sensitive data

2. **Configuration File** (`config.json`)
   - Application settings
   - Model parameters
   - Feature flags

3. **Code Defaults**
   - Fallback values
   - Safe defaults

### Configuration Loading

```
Application Start
  ↓
Load .env → Environment Variables
  ↓
Load config.json → Settings Object
  ↓
Apply Defaults → Final Configuration
  ↓
Initialize Components
```

## Security Considerations

### API Key Management
- Never commit `.env` file
- Use environment variables in production
- Rotate keys regularly

### Data Privacy
- Memories stored locally by default
- Vector DB choice affects data location
- Consider encryption for sensitive data

### Access Control
- n8n API key controls workflow access
- Agent memory is isolated per collection
- No cross-agent memory access

## Scalability

### Horizontal Scaling
- Multiple n8n instances (load balancer)
- Distributed vector database (Pinecone/Weaviate)
- Separate LLM API keys per instance

### Vertical Scaling
- Increase vector DB resources
- Cache embeddings
- Optimize chunk sizes

### Performance Optimization
- Batch embedding generation
- Cache frequently accessed memories
- Async workflow execution
- Index optimization

## Error Handling

### Error Levels

1. **API Errors**
   - n8n API failures → Retry with backoff
   - LLM API failures → Fallback model
   - Vector DB failures → Local cache

2. **Validation Errors**
   - Invalid input → Clear error messages
   - Missing config → Use defaults
   - Schema errors → Type checking

3. **Runtime Errors**
   - Workflow execution failures → Log and notify
   - Memory errors → Graceful degradation
   - Network errors → Retry mechanism

## Future Enhancements

### Planned Features
- Multi-agent collaboration
- Advanced memory management (forgetting, consolidation)
- Real-time streaming responses
- Built-in monitoring dashboard
- Agent marketplace (templates)

### Extension Points
- Custom vector databases
- Custom embedding models
- Custom workflow nodes
- Plugin system

## Development Guidelines

### Adding New Features

1. **Module Structure**
   - Keep modules focused
   - Use type hints
   - Document public APIs

2. **Testing**
   - Unit tests for core logic
   - Integration tests for API calls
   - Mock external services

3. **Documentation**
   - Update README
   - Add docstrings
   - Include examples

### Code Organization

```
src/
  ├── core/          # Core functionality
  ├── integrations/  # External integrations
  ├── utils/         # Utility functions
  └── models/        # Data models
```

## Conclusion

This architecture provides:
- **Modularity**: Easy to extend and modify
- **Scalability**: Can grow with your needs
- **Flexibility**: Multiple database and LLM options
- **Simplicity**: Clear separation of concerns

For implementation details, see the source code and examples.
