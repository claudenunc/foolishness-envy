#!/usr/bin/env python3
"""
Create AI Agent on Your Local n8n Instance
Run this script on your Windows machine where n8n is running
"""

import os
import sys
import json
from pathlib import Path

# Setup paths
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from src.agent_builder import AgentBuilder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Create AI agent on local n8n"""
    print("=" * 70)
    print("🤖 Creating AI Agent on Your n8n Instance")
    print("=" * 70)

    # Check environment
    print("\n📋 Checking configuration...")
    n8n_url = os.getenv("N8N_BASE_URL", "http://localhost:5678")
    n8n_key = os.getenv("N8N_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not n8n_key:
        print("❌ N8N_API_KEY not found in .env file")
        return
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return

    print(f"✅ n8n URL: {n8n_url}")
    print(f"✅ API keys configured")

    # Initialize agent builder
    print("\n🔧 Initializing agent builder...")
    try:
        builder = AgentBuilder()
        print("✅ Agent builder initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return

    # Load workflow template
    print("\n📄 Loading workflow template...")
    template_path = script_dir / "templates" / "workflows" / "basic_chat_agent.json"

    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return

    with open(template_path, "r") as f:
        template = json.load(f)
    print("✅ Template loaded")

    # Create the agent
    print("\n🚀 Creating AI agent with workflow...")
    agent_name = "Smart Assistant"

    try:
        agent = builder.create_agent(
            name=agent_name,
            description="An intelligent AI assistant with RAG memory capabilities",
            workflow_template=template,
            initial_instructions="""You are a helpful AI assistant with access to long-term memory.
You can remember past conversations and provide context-aware responses.
Be friendly, helpful, and informative in all your interactions."""
        )
        print(f"✅ Agent created successfully!")
        print(f"   Name: {agent.name}")
        print(f"   Workflow ID: {agent.workflow_id}")
        print(f"   Memory: {agent.memory_collection}")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        print(f"\nMake sure n8n is running at {n8n_url}")
        return

    # Add knowledge to agent
    print("\n📚 Adding knowledge to agent memory...")

    knowledge_base = [
        ("I am an AI assistant built with n8n and RAG memory. I can help with various tasks and remember our conversations.",
         {"type": "identity"}, 1.0),
        ("n8n is a powerful workflow automation tool that connects different services and automates tasks.",
         {"type": "knowledge", "topic": "n8n"}, 0.9),
        ("RAG (Retrieval Augmented Generation) enhances AI responses by retrieving relevant information from a knowledge base.",
         {"type": "knowledge", "topic": "ai"}, 0.9),
        ("Python is excellent for automation, data science, web development, and AI applications.",
         {"type": "knowledge", "topic": "programming"}, 0.8),
        ("This system uses OpenAI for embeddings and language models, with vector storage for semantic search.",
         {"type": "technical"}, 0.7),
    ]

    added_count = 0
    for content, metadata, importance in knowledge_base:
        try:
            memory_id = builder.add_agent_memory(
                agent_name=agent_name,
                content=content,
                metadata=metadata,
                importance=importance
            )
            added_count += 1
            print(f"   ✅ Added: {metadata.get('topic', metadata.get('type', 'general'))}")
        except Exception as e:
            print(f"   ⚠️  Failed to add memory: {e}")

    print(f"\n✅ Added {added_count}/{len(knowledge_base)} knowledge items")

    # Activate workflow
    print("\n⚡ Activating workflow...")
    try:
        builder.n8n_client.activate_workflow(agent.workflow_id)
        print("✅ Workflow activated")
    except Exception as e:
        print(f"⚠️  Could not activate workflow: {e}")
        print("   You can activate it manually in n8n UI")

    # Test memory search
    print("\n🔍 Testing agent memory...")
    test_query = "What can you tell me about n8n?"
    print(f"   Query: '{test_query}'")

    try:
        results = builder.search_agent_memory(
            agent_name=agent_name,
            query=test_query,
            top_k=3
        )
        print(f"\n   Found {len(results)} relevant memories:")
        for i, result in enumerate(results, 1):
            content = result['content']
            if len(content) > 80:
                content = content[:77] + "..."
            relevance = (1 - result.get('distance', 0)) * 100
            print(f"   {i}. {content}")
            print(f"      Relevance: {relevance:.1f}%")
    except Exception as e:
        print(f"   ⚠️  Memory search failed: {e}")

    # Success summary
    print("\n" + "=" * 70)
    print("🎉 SUCCESS! Your AI Agent is Ready!")
    print("=" * 70)
    print(f"\n📌 Agent Details:")
    print(f"   Name: {agent_name}")
    print(f"   Workflow ID: {agent.workflow_id}")
    print(f"   Knowledge Items: {added_count}")
    print(f"   n8n URL: {n8n_url}")

    print(f"\n🌐 Next Steps:")
    print(f"   1. Open n8n UI: {n8n_url}")
    print(f"   2. Find workflow: '{agent_name} Workflow'")
    print(f"   3. Test the workflow with webhook")
    print(f"   4. View workflow execution logs")

    print(f"\n💡 Quick Test:")
    print(f"   from src.agent_builder import AgentBuilder")
    print(f"   builder = AgentBuilder()")
    print(f"   results = builder.search_agent_memory('{agent_name}', 'your question')")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    print("\n⚠️  Make sure n8n is running before executing this script!")
    print("   Check: http://localhost:5678\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Agent creation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n📝 Troubleshooting:")
        print("   1. Ensure n8n is running: http://localhost:5678")
        print("   2. Check .env file has correct API keys")
        print("   3. Install dependencies: pip install -r requirements.txt")
        sys.exit(1)
