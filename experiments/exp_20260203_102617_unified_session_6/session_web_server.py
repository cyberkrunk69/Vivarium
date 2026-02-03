#!/usr/bin/env python3
"""
Web Server for LAN Session Dashboard
Serves dashboard HTML and provides REST API endpoints
"""

from flask import Flask, jsonify, request, send_from_directory, render_template_string
import os
import logging
from datetime import datetime
import json
from lan_session_manager import get_session_manager
from session_websocket_server import get_websocket_server

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Global session manager
session_manager = get_session_manager()
websocket_server = get_websocket_server()

def get_client_ip():
    """Get client IP address from request"""
    # Check for forwarded IP first (proxy/reverse proxy)
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    elif request.environ.get('HTTP_X_REAL_IP'):
        return request.environ['HTTP_X_REAL_IP']
    else:
        return request.environ.get('REMOTE_ADDR', 'unknown')

@app.route('/')
def dashboard_home():
    """Serve main dashboard page"""
    client_ip = get_client_ip()
    logger.info(f"Dashboard access from {client_ip}")

    # Ensure session exists
    session_manager.create_session(client_ip)

    # Read and return dashboard HTML
    dashboard_path = os.path.join(os.path.dirname(__file__), 'session_dashboard.html')
    try:
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return jsonify({'error': 'Dashboard template not found'}), 500

@app.route('/api/client-ip')
def get_client_ip_endpoint():
    """Return client IP address"""
    client_ip = get_client_ip()
    return jsonify({
        'ip': client_ip,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard/<client_ip>')
def get_dashboard_data(client_ip):
    """Get dashboard data for specific client"""
    try:
        # Validate IP format (basic check)
        if not client_ip or client_ip == 'undefined':
            client_ip = get_client_ip()

        # Ensure session exists
        session = session_manager.create_session(client_ip)

        # Get dashboard data
        dashboard_data = session_manager.get_user_dashboard_data(client_ip)

        return jsonify(dashboard_data)

    except Exception as e:
        logger.error(f"Error getting dashboard data for {client_ip}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<client_ip>')
def get_session_info(client_ip):
    """Get session information"""
    try:
        session = session_manager.get_session(client_ip)
        if not session:
            return jsonify({'error': 'Session not found'}), 404

        return jsonify(session.get_session_info())

    except Exception as e:
        logger.error(f"Error getting session info for {client_ip}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/submit', methods=['POST'])
def submit_task():
    """Submit a new task"""
    try:
        client_ip = get_client_ip()
        data = request.get_json()

        if not data or 'description' not in data:
            return jsonify({'error': 'Task description required'}), 400

        description = data['description']
        task_type = data.get('type', 'USER_TRIGGERED')

        # Submit task
        task_id = session_manager.submit_task(client_ip, description, task_type)

        logger.info(f"Task submitted: {task_id} by {client_ip}")

        return jsonify({
            'task_id': task_id,
            'status': 'submitted',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error submitting task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    try:
        data = request.get_json()
        status = data.get('status', 'completed') if data else 'completed'

        session_manager.complete_task(task_id, status)

        logger.info(f"Task completed: {task_id} with status {status}")

        return jsonify({
            'task_id': task_id,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error completing task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/workspace/<client_ip>/validate', methods=['POST'])
def validate_file_access(client_ip):
    """Validate file access for user"""
    try:
        data = request.get_json()
        if not data or 'file_path' not in data:
            return jsonify({'error': 'File path required'}), 400

        file_path = data['file_path']
        is_valid = session_manager.validate_file_access(client_ip, file_path)

        return jsonify({
            'file_path': file_path,
            'access_allowed': is_valid,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error validating file access: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/all')
def get_all_sessions():
    """Get all session information (admin view)"""
    try:
        # This could be restricted to admin IPs
        sessions_info = session_manager.get_all_sessions_info()
        return jsonify(sessions_info)

    except Exception as e:
        logger.error(f"Error getting all sessions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/health')
def system_health():
    """Get system health information"""
    try:
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'active_sessions': len(session_manager.sessions),
            'active_tasks': len(session_manager.active_tasks),
            'websocket_connections': sum(len(clients) for clients in websocket_server.clients.values())
        }

        return jsonify(health_data)

    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/activity/log')
def get_activity_log():
    """Get recent activity log"""
    try:
        client_ip = get_client_ip()

        # Get last 50 activity entries visible to user
        activity_data = session_manager.activity_tracker.get_visible_activity(client_ip)

        # Add recent activity log entries
        recent_log = session_manager.activity_tracker.activity_log[-50:]

        return jsonify({
            'my_tasks': activity_data['my_tasks'],
            'network_activity': activity_data['network_activity'],
            'recent_log': recent_log,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error getting activity log: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

def create_app():
    """Application factory"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    return app

def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the web server"""
    logger.info(f"Starting LAN Session Web Server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='LAN Session Web Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    # Start WebSocket server in background
    websocket_server.run_server_threaded()

    # Start web server
    run_server(host=args.host, port=args.port, debug=args.debug)