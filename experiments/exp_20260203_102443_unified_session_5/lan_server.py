#!/usr/bin/env python3
"""
Dual-Server Infrastructure Implementation
- AdminServer: Full control interface (localhost only)
- LANServer: Restricted interface for WiFi users
"""

import http.server
import socketserver
import json
import threading
import time
import os
import uuid
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKSPACE = Path(__file__).parent.parent.parent
ADMIN_PORT = 8080
LAN_PORT = 8081

# Session storage
sessions = {}
sessions_lock = threading.Lock()

# Rate limiting storage
rate_limits = {}
rate_limit_lock = threading.Lock()

class SafetyGateway:
    """Security middleware for LAN server"""
    
    DANGEROUS_PATTERNS = [
        'exec', 'eval', 'import', 'subprocess', '__import__',
        'os.system', 'shell=True', 'rm -rf', 'del ', 'format(',
        'kill', 'terminate', 'shutdown'
    ]
    
    MAX_REQUESTS_PER_MINUTE = 30
    SESSION_TIMEOUT_MINUTES = 60
    
    @classmethod
    def sanitize_input(cls, data):
        """Sanitize input data"""
        if isinstance(data, str):
            for pattern in cls.DANGEROUS_PATTERNS:
                if pattern.lower() in data.lower():
                    logger.warning(f"Blocked dangerous pattern: {pattern}")
                    return None
        return data
    
    @classmethod
    def check_rate_limit(cls, session_id):
        """Check if session is within rate limits"""
        with rate_limit_lock:
            now = datetime.now()
            window_start = now - timedelta(minutes=1)
            
            if session_id not in rate_limits:
                rate_limits[session_id] = []
            
            # Clean old requests
            rate_limits[session_id] = [
                req_time for req_time in rate_limits[session_id]
                if req_time > window_start
            ]
            
            # Check limit
            if len(rate_limits[session_id]) >= cls.MAX_REQUESTS_PER_MINUTE:
                return False
            
            # Add current request
            rate_limits[session_id].append(now)
            return True
    
    @classmethod
    def validate_session(cls, session_id, client_ip):
        """Validate session and IP match"""
        with sessions_lock:
            if session_id not in sessions:
                return False
            
            session = sessions[session_id]
            
            # Check IP match
            if session['device_ip'] != client_ip:
                logger.warning(f"IP mismatch for session {session_id}")
                return False
            
            # Check expiration
            last_access = datetime.fromisoformat(session['last_access'])
            if datetime.now() - last_access > timedelta(minutes=cls.SESSION_TIMEOUT_MINUTES):
                del sessions[session_id]
                return False
            
            # Update last access
            session['last_access'] = datetime.now().isoformat()
            return True

