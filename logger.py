import os
import sys
import json
from datetime import datetime
from typing import Optional, Any, Dict

LOG_LEVELS = {
    "DEBUG": 0,
    "INFO": 1,
    "WARN": 2,
    "ERROR": 3,
}

class Logger:
    def __init__(self, worker_id: str = "default", output_file: Optional[str] = None, level: str = "INFO"):
        """
        Initialize logger with worker ID and optional file output.

        Args:
            worker_id: Identifier for distributed debugging
            output_file: Path to log file (None = stdout only)
            level: Minimum log level (DEBUG, INFO, WARN, ERROR)
        """
        self.worker_id = worker_id
        self.output_file = output_file
        self.level = level
        self.min_level = LOG_LEVELS.get(level, 1)

    def _format_message(self, level: str, message: str, source: str, context: Dict[str, Any]) -> str:
        """Format log message with timestamp, level, source, and context."""
        timestamp = datetime.now().isoformat()
        context_str = " " + str(context) if context else ""
        return f"[{timestamp}] [{level}] [{source}] {message}{context_str}"

    def _write_log(self, formatted_message: str) -> None:
        """Write log to file and/or stdout."""
        if self.output_file:
            try:
                with open(self.output_file, "a", encoding='utf-8') as f:
                    f.write(formatted_message + "\n")
            except IOError as e:
                sys.stderr.write(f"Failed to write to log file: {e}\n")

        # Always output to stdout
        print(formatted_message)

    def log(self, level: str, message: str, source: str = "app", **context) -> None:
        """
        Log a message with specified level and context.

        Args:
            level: Log level (DEBUG, INFO, WARN, ERROR)
            message: Main log message
            source: Source identifier (defaults to "app")
            **context: Additional context data as key=value pairs
        """
        level = level.upper()
        if level not in LOG_LEVELS:
            level = "INFO"

        if LOG_LEVELS[level] < self.min_level:
            return

        formatted = self._format_message(level, message, source, context)
        self._write_log(formatted)

    def debug(self, message: str, source: str = "app", **context) -> None:
        """Log debug message."""
        self.log("DEBUG", message, source, **context)

    def info(self, message: str, source: str = "app", **context) -> None:
        """Log info message."""
        self.log("INFO", message, source, **context)

    def warn(self, message: str, source: str = "app", **context) -> None:
        """Log warning message."""
        self.log("WARN", message, source, **context)

    def error(self, message: str, source: str = "app", **context) -> None:
        """Log error message."""
        self.log("ERROR", message, source, **context)

    def _write_json_log(self, json_data: str) -> None:
        """Write structured JSON log to structured_logs.jsonl file."""
        json_logfile = "structured_logs.jsonl"
        try:
            with open(json_logfile, "a", encoding='utf-8') as f:
                f.write(json_data + "\n")
        except IOError as e:
            sys.stderr.write(f"Failed to write to JSON log file: {e}\n")

    def json_log(self, level: str, message: str, **context) -> None:
        """
        Log a structured JSON message.

        Args:
            level: Log level (DEBUG, INFO, WARN, ERROR)
            message: Main log message
            **context: Additional context data as key=value pairs

        Format: {timestamp, level, message, context}
        Writes to structured_logs.jsonl
        """
        level = level.upper()
        if level not in LOG_LEVELS:
            level = "INFO"

        if LOG_LEVELS[level] < self.min_level:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "worker_id": self.worker_id,
            "context": context
        }

        json_str = json.dumps(log_entry)
        self._write_json_log(json_str)


# Global logger instance
_logger: Optional[Logger] = None

def init_logger(worker_id: str = "default", output_file: Optional[str] = None, level: str = "INFO") -> Logger:
    """Initialize global logger instance."""
    global _logger
    _logger = Logger(worker_id=worker_id, output_file=output_file, level=level)
    return _logger

def get_logger() -> Logger:
    """Get global logger instance."""
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger

def log(level: str, message: str, source: str = "app", **context) -> None:
    """Log using global logger instance."""
    get_logger().log(level, message, source, **context)

def debug(message: str, source: str = "app", **context) -> None:
    """Log debug message using global logger."""
    get_logger().debug(message, source, **context)

def info(message: str, source: str = "app", **context) -> None:
    """Log info message using global logger."""
    get_logger().info(message, source, **context)

def warn(message: str, source: str = "app", **context) -> None:
    """Log warning message using global logger."""
    get_logger().warn(message, source, **context)

def error(message: str, source: str = "app", **context) -> None:
    """Log error message using global logger."""
    get_logger().error(message, source, **context)

def json_log(level: str, message: str, **context) -> None:
    """Log structured JSON message using global logger."""
    get_logger().json_log(level, message, **context)
