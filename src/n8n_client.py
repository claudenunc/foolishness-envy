"""
N8N API Client
Handles all interactions with n8n API for workflow management and execution.
"""

import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class N8NClient:
    """Client for interacting with n8n API"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize N8N client

        Args:
            api_key: n8n API key (defaults to N8N_API_KEY env var)
            base_url: n8n instance URL (defaults to N8N_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        self.base_url = (base_url or os.getenv("N8N_BASE_URL", "")).rstrip("/")

        if not self.api_key:
            raise ValueError("N8N_API_KEY not provided")
        if not self.base_url:
            raise ValueError("N8N_BASE_URL not provided")

        self.headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        response = requests.get(
            f"{self.base_url}/api/v1/workflows",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["data"]

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID"""
        response = requests.get(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow"""
        response = requests.post(
            f"{self.base_url}/api/v1/workflows",
            headers=self.headers,
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()

    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing workflow"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()

    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        response = requests.delete(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return True

    def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Activate a workflow"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json={"active": True}
        )
        response.raise_for_status()
        return response.json()

    def deactivate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Deactivate a workflow"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json={"active": False}
        )
        response.raise_for_status()
        return response.json()

    def execute_workflow(self, workflow_id: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow"""
        response = requests.post(
            f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
            headers=self.headers,
            json=data or {}
        )
        response.raise_for_status()
        return response.json()

    def get_executions(self, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get workflow executions"""
        url = f"{self.base_url}/api/v1/executions"
        if workflow_id:
            url += f"?workflowId={workflow_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]

    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get a specific execution by ID"""
        response = requests.get(
            f"{self.base_url}/api/v1/executions/{execution_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