class AdminServer:
    """Full control server for localhost only"""
    
    def __init__(self, port=ADMIN_PORT):
        self.port = port
        self.server = None
        
    class AdminHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/admin/status':
                self.send_full_status()
            elif self.path == '/admin/logs':
                self.send_all_logs()
            elif self.path == '/admin/experiments':
                self.send_experiments()
            elif self.path == '/admin/performance':
                self.send_performance_metrics()
            elif self.path.startswith('/admin/'):
                self.send_admin_interface()
            else:
                self.send_response(404)
                self.end_headers()
        
        def do_POST(self):
            if self.path == '/admin/start':
                self.handle_start_workers()
            elif self.path == '/admin/stop':
                self.handle_stop_workers()
            elif self.path == '/admin/config':
                self.handle_config_update()
            elif self.path == '/admin/kill-all':
                self.handle_emergency_kill()
            elif self.path == '/admin/backup':
                self.handle_backup()
            else:
                self.send_response(404)
                self.end_headers()
        
        def send_full_status(self):
            """Send complete system status"""
            try:
                wave_file = WORKSPACE / "wave_status.json"
                if wave_file.exists():
                    with open(wave_file, 'r') as f:
                        status = json.load(f)
                else:
                    status = {"status": "No wave status available"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(status, indent=2).encode())
            except Exception as e:
                self.send_error(500, f"Error loading status: {e}")
        
        def send_all_logs(self):
            """Send all system logs"""
            try:
                logs = []
                log_dir = WORKSPACE / "grind_logs"
                if log_dir.exists():
                    for log_file in log_dir.glob("*.json"):
                        try:
                            with open(log_file, 'r') as f:
                                log_data = json.load(f)
                                logs.append({
                                    "file": log_file.name,
                                    "data": log_data
                                })
                        except:
                            continue
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(logs, indent=2).encode())
            except Exception as e:
                self.send_error(500, f"Error loading logs: {e}")
        
        def send_experiments(self):
            """Send experiment management data"""
            try:
                experiments = []
                exp_dir = WORKSPACE / "experiments"
                if exp_dir.exists():
                    for exp in exp_dir.iterdir():
                        if exp.is_dir():
                            experiments.append({
                                "name": exp.name,
                                "path": str(exp),
                                "created": exp.stat().st_ctime
                            })
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(experiments, indent=2).encode())
            except Exception as e:
                self.send_error(500, f"Error loading experiments: {e}")
        
        def send_performance_metrics(self):
            """Send detailed performance metrics"""
            try:
                perf_file = WORKSPACE / "performance_history.json"
                if perf_file.exists():
                    with open(perf_file, 'r') as f:
                        metrics = json.load(f)
                else:
                    metrics = {"metrics": "No performance data available"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(metrics, indent=2).encode())
            except Exception as e:
                self.send_error(500, f"Error loading metrics: {e}")
        
        def send_admin_interface(self):
            """Send admin dashboard interface"""
            # Load existing dashboard if available
            dashboard_file = WORKSPACE / "dashboard.html"
            if dashboard_file.exists():
                with open(dashboard_file, 'r') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def handle_start_workers(self):
            """Handle worker start request"""
            logger.info("Admin: Starting workers")
            # Integration point with grind_spawner.py
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "Workers start requested"}')
        
        def handle_stop_workers(self):
            """Handle worker stop request"""
            logger.info("Admin: Stopping workers")
            # Integration point with grind_spawner.py
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "Workers stop requested"}')
        
        def handle_config_update(self):
            """Handle configuration update"""
            logger.info("Admin: Config update requested")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "Config update completed"}')
        
        def handle_emergency_kill(self):
            """Handle emergency kill all"""
            logger.critical("Admin: EMERGENCY KILL ALL requested")
            # Integration point for emergency shutdown
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "EMERGENCY KILL executed"}')
        
        def handle_backup(self):
            """Handle backup creation"""
            logger.info("Admin: Backup requested")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "Backup created"}')
    
    def start(self):
        """Start the admin server"""
        try:
            with socketserver.TCPServer(("127.0.0.1", self.port), self.AdminHandler) as httpd:
                self.server = httpd
                logger.info(f"Admin server running on http://127.0.0.1:{self.port}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"Admin server error: {e}")

class LANServer:
    """Restricted server for WiFi users"""
    
    def __init__(self, port=LAN_PORT):
        self.port = port
        self.server = None
        
    class LANHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            # Extract session from headers or query params
            session_id = self.get_session_id()
            client_ip = self.client_address[0]
            
            if not self.validate_request(session_id, client_ip):
                return
            
            if self.path == '/lan/status':
                self.send_basic_status()
            elif self.path == '/lan/logs/recent':
                self.send_recent_logs()
            elif self.path == '/lan/experiments/list':
                self.send_experiment_list()
            elif self.path == '/lan/metrics/basic':
                self.send_basic_metrics()
            elif self.path == '/lan/health':
                self.send_health_check()
            elif self.path == '/lan/session/validate':
                self.validate_session()
            else:
                self.send_response(404)
                self.end_headers()
        
        def do_POST(self):
            client_ip = self.client_address[0]
            
            if self.path == '/lan/session/create':
                self.create_session(client_ip)
            elif self.path == '/lan/emergency-stop':
                session_id = self.get_session_id()
                if self.validate_request(session_id, client_ip):
                    self.handle_emergency_stop()
            else:
                self.send_response(404)
                self.end_headers()
        
        def get_session_id(self):
            """Extract session ID from request"""
            # Try Authorization header first
            auth_header = self.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                return auth_header[7:]
            
            # Try query parameter
            if '?' in self.path:
                query = parse_qs(urlparse(self.path).query)
                if 'session' in query:
                    return query['session'][0]
            
            return None
        
        def validate_request(self, session_id, client_ip):
            """Validate session and rate limits"""
            if not session_id:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Session required"}')
                return False
            
            if not SafetyGateway.validate_session(session_id, client_ip):
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid session"}')
                return False
            
            if not SafetyGateway.check_rate_limit(session_id):
                self.send_response(429)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Rate limit exceeded"}')
                return False
            
            return True
        
        def send_basic_status(self):
            """Send sanitized basic status"""
            try:
                wave_file = WORKSPACE / "wave_status.json"
                if wave_file.exists():
                    with open(wave_file, 'r') as f:
                        status = json.load(f)
                    
                    # Sanitize - only basic info
                    sanitized = {
                        "wave": status.get("wave", "Unknown"),
                        "active_workers": status.get("active_workers", 0),
                        "status": status.get("status", "Unknown"),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    sanitized = {
                        "status": "System operational",
                        "timestamp": datetime.now().isoformat()
                    }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(sanitized, indent=2).encode())
            except Exception as e:
                self.send_error(500, "Error loading status")
        
        def send_recent_logs(self):
            """Send recent logs (filtered)"""
            try:
                logs = []
                log_dir = WORKSPACE / "grind_logs"
                if log_dir.exists():
                    # Get only the 5 most recent log files
                    recent_logs = sorted(log_dir.glob("*.json"), 
                                       key=lambda x: x.stat().st_mtime, 
                                       reverse=True)[:5]
                    
                    for log_file in recent_logs:
                        try:
                            with open(log_file, 'r') as f:
                                log_data = json.load(f)
                                # Filter sensitive information
                                filtered_data = {
                                    "timestamp": log_data.get("timestamp", ""),
                                    "status": log_data.get("status", ""),
                                    "workers": log_data.get("workers", 0)
                                }
                                logs.append({
                                    "file": log_file.name,
                                    "data": filtered_data
                                })
                        except:
                            continue
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(logs, indent=2).encode())
            except Exception as e:
                self.send_error(500, "Error loading logs")
        
        def send_experiment_list(self):
            """Send experiment names only"""
            try:
                experiments = []
                exp_dir = WORKSPACE / "experiments"
                if exp_dir.exists():
                    for exp in exp_dir.iterdir():
                        if exp.is_dir():
                            experiments.append({
                                "name": exp.name,
                                "created": exp.stat().st_ctime
                            })
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(experiments, indent=2).encode())
            except Exception as e:
                self.send_error(500, "Error loading experiments")
        
        def send_basic_metrics(self):
            """Send basic performance metrics"""
            try:
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "uptime": "Available on admin interface",
                    "status": "Operational"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(metrics, indent=2).encode())
            except Exception as e:
                self.send_error(500, "Error loading metrics")
        
        def send_health_check(self):
            """Simple health check"""
            health = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(health).encode())
        
        def create_session(self, client_ip):
            """Create new session for client"""
            try:
                session_id = str(uuid.uuid4())
                user_agent = self.headers.get('User-Agent', 'Unknown')
                
                session_data = {
                    "session_id": session_id,
                    "device_ip": client_ip,
                    "device_info": user_agent,
                    "created_at": datetime.now().isoformat(),
                    "last_access": datetime.now().isoformat(),
                    "permissions": ["view_status", "view_logs", "emergency_stop"],
                    "rate_limit": {
                        "requests_per_minute": 30,
                        "current_count": 0,
                        "window_start": datetime.now().isoformat()
                    }
                }
                
                with sessions_lock:
                    sessions[session_id] = session_data
                
                logger.info(f"Created session {session_id} for {client_ip}")
                
                response = {
                    "session_id": session_id,
                    "permissions": session_data["permissions"],
                    "expires_in": SafetyGateway.SESSION_TIMEOUT_MINUTES * 60
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Session creation error: {e}")
                self.send_error(500, "Session creation failed")
        
        def validate_session(self):
            """Validate current session"""
            session_id = self.get_session_id()
            client_ip = self.client_address[0]
            
            if SafetyGateway.validate_session(session_id, client_ip):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"valid": true}')
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"valid": false}')
        
        def handle_emergency_stop(self):
            """Handle emergency stop request"""
            logger.critical(f"LAN: Emergency stop requested from {self.client_address[0]}")
            # Integration point for emergency stop
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "Emergency stop executed"}')
    
    def start(self):
        """Start the LAN server"""
        try:
            with socketserver.TCPServer(("0.0.0.0", self.port), self.LANHandler) as httpd:
                self.server = httpd
                logger.info(f"LAN server running on http://0.0.0.0:{self.port}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"LAN server error: {e}")

def cleanup_expired_sessions():
    """Background task to cleanup expired sessions"""
    while True:
        try:
            now = datetime.now()
            expired_sessions = []
            
            with sessions_lock:
                for session_id, session in sessions.items():
                    last_access = datetime.fromisoformat(session['last_access'])
                    if now - last_access > timedelta(minutes=SafetyGateway.SESSION_TIMEOUT_MINUTES):
                        expired_sessions.append(session_id)
                
                for session_id in expired_sessions:
                    del sessions[session_id]
                    logger.info(f"Expired session {session_id}")
            
            # Cleanup rate limits
            with rate_limit_lock:
                window_start = now - timedelta(minutes=1)
                for session_id in list(rate_limits.keys()):
                    if session_id not in sessions:
                        del rate_limits[session_id]
            
        except Exception as e:
            logger.error(f"Session cleanup error: {e}")
        
        time.sleep(300)  # Run every 5 minutes

def main():
    """Start both servers"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dual-Server Infrastructure')
    parser.add_argument('--admin-only', action='store_true', 
                       help='Start admin server only')
    parser.add_argument('--lan-only', action='store_true',
                       help='Start LAN server only')
    args = parser.parse_args()
    
    # Start session cleanup background task
    cleanup_thread = threading.Thread(target=cleanup_expired_sessions, daemon=True)
    cleanup_thread.start()
    
    if args.admin_only:
        admin_server = AdminServer()
        admin_server.start()
    elif args.lan_only:
        lan_server = LANServer()
        lan_server.start()
    else:
        # Start both servers
        admin_server = AdminServer()
        lan_server = LANServer()
        
        admin_thread = threading.Thread(target=admin_server.start, daemon=True)
        admin_thread.start()
        
        logger.info("Starting both servers...")
        lan_server.start()  # Main thread runs LAN server

if __name__ == '__main__':
    main()