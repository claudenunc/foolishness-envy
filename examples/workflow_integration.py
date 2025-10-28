"""
Examples for integrating with n8n workflows
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.n8n_client import N8NClient
from src.agent_builder import AgentBuilder


def list_workflows_example():
    """Example: List all n8n workflows"""
    print("\n=== Listing Workflows ===")
    client = N8NClient()

    try:
        workflows = client.list_workflows()
        print(f"Found {len(workflows)} workflows:")
        for wf in workflows:
            status = "Active" if wf.get("active") else "Inactive"
            print(f"  - {wf['name']} (ID: {wf['id']}) [{status}]")
    except Exception as e:
        print(f"Error: {e}")


def create_workflow_example():
    """Example: Create a new workflow"""
    print("\n=== Creating Workflow ===")

    # Load template
    template_path = "templates/workflows/basic_chat_agent.json"
    with open(template_path, "r") as f:
        template = json.load(f)

    client = N8NClient()

    try:
        workflow_data = {
            "name": "AI Chat Agent",
            "nodes": template["nodes"],
            "connections": template["connections"],
            "settings": template.get("settings", {}),
            "active": False
        }

        workflow = client.create_workflow(workflow_data)
        print(f"Created workflow: {workflow['name']}")
        print(f"Workflow ID: {workflow['id']}")
        print(f"Webhook URL: {workflow.get('webhookUrl', 'N/A')}")

        return workflow["id"]
    except Exception as e:
        print(f"Error: {e}")
        return None


def execute_workflow_example(workflow_id: str):
    """Example: Execute a workflow"""
    print("\n=== Executing Workflow ===")
    client = N8NClient()

    try:
        # Prepare execution data
        data = {
            "query": "What is artificial intelligence?",
            "context": "AI is a field of computer science."
        }

        result = client.execute_workflow(workflow_id, data)
        print(f"Execution started: {result.get('id')}")
        print(f"Status: {result.get('status', 'unknown')}")

        return result.get("id")
    except Exception as e:
        print(f"Error: {e}")
        return None


def agent_with_workflow_example():
    """Example: Create agent with workflow"""
    print("\n=== Creating Agent with Workflow ===")

    # Load template
    template_path = "templates/workflows/basic_chat_agent.json"
    with open(template_path, "r") as f:
        template = json.load(f)

    builder = AgentBuilder()

    try:
        # Create agent with workflow
        agent = builder.create_agent(
            name="Smart Assistant",
            description="AI assistant with n8n workflow",
            workflow_template=template,
            initial_instructions="You are a helpful AI assistant."
        )

        print(f"Created agent: {agent.name}")
        print(f"Workflow ID: {agent.workflow_id}")

        # Add some knowledge
        builder.add_agent_memory(
            agent_name="Smart Assistant",
            content="Python is a high-level programming language.",
            metadata={"topic": "programming"}
        )

        builder.add_agent_memory(
            agent_name="Smart Assistant",
            content="Machine learning is a subset of AI.",
            metadata={"topic": "ai"}
        )

        print("Added knowledge to agent memory")

        # Activate the workflow
        builder.n8n_client.activate_workflow(agent.workflow_id)
        print("Workflow activated")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples"""
    print("=== N8N Workflow Integration Examples ===")

    # Check if API keys are set
    if not os.getenv("N8N_API_KEY"):
        print("\nError: N8N_API_KEY not set")
        print("Please add your n8n API key to .env file")
        return

    # Example 1: List workflows
    list_workflows_example()

    # Example 2: Create workflow
    workflow_id = create_workflow_example()

    # Example 3: Execute workflow (if created)
    if workflow_id:
        execution_id = execute_workflow_example(workflow_id)

    # Example 4: Create agent with workflow
    agent_with_workflow_example()

    print("\n=== Examples completed ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Set N8N_API_KEY in .env")
        print("2. Set N8N_BASE_URL in .env")
        print("3. Your n8n instance is running")
