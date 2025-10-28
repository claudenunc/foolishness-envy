#!/usr/bin/env python3
"""
Create your first AI agent on n8n
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent_builder import AgentBuilder

load_dotenv()

def main():
    """Create first AI agent"""
    print("=" * 60)
    print("Creating Your First AI Agent")
    print("=" * 60)

    # Initialize agent builder
    print("\n1. Initializing agent builder...")
    builder = AgentBuilder()

    # Load workflow template
    print("2. Loading workflow template...")
    template_path = "templates/workflows/basic_chat_agent.json"
    with open(template_path, "r") as f:
        template = json.load(f)

    # Create the agent
    print("3. Creating AI agent with workflow...")
    agent_name = "Smart Assistant"
    agent = builder.create_agent(
        name=agent_name,
        description="An intelligent AI assistant that can help with various tasks using RAG memory",
        workflow_template=template,
        initial_instructions="""You are a helpful AI assistant with access to long-term memory.
You can remember conversations and provide context-aware responses.
Be friendly, helpful, and informative."""
    )

    print(f"\n✓ Agent created: {agent.name}")
    print(f"  Description: {agent.description}")
    print(f"  Workflow ID: {agent.workflow_id}")
    print(f"  Memory Collection: {agent.memory_collection}")

    # Add some initial knowledge to the agent
    print("\n4. Adding knowledge to agent memory...")

    knowledge_items = [
        {
            "content": "I am an AI assistant built using n8n workflows and RAG memory. I can help with programming, automation, and general questions.",
            "metadata": {"type": "identity", "category": "about"},
            "importance": 1.0
        },
        {
            "content": "n8n is a workflow automation tool that allows you to connect different services and automate tasks. It's open-source and very powerful.",
            "metadata": {"type": "knowledge", "category": "n8n"},
            "importance": 0.9
        },
        {
            "content": "RAG (Retrieval Augmented Generation) is a technique that enhances AI responses by retrieving relevant information from a knowledge base before generating responses.",
            "metadata": {"type": "knowledge", "category": "ai"},
            "importance": 0.9
        },
        {
            "content": "Python is a versatile programming language great for automation, data science, web development, and AI applications.",
            "metadata": {"type": "knowledge", "category": "programming"},
            "importance": 0.8
        },
        {
            "content": "This system uses OpenAI for embeddings and language models, with ChromaDB or Pinecone for vector storage.",
            "metadata": {"type": "knowledge", "category": "technical"},
            "importance": 0.7
        }
    ]

    for i, item in enumerate(knowledge_items, 1):
        memory_id = builder.add_agent_memory(
            agent_name=agent_name,
            content=item["content"],
            metadata=item["metadata"],
            importance=item["importance"]
        )
        print(f"  ✓ Added memory {i}/{len(knowledge_items)}: {item['metadata']['category']}")

    # Activate the workflow
    print("\n5. Activating workflow...")
    try:
        builder.n8n_client.activate_workflow(agent.workflow_id)
        print("  ✓ Workflow activated")
    except Exception as e:
        print(f"  ⚠ Could not activate workflow: {e}")
        print("  You can activate it manually in the n8n UI")

    # Test the agent's memory
    print("\n6. Testing agent memory...")
    test_query = "What is n8n?"
    print(f"  Query: '{test_query}'")

    results = builder.search_agent_memory(
        agent_name=agent_name,
        query=test_query,
        top_k=3
    )

    print(f"  Found {len(results)} relevant memories:")
    for i, result in enumerate(results, 1):
        print(f"\n  {i}. {result['content'][:100]}...")
        print(f"     Category: {result['metadata'].get('category', 'N/A')}")
        print(f"     Relevance: {1 - result.get('distance', 0):.2%}")

    # Print summary
    print("\n" + "=" * 60)
    print("🎉 Agent Created Successfully!")
    print("=" * 60)
    print(f"\nAgent Name: {agent_name}")
    print(f"Workflow ID: {agent.workflow_id}")
    print(f"Knowledge Items: {len(knowledge_items)}")
    print(f"\n✓ Your agent is ready to use!")
    print("\nNext Steps:")
    print("1. Open n8n UI: http://localhost:5678")
    print(f"2. Find your workflow: '{agent_name} Workflow'")
    print("3. Test the workflow with the webhook")
    print("4. Or run: python examples/workflow_integration.py")
    print("\nYou can also interact with the agent using:")
    print("  from src.agent_builder import AgentBuilder")
    print("  builder = AgentBuilder()")
    print(f"  builder.search_agent_memory('{agent_name}', 'your query')")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAgent creation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error creating agent: {e}")
        print("\nMake sure:")
        print("1. n8n is running (http://localhost:5678)")
        print("2. API keys are set in .env file")
        print("3. Dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
