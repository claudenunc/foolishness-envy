"""
Agent Builder
Creates and manages AI agents with n8n workflows and RAG memory.
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from .n8n_client import N8NClient
from .rag_memory import RAGMemory

load_dotenv()


class Agent:
    """Represents an AI agent with memory and n8n workflows"""

    def __init__(
        self,
        name: str,
        description: str,
        workflow_id: Optional[str] = None,
        memory_collection: Optional[str] = None
    ):
        """
        Initialize an agent

        Args:
            name: Agent name
            description: Agent description
            workflow_id: Associated n8n workflow ID
            memory_collection: Memory collection name
        """
        self.name = name
        self.description = description
        self.workflow_id = workflow_id
        self.memory_collection = memory_collection or f"agent_{name.lower().replace(' ', '_')}"
        self.created_at = datetime.now().isoformat()

        # Initialize memory
        self.memory = RAGMemory(collection_name=self.memory_collection)

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "workflow_id": self.workflow_id,
            "memory_collection": self.memory_collection,
            "created_at": self.created_at
        }


class AgentBuilder:
    """Builds and manages AI agents"""

    def __init__(self):
        """Initialize the agent builder"""
        self.n8n_client = N8NClient()
        self.agents: Dict[str, Agent] = {}
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {}

    def create_agent(
        self,
        name: str,
        description: str,
        workflow_template: Optional[Dict[str, Any]] = None,
        initial_instructions: Optional[str] = None
    ) -> Agent:
        """
        Create a new agent

        Args:
            name: Agent name
            description: Agent description
            workflow_template: Optional n8n workflow template
            initial_instructions: Initial instructions for the agent

        Returns:
            Created agent
        """
        # Create workflow if template provided
        workflow_id = None
        if workflow_template:
            workflow_data = {
                "name": f"{name} Workflow",
                "nodes": workflow_template.get("nodes", []),
                "connections": workflow_template.get("connections", {}),
                "settings": workflow_template.get("settings", {}),
                "active": False
            }
            workflow = self.n8n_client.create_workflow(workflow_data)
            workflow_id = workflow["id"]

        # Create agent
        agent = Agent(
            name=name,
            description=description,
            workflow_id=workflow_id
        )

        # Add initial instructions to memory
        if initial_instructions:
            agent.memory.add_memory(
                content=initial_instructions,
                metadata={"type": "instructions", "agent": name},
                importance=1.0
            )

        # Store agent
        self.agents[name] = agent

        return agent

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents"""
        return [agent.to_dict() for agent in self.agents.values()]

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        use_memory: bool = True
    ) -> Dict[str, Any]:
        """
        Run an agent

        Args:
            agent_name: Name of the agent to run
            input_data: Input data for the agent
            use_memory: Whether to use RAG memory

        Returns:
            Execution result
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")

        if not agent.workflow_id:
            raise ValueError(f"Agent '{agent_name}' has no workflow")

        # Get relevant context from memory if enabled
        context = ""
        if use_memory and "query" in input_data:
            memories = agent.memory.search_memory(
                query=input_data["query"],
                top_k=self.config.get("rag_settings", {}).get("top_k_results", 5)
            )
            context = "\n".join([m["content"] for m in memories])

        # Prepare execution data
        execution_data = {
            **input_data,
            "context": context,
            "agent_name": agent_name
        }

        # Execute workflow
        result = self.n8n_client.execute_workflow(
            workflow_id=agent.workflow_id,
            data=execution_data
        )

        # Store interaction in memory
        if use_memory:
            agent.memory.add_memory(
                content=f"Query: {input_data.get('query', '')}\nResponse: {result.get('data', '')}",
                metadata={
                    "type": "interaction",
                    "execution_id": result.get("id"),
                    "timestamp": datetime.now().isoformat()
                }
            )

        return result

    def add_agent_memory(
        self,
        agent_name: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0
    ) -> str:
        """
        Add memory to an agent

        Args:
            agent_name: Name of the agent
            content: Memory content
            metadata: Additional metadata
            importance: Importance score

        Returns:
            Memory ID
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")

        return agent.memory.add_memory(
            content=content,
            metadata=metadata,
            importance=importance
        )

    def search_agent_memory(
        self,
        agent_name: str,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search agent memory

        Args:
            agent_name: Name of the agent
            query: Search query
            top_k: Number of results

        Returns:
            Search results
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")

        return agent.memory.search_memory(query=query, top_k=top_k)

    def create_workflow_from_template(
        self,
        template_name: str,
        agent_name: str
    ) -> str:
        """
        Create a workflow from a template

        Args:
            template_name: Template name
            agent_name: Agent name

        Returns:
            Workflow ID
        """
        template_path = f"templates/workflows/{template_name}.json"
        if not os.path.exists(template_path):
            raise ValueError(f"Template '{template_name}' not found")

        with open(template_path, "r") as f:
            template = json.load(f)

        workflow_data = {
            "name": f"{agent_name} - {template['name']}",
            "nodes": template["nodes"],
            "connections": template["connections"],
            "settings": template.get("settings", {}),
            "active": False
        }

        workflow = self.n8n_client.create_workflow(workflow_data)
        return workflow["id"]
