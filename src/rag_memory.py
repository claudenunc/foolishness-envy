"""
RAG (Retrieval Augmented Generation) Memory System
Implements semantic memory storage and retrieval using vector embeddings.
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


@dataclass
class MemoryItem:
    """Represents a memory item in the RAG system"""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: str
    importance: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RAGMemory:
    """RAG Memory system using vector embeddings and semantic search"""

    def __init__(self, collection_name: str = "agent_memory"):
        """
        Initialize RAG Memory system

        Args:
            collection_name: Name of the vector collection
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("chromadb not installed. Run: pip install chromadb")

        if not OPENAI_AVAILABLE:
            raise ImportError("openai not installed. Run: pip install openai")

        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = collection_name

        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Agent memory with RAG capabilities"}
        )

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI

        Args:
            text: Text to embed

        Returns:
            List of embedding values
        """
        response = self.openai_client.embeddings.create(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
            input=text
        )
        return response.data[0].embedding

    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0
    ) -> str:
        """
        Add a memory to the RAG system

        Args:
            content: Memory content
            metadata: Additional metadata
            importance: Importance score (0-1)

        Returns:
            Memory ID
        """
        memory_id = f"mem_{datetime.now().timestamp()}"
        timestamp = datetime.now().isoformat()

        # Generate embedding
        embedding = self.generate_embedding(content)

        # Prepare metadata
        full_metadata = {
            "timestamp": timestamp,
            "importance": importance,
            **(metadata or {})
        }

        # Add to vector store
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[full_metadata],
            ids=[memory_id]
        )

        return memory_id

    def search_memory(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant memories using semantic search

        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of relevant memories
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        # Search in vector store
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )

        # Format results
        memories = []
        for i in range(len(results["ids"][0])):
            memories.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None
            })

        return memories

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific memory by ID

        Args:
            memory_id: Memory ID

        Returns:
            Memory data or None
        """
        try:
            result = self.collection.get(ids=[memory_id])
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "content": result["documents"][0],
                    "metadata": result["metadatas"][0]
                }
        except Exception:
            pass
        return None

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory

        Args:
            memory_id: Memory ID

        Returns:
            Success status
        """
        try:
            self.collection.delete(ids=[memory_id])
            return True
        except Exception:
            return False

    def get_conversation_context(
        self,
        query: str,
        max_tokens: int = 2000,
        top_k: int = 5
    ) -> str:
        """
        Get relevant conversation context for a query

        Args:
            query: Current query
            max_tokens: Maximum context tokens
            top_k: Number of memories to retrieve

        Returns:
            Formatted context string
        """
        memories = self.search_memory(query, top_k=top_k)

        context_parts = []
        total_length = 0

        for memory in memories:
            content = memory["content"]
            if total_length + len(content) > max_tokens * 4:  # Rough token estimate
                break
            context_parts.append(f"- {content}")
            total_length += len(content)

        return "\n".join(context_parts)

    def clear_collection(self):
        """Clear all memories from the collection"""
        self.chroma_client.delete_collection(name=self.collection_name)
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"description": "Agent memory with RAG capabilities"}
        )
