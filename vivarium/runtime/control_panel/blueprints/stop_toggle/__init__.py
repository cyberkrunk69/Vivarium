"""Stop toggle blueprint: kill switch for runtime (emergency stop)."""
from .routes import bp as stop_toggle_bp, get_stop_status

__all__ = ['stop_toggle_bp', 'get_stop_status']
