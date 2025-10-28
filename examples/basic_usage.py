"""
Basic usage examples for the N8N Agent Builder with RAG Memory
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent_builder import AgentBuilder


def main():
    """Run basic examples"""

    print("=== N8N Agent Builder Examples ===\n")

    # Initialize agent builder
    builder = AgentBuilder()

    # Example 1: Create a simple chat agent
    print("1. Creating a chat agent...")
    chat_agent = builder.create_agent(
        name="Customer Support",
        description="Helpful customer support agent",
        initial_instructions="You are a friendly customer support agent. Help users with their questions."
    )
    print(f"   Created: {chat_agent.name}")
    print(f"   Memory collection: {chat_agent.memory_collection}\n")

    # Example 2: Add memories to the agent
    print("2. Adding knowledge to agent memory...")
    builder.add_agent_memory(
        agent_name="Customer Support",
        content="Our company offers 24/7 customer support via email and chat.",
        metadata={"category": "support_info"},
        importance=0.9
    )
    builder.add_agent_memory(
        agent_name="Customer Support",
        content="Refunds are processed within 5-7 business days.",
        metadata={"category": "refund_policy"},
        importance=0.8
    )
    builder.add_agent_memory(
        agent_name="Customer Support",
        content="Premium members get priority support and free shipping.",
        metadata={"category": "premium_benefits"},
        importance=0.7
    )
    print("   Added 3 knowledge items to memory\n")

    # Example 3: Search memory
    print("3. Searching agent memory...")
    query = "What are the benefits for premium users?"
    results = builder.search_agent_memory(
        agent_name="Customer Support",
        query=query,
        top_k=2
    )
    print(f"   Query: '{query}'")
    print("   Results:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['content']}")
        print(f"      (relevance: {1 - result.get('distance', 0):.2f})")
    print()

    # Example 4: Create a data processing agent
    print("4. Creating a data processing agent...")
    data_agent = builder.create_agent(
        name="Data Analyzer",
        description="Agent for analyzing and processing data",
        initial_instructions="You analyze data and provide insights."
    )
    print(f"   Created: {data_agent.name}\n")

    # Example 5: List all agents
    print("5. Listing all agents...")
    agents = builder.list_agents()
    print(f"   Total agents: {len(agents)}")
    for agent in agents:
        print(f"   - {agent['name']}: {agent['description']}")
    print()

    print("=== Examples completed ===")
    print("\nNote: To execute workflows, make sure to:")
    print("1. Set your N8N_API_KEY in .env file")
    print("2. Set your N8N_BASE_URL in .env file")
    print("3. Set your OPENAI_API_KEY in .env file")
    print("4. Create workflow templates in n8n")


if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set in environment")
        print("Please copy .env.example to .env and add your API keys\n")

    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Copied .env.example to .env")
        print("2. Added your API keys to .env")
        print("3. Installed dependencies: pip install -r requirements.txt")
