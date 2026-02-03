"""
MetaGPT-style Shared Message Pool for Multi-Agent Coordination

Implements publish-subscribe messaging between roles for structured communication.
Based on arXiv:2308.00352 (MetaGPT: Communicative Agents for Software Development).
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class MessagePool:
    """
    Centralized message pool for agent communication.

    Agents publish structured messages and subscribe to relevant message types.
    All communication is stored in JSON format for auditability and persistence.
    """

    def __init__(self, storage_path: str = "message_pool.json"):
        """
        Initialize the message pool with optional persistent storage.

        Args:
            storage_path: Path to JSON file for storing messages
        """
        self.storage_path = storage_path
        self.messages: List[Dict[str, Any]] = []
        self._message_counter = 0
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load existing messages from storage file if it exists."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.messages = data.get("messages", [])
                    self._message_counter = len(self.messages)
            except (json.JSONDecodeError, IOError):
                self.messages = []
                self._message_counter = 0

    def _save_to_file(self) -> None:
        """Persist current messages to storage file."""
        with open(self.storage_path, 'w') as f:
            json.dump({"messages": self.messages}, f, indent=2)

    def publish(
        self,
        from_role: str,
        message_type: str,
        content: Dict[str, Any],
        subscribers: Optional[List[str]] = None
    ) -> str:
        """
        Publish a message to the pool.

        Args:
            from_role: Role publishing the message
            message_type: Type of message (TASK_ASSIGNMENT, EXECUTION_PLAN, etc.)
            content: Message content as dict
            subscribers: List of roles that should consume this message

        Returns:
            Message ID
        """
        self._message_counter += 1
        message_id = f"msg_{self._message_counter:03d}"

        message = {
            "id": message_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "from_role": from_role,
            "type": message_type,
            "content": content,
            "subscribers": subscribers or []
        }

        self.messages.append(message)
        self._save_to_file()

        return message_id

    def subscribe(self, role: str, message_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get messages relevant to a role.

        Args:
            role: Role name requesting messages
            message_type: Optional filter by message type

        Returns:
            List of messages intended for this role
        """
        relevant_messages = []

        for message in self.messages:
            # Check if role is in subscribers list
            if role not in message.get("subscribers", []):
                continue

            # Filter by message type if specified
            if message_type and message.get("type") != message_type:
                continue

            relevant_messages.append(message)

        return relevant_messages

    def get_message_by_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific message by ID.

        Args:
            message_id: Message ID to retrieve

        Returns:
            Message dict or None if not found
        """
        for message in self.messages:
            if message["id"] == message_id:
                return message
        return None

    def get_messages_by_type(self, message_type: str) -> List[Dict[str, Any]]:
        """
        Get all messages of a specific type.

        Args:
            message_type: Type of messages to retrieve

        Returns:
            List of messages of that type
        """
        return [msg for msg in self.messages if msg.get("type") == message_type]

    def get_messages_from_role(self, from_role: str) -> List[Dict[str, Any]]:
        """
        Get all messages published by a specific role.

        Args:
            from_role: Role name

        Returns:
            List of messages from that role
        """
        return [msg for msg in self.messages if msg.get("from_role") == from_role]

    def clear(self) -> None:
        """Clear all messages from the pool."""
        self.messages = []
        self._message_counter = 0
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)

    def export_messages(self) -> Dict[str, Any]:
        """
        Export all messages in structured format.

        Returns:
            Dictionary containing all messages
        """
        return {
            "messages": self.messages,
            "total_count": len(self.messages),
            "last_updated": datetime.now().isoformat() + "Z"
        }


# Global message pool instance
_global_pool: Optional[MessagePool] = None


def get_message_pool(storage_path: str = "message_pool.json") -> MessagePool:
    """
    Get or create the global message pool instance.

    Args:
        storage_path: Path to JSON storage file

    Returns:
        MessagePool instance
    """
    global _global_pool
    if _global_pool is None:
        _global_pool = MessagePool(storage_path)
    return _global_pool


def reset_message_pool() -> None:
    """Reset the global message pool instance."""
    global _global_pool
    _global_pool = None
