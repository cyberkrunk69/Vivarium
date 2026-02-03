# Engine Visibility Specification

## Overview

This document specifies the implementation of per-node engine and model visibility in the Black Swarm Command Center dashboard. The enhancement provides real-time visibility into which inference engine (Claude or Groq) and model each worker is using, along with selection reasoning and usage statistics.

## Features Implemented

### 1. Per-Worker Engine Display

Each worker card now displays:

#### Engine Badge
- **Claude**: Orange badge (🧠) with "CLAUDE" text
- **Groq**: Blue badge (⚡) with "GROQ" text
- **Visual Styling**: Color-coded borders and backgrounds
- **Positioning**: Top-right corner of worker card

#### Model Information
- **Model Name**: Displayed in monospace font (e.g., `claude-sonnet-4`, `llama-3.3-70b`)
- **Selection Reason**: Italic text explaining why the engine was chosen
  - "Complex task" - for analytical/research work
  - "Budget optimization" - for cost-sensitive operations
  - "Fast execution" - for time-critical tasks
  - "Auto-selected" - default fallback

### 2. Real-Time Engine Switching

#### Visual Notifications
- **Flash Effect**: Yellow glow when engine switches occur
- **Badge Updates**: Immediate update of engine badge and model info
- **Console Logging**: Switch events logged to browser console

#### SSE Integration
- **Event Type**: `engine_switch`
- **Payload**:
  ```json
  {
    "worker_id": "worker_1",
    "from_engine": "groq",
    "to_engine": "claude",
    "reason": "Task complexity increased",
    "timestamp": "2026-02-03T10:30:40Z"
  }
  ```

### 3. Engine Usage Summary Panel

#### Distribution Metrics
- **Claude Percentage**: % of workers using Claude
- **Groq Percentage**: % of workers using Groq
- **Efficiency Score**: Cost vs usage optimization metric (0-100%)

#### Cost Breakdown
- **Claude Cost**: Total USD spent on Claude API calls
- **Groq Cost**: Total USD spent on Groq API calls
- **Token Usage**: Input/output tokens per engine

#### Model Distribution Chart
- **Horizontal Bar Chart**: Shows usage percentage per model
- **Color Coding**: Gradient from Claude orange to Groq blue
- **Real-time Updates**: Refreshes as workers switch models

### 4. Enhanced Data Structure

#### Worker Object Schema
```json
{
  "id": "worker_1",
  "status": "running",
  "current_task": "Analyzing code patterns",
  "engine": "claude",
  "model": "claude-sonnet-4",
  "selection_reason": "Complex task",
  "type": "ResearchWorker"
}
```

#### Engine Statistics Schema
```json
{
  "claude_percentage": 60.0,
  "groq_percentage": 40.0,
  "claude_cost": 0.234,
  "groq_cost": 0.089,
  "claude_tokens": 15420,
  "groq_tokens": 8930,
  "efficiency_score": 78.5,
  "model_distribution": {
    "claude-sonnet-4": 45.0,
    "claude-haiku-4": 15.0,
    "llama-3.3-70b": 30.0,
    "llama-3.1-8b": 10.0
  }
}
```

## Implementation Files

### Frontend Components

#### `dashboard_enhanced.html`
- **Enhanced Worker Cards**: Engine badges, model info, selection reasoning
- **Engine Summary Panel**: Usage distribution and cost breakdown
- **Real-time Updates**: SSE handling for engine switches
- **Model Chart**: Horizontal bar chart for model distribution

#### Styling Additions
- **Engine Colors**:
  - Claude: `--claude-primary: #ff7a4d`
  - Groq: `--groq-primary: #4d7fff`
- **Badge Styles**: Rounded badges with engine icons
- **Flash Effects**: Yellow glow for engine switches
- **Chart Components**: Progress bars with gradients

### Backend Components

#### `progress_server_enhanced.py`
- **Engine Data Extraction**: Parse grind logs for engine/model usage
- **Statistics Calculation**: Compute usage percentages and efficiency scores
- **Worker Enhancement**: Add engine/model fields to worker data
- **SSE Broadcasting**: Real-time engine switch notifications

