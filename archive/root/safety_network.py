"""
Network Isolation Enforcement Module

Prevents unauthorized external network access from generated code.
Maintains whitelist of allowed local addresses and blocks external patterns.
"""

import re
import socket
from contextlib import contextmanager
from typing import List, Dict, Set
from datetime import datetime


class NetworkGuard:
    """Enforces network isolation for generated code execution."""

    def __init__(self):
        # Whitelist: only local addresses allowed
        self.whitelist: Set[str] = {
            '127.0.0.1',
            'localhost',
            '::1',
            '0.0.0.0'
        }

        # Blocked patterns: external network protocols
        self.blocked_patterns: List[str] = [
            r'https?://',
            r'ftp://',
            r'ftps://',
            r'ssh://',
            r'telnet://',
            r'smtp://',
            r'ws://',
            r'wss://',
            r'requests\.',
            r'urllib',
            r'httpx\.',
            r'aiohttp\.',
            r'socket\.connect',
            r'socket\.socket\(',
            r'http\.client',
            r'xmlrpc\.',
        ]

        # Exception: GitHub push only when user explicitly requests
        self.github_allowed = False
        self.github_patterns: List[str] = [
            r'git\s+push',
            r'gh\s+',
            r'github\.com',
            r'api\.github\.com',
        ]

        self.violation_log: List[Dict] = []

    def allow_github_push(self, allowed: bool = True):
        """Enable/disable GitHub push operations."""
        self.github_allowed = allowed

    def scan_for_network_access(self, code_text: str) -> List[Dict[str, str]]:
        """
        Scan code for network access violations.

        Args:
            code_text: Python code to scan

        Returns:
            List of violations with line numbers and descriptions
        """
        violations = []
        lines = code_text.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue

            # Check blocked patterns
            for pattern in self.blocked_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        'line': line_num,
                        'code': line.strip(),
                        'pattern': pattern,
                        'severity': 'HIGH',
                        'message': f'Blocked network pattern detected: {pattern}'
                    })

            # Check GitHub patterns (only if not explicitly allowed)
            if not self.github_allowed:
                for pattern in self.github_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            'line': line_num,
                            'code': line.strip(),
                            'pattern': pattern,
                            'severity': 'MEDIUM',
                            'message': f'GitHub access detected (requires explicit permission): {pattern}'
                        })

        # Log violations
        if violations:
            self.violation_log.append({
                'timestamp': datetime.now().isoformat(),
                'violations': violations,
                'code_preview': code_text[:200]
            })

        return violations

    def is_address_allowed(self, address: str) -> bool:
        """Check if network address is whitelisted."""
        # Check exact whitelist matches
        if address in self.whitelist:
            return True

        # Check if it's a local address
        try:
            # Resolve hostname
            ip = socket.gethostbyname(address)
            if ip in self.whitelist or ip.startswith('127.') or ip.startswith('192.168.'):
                return True
        except socket.gaierror:
            pass

        return False

    def get_violation_summary(self) -> Dict:
        """Get summary of all logged violations."""
        return {
            'total_scans': len(self.violation_log),
            'total_violations': sum(len(v['violations']) for v in self.violation_log),
            'recent_violations': self.violation_log[-10:] if self.violation_log else []
        }


@contextmanager
def block_external_calls():
    """
    Context manager that blocks external network calls during execution.

    Patches common network libraries to prevent external access.
    """
    import unittest.mock as mock

    def blocked_call(*args, **kwargs):
        raise PermissionError(
            "External network access blocked by safety_network.py. "
            "Only localhost (127.0.0.1) is permitted."
        )

    # Patch common network libraries
    patches = []

    try:
        # Patch socket operations
        if 'socket' in globals() or True:
            import socket as socket_module
            patches.append(mock.patch.object(socket_module.socket, 'connect', side_effect=blocked_call))

        # Patch requests library if available
        try:
            import requests
            patches.append(mock.patch.object(requests, 'get', side_effect=blocked_call))
            patches.append(mock.patch.object(requests, 'post', side_effect=blocked_call))
            patches.append(mock.patch.object(requests, 'put', side_effect=blocked_call))
            patches.append(mock.patch.object(requests, 'delete', side_effect=blocked_call))
        except ImportError:
            pass

        # Patch urllib if available
        try:
            import urllib.request
            patches.append(mock.patch.object(urllib.request, 'urlopen', side_effect=blocked_call))
        except ImportError:
            pass

        # Start all patches
        for patch_obj in patches:
            patch_obj.start()

        yield

    finally:
        # Stop all patches
        for patch_obj in patches:
            try:
                patch_obj.stop()
            except Exception:
                pass


# Global instance
network_guard = NetworkGuard()


def scan_for_network_access(code_text: str) -> List[Dict[str, str]]:
    """
    Convenience function to scan code for network violations.

    Args:
        code_text: Python code to scan

    Returns:
        List of violations
    """
    return network_guard.scan_for_network_access(code_text)
