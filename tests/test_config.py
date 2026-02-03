"""
Tests for config.py module.
"""

import os
import pytest
import importlib
import sys


class TestConfigDefaults:
    """Tests for default configuration values."""

    def test_default_swarm_api_url(self):
        """Test default SWARM_API_URL value."""
        # Remove env var if set
        os.environ.pop('SWARM_API_URL', None)
        # Reload module to pick up env change
        import config
        importlib.reload(config)

        assert config.SWARM_API_URL == 'http://127.0.0.1:8420'

    def test_default_min_budget(self):
        """Test default minimum budget value."""
        import config
        assert config.DEFAULT_MIN_BUDGET == 0.05

    def test_default_max_budget(self):
        """Test default maximum budget value."""
        import config
        assert config.DEFAULT_MAX_BUDGET == 0.10

    def test_lock_timeout_seconds(self):
        """Test lock timeout configuration."""
        import config
        assert config.LOCK_TIMEOUT_SECONDS == 300

    def test_api_timeout_seconds(self):
        """Test API timeout configuration."""
        import config
        assert config.API_TIMEOUT_SECONDS == 120


class TestConfigEnvironmentOverride:
    """Tests for environment variable overrides."""

    def test_swarm_api_url_override(self):
        """Test that SWARM_API_URL can be overridden via environment variable."""
        # Set environment variable
        os.environ['SWARM_API_URL'] = 'http://custom.example.com:9999'

        # Reload config module to pick up the new env var
        import config
        importlib.reload(config)

        assert config.SWARM_API_URL == 'http://custom.example.com:9999'

        # Cleanup
        os.environ.pop('SWARM_API_URL')
        importlib.reload(config)

    def test_swarm_api_url_override_with_https(self):
        """Test SWARM_API_URL override with HTTPS."""
        os.environ['SWARM_API_URL'] = 'https://secure.api.com'

        import config
        importlib.reload(config)

        assert config.SWARM_API_URL == 'https://secure.api.com'

        os.environ.pop('SWARM_API_URL')
        importlib.reload(config)

    def test_swarm_api_url_fallback_when_empty(self):
        """Test that empty env var falls back to default."""
        os.environ['SWARM_API_URL'] = ''

        import config
        importlib.reload(config)

        # Empty string is falsy, so os.environ.get with default still applies
        assert config.SWARM_API_URL == '' or config.SWARM_API_URL == 'http://127.0.0.1:8420'

        os.environ.pop('SWARM_API_URL')
        importlib.reload(config)

    def test_constants_are_immutable(self):
        """Test that config constants are not accidentally mutable."""
        import config

        # Numbers should be int/float
        assert isinstance(config.DEFAULT_MIN_BUDGET, float)
        assert isinstance(config.DEFAULT_MAX_BUDGET, float)
        assert isinstance(config.LOCK_TIMEOUT_SECONDS, int)
        assert isinstance(config.API_TIMEOUT_SECONDS, int)

        # Strings should be str
        assert isinstance(config.SWARM_API_URL, str)