#### Key Functions
- `extract_engine_info_from_logs()`: Parse logs for engine statistics
- `calculate_efficiency_score()`: Cost vs usage optimization metric
- `broadcast_engine_switch()`: Send real-time switch notifications
- `load_wave_status()`: Enhanced worker data with engine info

## Data Flow

### 1. Log Analysis
- **Source**: `grind_logs/*.json` files
- **Extraction**: Engine type, model name, costs, tokens
- **Processing**: Aggregate statistics and percentages

### 2. Worker Enhancement
- **Base Data**: Existing worker objects from wave_status.json
- **Enhancement**: Add engine, model, selection_reason fields
- **Inference**: Determine engine from task content if not specified

### 3. Real-time Updates
- **File Watching**: Monitor log files for changes
- **SSE Broadcasting**: Send updates to connected clients
- **UI Updates**: Immediate reflection in dashboard

## Usage Instructions

### Starting Enhanced Dashboard
```bash
cd experiments/exp_20260203_103040_unified_session_13/
python progress_server_enhanced.py --port 8080 --lan
```

### Viewing Engine Information
1. **Navigate** to http://localhost:8080
2. **Worker Cards** show engine badges and model info
3. **Engine Summary** panel displays usage statistics
4. **Real-time Updates** occur as workers switch engines

### Testing Engine Switches
```bash
# Trigger test engine switch notification
curl http://localhost:8080/api/engine-switch
```

## Configuration Options

### Engine Selection Logic
The enhanced server infers engine assignments based on:

1. **Task Content Analysis**:
   - Keywords: "groq", "fast", "cheap" → Groq
   - Keywords: "claude", "complex", "analysis" → Claude

2. **Worker Type**:
   - Research/Optimizer workers → Claude (better reasoning)
   - General workers → Groq (cost optimization)

3. **Default Fallback**:
   - Unknown tasks → Groq (budget optimization)

### Visual Customization
- **Engine Colors**: Modify CSS variables in dashboard_enhanced.html
- **Badge Styles**: Adjust `.engine-badge` classes
- **Chart Colors**: Update `.model-bar-fill` gradient

## Integration Notes

### Compatibility
- **Existing Systems**: Maintains compatibility with original progress_server.py
- **Data Sources**: Uses existing log files and wave_status.json
- **No Core Changes**: Does not modify core spawner files (read-only rule)

### Performance
- **Log Parsing**: Only processes 10 most recent log files
- **Memory Usage**: Minimal additional overhead
- **Update Frequency**: 1-second file monitoring, 30-second data refresh

### Security
- **Data Isolation**: Enhanced dashboard isolated in experiment directory
- **No Modifications**: Core system files remain untouched
- **Safe Defaults**: Graceful fallbacks for missing data

## Future Enhancements

### Potential Additions
1. **Historical Trends**: Engine usage over time
2. **Performance Metrics**: Response time per engine
3. **Cost Projections**: Budget burn rate predictions
4. **Model Recommendations**: Suggest optimal engine for task types
5. **Alert System**: Notifications for cost thresholds or failures

### Scaling Considerations
- **Multiple Workers**: Support for 50+ concurrent workers
- **Data Retention**: Log rotation and archival strategies
- **Load Balancing**: Engine selection optimization algorithms
- **Monitoring**: Health checks and performance metrics

## Testing Checklist

- [x] Worker cards display engine badges
- [x] Model names shown in monospace font
- [x] Selection reasoning displayed
- [x] Engine summary panel functional
- [x] Cost breakdown by engine
- [x] Model distribution chart
- [x] Real-time SSE updates
- [x] Engine switch notifications
- [x] Log file parsing
- [x] Statistics calculation
- [x] Responsive design
- [x] Error handling for missing data

## Conclusion

The Engine Visibility implementation provides comprehensive insight into the Black Swarm's inference engine usage, enabling operators to monitor cost optimization, understand engine selection logic, and track real-time performance. The enhancement maintains system stability while adding powerful observability features.