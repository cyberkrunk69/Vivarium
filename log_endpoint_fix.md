# Log Endpoint Fix

### Insert the following code after the `@app.route('/progress-stream')` block:

```python
@app.route('/grind_logs/latest.log')
def serve_latest_grind_log():
    """Serve the most recent grind log."""
    grind_logs_dir = os.path.join(os.path.dirname(__file__), 'grind_logs')
    latest_log_file = max(glob.glob(os.path.join(grind_logs_dir, '*.json')), key=os.path.getmtime, default=None)
    
    if latest_log_file:
        with open(latest_log_file, 'r') as f:
            log_data = json.load(f)
            return Response(json.dumps(log_data), mimetype='application/json')
    else:
        return Response("", mimetype='text/plain', status=404)
```

This code adds a new route `/grind_logs/latest.log` that finds the most recent `*.json` file in the `grind_logs` directory, reads its contents, and returns it as `application/json`. If no log files exist, it returns an empty response with a 404 status code. The new route uses the same framework and pattern as the existing routes in the server.