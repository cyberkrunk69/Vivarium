# Engine/Model Visibility Specification

## Overview

This specification documents the implementation of engine and model visibility in the Black Swarm Command Center dashboard. The system provides real-time tracking of inference engine selection, model usage, cost accumulation, and performance metrics across all worker nodes.

## Implementation Components

### 1. Enhanced Progress Server (`progress_server_enhanced.py`)

**Features:**
- Real-time engine selection tracking
- Per-worker engine/model visibility
- Cost accumulation monitoring
- Engine switch detection and logging
- SSE (Server-Sent Events) for live updates

**Key Classes:**
- `EngineTracker`: Main tracking class for engine usage
- `ThreadedServer`: Enhanced HTTP server with engine API endpoints

**API Endpoints:**
- `GET /`: Enhanced dashboard with engine visibility
- `GET /events`: SSE stream with engine data
- `POST /api/engine/record`: Record engine selections
- `GET /api/status`: Full dashboard data with engine info

### 2. Enhanced Dashboard (`dashboard_enhanced.html`)

**UI Components:**

#### Engine Distribution Panel
- Real-time usage bar showing Claude vs Groq distribution
- Live percentage calculations
- Cost breakdown by engine
- Total switches counter

#### Worker Cards with Engine Visibility
- Engine badges (CLAUDE/GROQ) with color coding
- Model names displayed prominently
- Selection reason explanations
- Per-worker cost accumulation
- Engine switch counters
- Real-time activity indicators

#### Visual Design Elements
- Color-coded engine indicators:
  - Claude: `#00ff94` (green)
  - Groq: `#ff6b35` (orange)
- Animated progress bars
- Real-time pulse animations
- Responsive grid layout

### 3. Engine Tracker Integration (`engine_tracker_integration.py`)

**Core Features:**
- Background tracking thread
- Real-time event recording
- Dashboard integration via HTTP API
- Session report generation
- Cost optimization tracking

**Key Methods:**
- `record_engine_selection()`: Log engine choices
- `record_cost_update()`: Track spending
- `get_engine_distribution()`: Usage statistics
- `export_session_report()`: Comprehensive reporting

### 4. Summary Panel (`summary_panel.html`)

**Analytics Dashboard:**
- Interactive charts (Chart.js integration)
- Model usage distribution
- Cost timeline visualization
- Efficiency scoring
- Recent events timeline
- Performance metrics

## Data Structure

### Worker Engine Data

```json
{
  "worker_id": "worker_1",
  "engine_type": "CLAUDE",
  "model_name": "claude-sonnet-4",
  "selection_reason": "Complex analysis task",
  "cost_accumulated": 0.045,
  "engine_switches": 2,
  "engine_color": "claude"
}
```

### Engine Event

```json
{
  "worker_id": "worker_1",
  "event_type": "switch",
  "engine": "groq",
  "model": "llama-3.3-70b",
  "reason": "Speed optimization",
  "cost": 0.01,
  "timestamp": "2026-02-03T10:35:22.123Z"
}
```

### Engine Distribution Summary

```json
{
  "claude_percentage": 65.2,
  "groq_percentage": 34.8,
  "total_cost": 12.34,
  "claude_cost": 8.90,
  "groq_cost": 3.44,
  "total_switches": 23,
  "total_requests": 1247,
  "cost_savings": 8.54
}
```

## Real-time Features

### 1. Engine Selection Tracking
- Records every engine choice with reasoning
- Tracks model selection rationale
- Monitors cost implications

### 2. Switch Detection
- Identifies when workers change engines
- Logs switch reasoning
- Tracks switch frequency per worker

### 3. Cost Monitoring
- Real-time cost accumulation
- Per-engine spending breakdown
- Cost efficiency calculations

### 4. Performance Metrics
- Engine utilization percentages
- Average cost per request
- Switch rate analysis
- Efficiency scoring

## Integration Points

### 1. Unified Grind Spawner
The enhanced system integrates with `grind_spawner_unified.py` to capture engine selections:

