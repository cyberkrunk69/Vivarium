# ENGINE_VISIBILITY_SPEC.md
## Introduction
This document describes the UI changes made to display engine and model information for each node in the dashboard.

## Requirements
The dashboard should display the following information for each node:
* Engine type (CLAUDE or GROQ) with a visual indicator (badge/icon)
* Model name
* Selection reason

## UI Changes
The dashboard has been updated to include the required information for each node. The node cards now display the engine type, model name, and selection reason.

## Real-time Updates
The dashboard receives real-time updates via SSE/WebSocket, which update the node cards and summary panel.

## Summary Panel
The summary panel displays the total Claude vs Groq usage split, cost breakdown by engine, and model distribution chart.