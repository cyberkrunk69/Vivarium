# DUAL-SERVER ARCHITECTURE (ADMIN + LAN)


## Architecture Diagram (ASCII)
```
  +---------------+
  |  Laptop     |
  |  (localhost) |
  +---------------+
           |
           |
           v
  +---------------+
  |  Admin Server  |
  |  (localhost:8080) |
  +---------------+
           |
           |
           v
  +---------------+
  |  LAN Server   |
  |  (0.0.0.0:8081) |
  +---------------+
           |
           |
           v
  +---------------+
  |  WiFi Users  |
  |  (restricted) |
  +---------------+
```


## Security Model
The system will have two servers with clear separation of privilege levels:

*   Admin Server (localhost:8080): This server will have full control and will only be accessible from the actual laptop.
*   LAN Server (0.0.0.0:8081): This server will have restricted functionality and will be accessible to WiFi users.


## API Endpoints for Each Server
### Admin Server (localhost:8080)

*   `GET /admin/dashboard`: Displays the admin dashboard
*   `POST /admin/users`: Creates a new user
*   `GET /admin/users`: Retrieves a list of all users
*   `PUT /admin/users/:id`: Updates a user
*   `DELETE /admin/users/:id`: Deletes a user

### LAN Server (0.0.0.0:8081)

*   `GET /lan/dashboard`: Displays the LAN dashboard
*   `GET /lan/data`: Retrieves data for the LAN user


## Session Management Design
The system will use session tracking per connected device. Each device will be assigned a unique session ID, which will be used to track the device's activity.


## IP-Based Access Control
The system will use IP-based access control to restrict access to the LAN server. Only devices with authorized IP addresses will be able to access the LAN server.