```python
from engine_tracker_integration import record_engine_selection

# Record when an engine is selected
record_engine_selection(
    worker_id="worker_1",
    engine="claude",
    model="claude-sonnet-4",
    reason="Complex reasoning task",
    cost=0.05
)
```

### 2. Inference Engine
Integration with `inference_engine.py` for automatic tracking:

```python
# Engine selection is automatically tracked
result = engine.execute(prompt="Task", model="sonnet")
tracker.record_cost_update(worker_id, result.cost_usd)
```

### 3. Progress Server
The enhanced progress server provides real-time updates:

```python
# Broadcast engine updates to dashboard
broadcast_update()

# Send engine events via SSE
client['wfile'].write(f"data: {engine_data}\n\n".encode('utf-8'))
```

## Configuration

### Environment Variables
- `DASHBOARD_URL`: Target dashboard for engine tracking
- `ENGINE_TRACKING_ENABLED`: Enable/disable tracking
- `COST_ALERT_THRESHOLD`: Cost alert threshold

### Dashboard Settings
- Update intervals: 5 seconds (engine data), 1 second (worker states)
- Event retention: 1000 events
- Cost precision: 3 decimal places

## Usage Instructions

### 1. Launch Enhanced Dashboard

```bash
cd experiments/exp_20260203_103522_unified_session_13/
python progress_server_enhanced.py --lan
```

### 2. View Summary Analytics

```bash
# Open summary panel
open summary_panel.html
```

### 3. Export Session Report

```python
from engine_tracker_integration import export_session_report

# Generate comprehensive report
report = export_session_report()
print(f"Report saved with {len(report['event_timeline'])} events")
```

## Performance Considerations

### 1. Minimal Overhead
- Tracking adds <1ms per engine selection
- Background thread for dashboard updates
- Efficient JSON serialization

### 2. Memory Management
- Event history limited to 1000 items
- Automatic cleanup of old data
- Optimized data structures

### 3. Network Efficiency
- SSE for real-time updates
- Compressed JSON payloads
- Smart update batching

## Future Enhancements

### 1. Advanced Analytics
- Cost prediction models
- Engine performance correlation
- Optimization suggestions

### 2. Alert System
- Cost threshold alerts
- Performance degradation warnings
- Engine failure notifications

### 3. Historical Analysis
- Long-term usage trends
- Cost optimization reports
- Efficiency benchmarking

## Troubleshooting

### Common Issues

1. **Dashboard Not Updating**
   - Check SSE connection in browser dev tools
   - Verify progress server is running
   - Check firewall settings

2. **Missing Engine Data**
   - Ensure engine tracker is initialized
   - Verify integration in spawner code
   - Check API endpoint connectivity

3. **Cost Tracking Inaccurate**
   - Verify inference engine cost reporting
   - Check cost update recording
   - Review calculation logic

### Debug Commands

```bash
# Check server status
curl http://localhost:8080/api/status

# Test engine recording
curl -X POST http://localhost:8080/api/engine/record \
  -H "Content-Type: application/json" \
  -d '{"worker_id":"test","engine":"claude","model":"sonnet","reason":"test"}'

# View recent events
tail -f grind_logs/engine_events.log
```

## Security Considerations

### 1. Data Privacy
- No sensitive task content in engine logs
- Cost data aggregation only
- Worker ID anonymization option

### 2. Access Control
- Dashboard access controls
- API authentication (if enabled)
- Network security for LAN mode

### 3. Data Retention
- Configurable event retention
- Automatic cleanup of old data
- Export for archival purposes

## Conclusion

The Engine/Model Visibility system provides comprehensive real-time insight into inference engine usage, cost optimization, and performance characteristics. The implementation balances detailed visibility with minimal performance overhead, enabling effective monitoring and optimization of the Black Swarm AI system.

The modular design allows for easy integration with existing components while providing extensibility for future enhancements. The visual dashboard and analytics tools enable both real-time monitoring and historical analysis of engine usage patterns.