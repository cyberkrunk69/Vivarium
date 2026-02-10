# LAN Session Isolation Design
## Overview
The goal of this design is to provide a secure and isolated environment for users connecting via LAN (WiFi). Each user will have their own session, separate from other users and the admin.

## Requirements
1. **Own Session**: Each user must have a separate session.
2. **Visibility**: Users must be able to see swarm activity across the whole surface.
3. **Clarity**: Users must be able to distinguish between tasks they triggered and background swarm activity.
4. **Isolation**: Users must not be able to affect the host machine or other users' machines.

## Architecture
### Per-IP Session Management
- Each user's session will be managed based on their IP address.
- A session will be created when a user connects via LAN, and it will be unique to their IP address.

### User Workspace Isolation
- Each user's workspace will be isolated from other users and the admin.
- This will prevent users from accessing or modifying other users' files or the host machine.

### Activity Tagging
- All activities will be tagged as either user-triggered or background swarm activity.
- This will allow users to clearly see what tasks they have triggered and what is happening in the background.

### Real-time Status
- A real-time status display will show 'Your tasks' vs 'Network activity'.
- This will provide users with a clear understanding of their own activities and the overall network activity.

## Implementation
The implementation of this design will involve creating a per-IP session management system, isolating user workspaces, tagging activities, and providing a real-time status display.