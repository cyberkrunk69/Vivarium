# admin_app.py
app = FastAPI(title="Admin Server")
app.add_middleware(IPAccessControl, allowed_ips=["127.0.0.1"])
app.add_middleware(SessionTracker, store=admin_sessions)

# lan_app.py
app = FastAPI(title="LAN Server")
app.add_middleware(IPAccessControl, allowed_subnet="192.168.0.0/24")
app.add_middleware(SessionTracker, store=lan_sessions)