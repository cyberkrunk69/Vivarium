# Engine Visibility Specification
**Black Swarm Command Center - Enhanced Dashboard**

## Overview

This specification details the implementation of engine/model visibility in the Black Swarm dashboard, enabling real-time monitoring of inference engine selection, model usage, and cost tracking per worker node.

## Features Implemented

### 1. Per-Node Engine Information Display

Each worker/node card now displays:

#### Engine Type Indicator
- **Visual Badge**: Color-coded badge showing engine type
  - 🧠 **Claude**: Blue gradient badge (#3949ab)
  - ⚡ **Groq**: Orange gradient badge (#ff8f00)
- **Engine Name**: Text display (CLAUDE/GROQ)

#### Model Information
- **Model Name**: Specific model being used
  - Claude: `claude-sonnet-4`, `claude-haiku-4`, `claude-opus-4-5`
  - Groq: `llama-3.3-70b`, `mixtral-8x7b`, etc.
- **Selection Reason**: Why this engine was chosen
  - "Complex task" (Claude for sophisticated reasoning)
  - "Budget optimization" (Groq for cost efficiency)
  - "Speed priority" (Groq for fast inference)
  - "Auto-selected" (System decision)

#### Performance Metrics
- **Tokens Used**: Total tokens consumed this session
- **Session Cost**: Dollar amount spent ($0.0000 format)
- **Engine Switches**: Number of times engine changed during execution

### 2. Real-Time Updates via SSE/WebSocket

#### Engine Switch Indicators
- **Visual Notification**: Pulsing orange indicator when engine switches
- **Animation**: 1-second pulse effect on worker card
- **Sound Alert**: Optional audio notification (can be toggled)

#### Live Cost Tracking
- **Per-Engine Costs**: Separate tracking for Claude vs Groq spend
- **Real-time Updates**: Costs update as tokens are consumed
- **Budget Warnings**: Visual alerts when approaching budget limits

#### Model Usage Monitoring
- **Model Distribution**: Live chart of model usage across workers
- **Usage Patterns**: Historical data on model selection trends

### 3. Summary Panel with Usage Breakdown

#### Engine Distribution Cards
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 🧠 Claude Usage│ │ ⚡ Groq Usage  │ │ 💰 Total Cost  │
│      65%        │ │      35%        │ │    $0.0357     │
│   $0.0245       │ │   $0.0112       │ │   Combined     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

#### Model Distribution Chart
- **Bar Chart**: Visual representation of model usage
- **Live Updates**: Real-time changes as workers switch models
- **Click Interaction**: Detailed model information on click

## Technical Implementation

### 1. Data Collection Layer

#### Enhanced Wave Status Structure
```json
{
  "current_activity": {
    "workers": [
      {
        "id": "W01",
        "type": "Execution Worker",
        "task": "Implementing feature X",
        "engine": "CLAUDE",
        "model": "claude-sonnet-4",
        "selection_reason": "Complex task",
        "cost_this_session": 0.0245,
        "tokens_used": 12450,
        "engine_switches": 2
      }
    ]
  }
}
```

#### Engine Summary Statistics
```json
{
  "engine_summary": {
    "claude_percentage": 65.0,
    "groq_percentage": 35.0,
    "total_cost": 0.0357,
    "cost_breakdown": {
      "claude": 0.0245,
      "groq": 0.0112
    },
    "model_distribution": {
      "claude-sonnet-4": 3,
      "llama-3.3-70b": 2,
      "claude-haiku-4": 1
    },
    "engine_switches_today": 7
  }
}
```

### 2. Frontend Components

#### Enhanced Worker Card Structure
```html
<article class="enhanced-worker claude-worker">
  <div class="worker-header">
    <div class="worker-title">
      <span class="worker-id">W01</span>
      <span class="engine-badge engine-claude">
        <span class="engine-icon">🧠</span>
        <span class="engine-name">CLAUDE</span>
      </span>
    </div>
    <div class="worker-status"></div>
  </div>
  <div class="worker-details">
    <div class="detail-row">
      <span class="label">Model</span>
      <span class="value">claude-sonnet-4</span>
    </div>
    <div class="detail-row">
      <span class="label">Reason</span>
      <span class="value">Complex task</span>
    </div>
    <!-- Additional metrics -->
  </div>
  <div class="worker-task">Current task description</div>
</article>
```

#### CSS Animation Classes
```css
.engine-claude {
  background: linear-gradient(135deg, rgba(57, 73, 171, 0.3), rgba(57, 73, 171, 0.2));
  border: 1px solid #3949ab;
  color: #7986cb;
}

.engine-groq {
  background: linear-gradient(135deg, rgba(255, 143, 0, 0.3), rgba(255, 143, 0, 0.2));
  border: 1px solid #ff8f00;
  color: #ffb74d;
}

.engine-switch-indicator {
  animation: engineSwitch 1s ease-in-out;
}
```

### 3. Server-Side Integration

#### Enhanced Progress Server (`enhanced_progress_server.py`)
- **File Location**: `experiments/exp_20260203_103351_unified_session_13/enhanced_progress_server.py`
- **Port**: 8080 (same as original)
- **Endpoints**:
  - `/` - Enhanced dashboard
  - `/events` - SSE stream with engine data
  - `/api/status` - JSON API with enhanced worker info

#### Data Sources Integration
- **Wave Status**: Enhanced `wave_status.json` structure
- **Cost Tracking**: Integration with `cost_tracker.py`
- **Engine State**: New `unified_session_state.json` tracking
- **Real-time Updates**: File watcher monitoring engine state changes

## File Structure

```
experiments/exp_20260203_103351_unified_session_13/
├── enhanced_progress_server.py    # Backend server with engine visibility
├── enhanced_dashboard.html        # Standalone dashboard with full features
└── ENGINE_VISIBILITY_SPEC.md     # This specification document
```

## Integration with Existing System

### 1. Backward Compatibility
- **Original Dashboard**: Continues to work unchanged
- **Data Format**: Enhanced format is superset of original
- **API Endpoints**: New endpoints don't conflict with existing

### 2. Migration Path
1. **Phase 1**: Deploy enhanced server alongside original
2. **Phase 2**: Update worker data collection to include engine info
3. **Phase 3**: Switch to enhanced dashboard as default
4. **Phase 4**: Deprecate original dashboard (optional)

### 3. Configuration
```bash
# Run enhanced server
python experiments/exp_20260203_103351_unified_session_13/enhanced_progress_server.py

# Or with LAN access
python enhanced_progress_server.py --lan
```

## Usage Examples

### 1. Monitoring Engine Distribution
- **Real-time Percentages**: See Claude vs Groq usage split
- **Cost Tracking**: Monitor spend per engine type
- **Trend Analysis**: Observe engine selection patterns over time

### 2. Worker Performance Analysis
- **Model Effectiveness**: Compare task completion between models
- **Cost Efficiency**: Analyze cost per task by engine
- **Switch Frequency**: Monitor how often workers change engines

### 3. Budget Management
- **Live Cost Tracking**: Real-time spend monitoring
- **Engine Cost Comparison**: See cost differences between Claude/Groq
- **Budget Alerts**: Visual warnings when approaching limits

## Visual Design Principles

### 1. Brand Consistency
- **Black Swarm Colors**: Maintains existing brand palette
- **Engine-Specific Colors**: Claude (blue), Groq (orange)
- **Accessibility**: High contrast, readable fonts

### 2. Information Hierarchy
- **Primary**: Engine type and current task
- **Secondary**: Model name and selection reason
- **Tertiary**: Performance metrics and costs

### 3. Animation and Feedback
- **Hover Effects**: Subtle animations on interaction
- **State Changes**: Visual feedback for engine switches
- **Loading States**: Skeleton loaders and loading indicators

## Performance Considerations

### 1. Data Efficiency
- **SSE Streaming**: Efficient real-time updates
- **Differential Updates**: Only send changed data
- **Compression**: Gzip compression for responses

### 2. Rendering Optimization
- **Virtual Scrolling**: For large worker lists
- **Debounced Updates**: Prevent excessive re-renders
- **CSS Animations**: Hardware-accelerated transitions

## Future Enhancements

### 1. Advanced Analytics
- **Engine Performance Charts**: Historical performance data
- **Cost Prediction**: Forecast spending based on usage patterns
- **Efficiency Metrics**: Task completion rates per engine

### 2. Interactive Features
- **Manual Engine Selection**: Allow operators to force engine choice
- **Budget Controls**: Set per-engine spending limits
- **Alert Configuration**: Customizable notification settings

### 3. Integration Expansions
- **Slack Notifications**: Engine switch alerts
- **Metrics Export**: CSV/JSON data export
- **API Extensions**: Additional endpoints for third-party tools

## Security and Privacy

### 1. Data Protection
- **No Sensitive Data**: Only metadata and statistics exposed
- **Local Network Only**: Dashboard runs on local/LAN only
- **No External Requests**: All data stays within network

### 2. Access Control
- **Network-Level**: Firewall rules limit dashboard access
- **No Authentication**: Relies on network security
- **Read-Only**: Dashboard doesn't modify system state

## Conclusion

The Engine Visibility enhancement provides comprehensive real-time monitoring of inference engine selection and performance within the Black Swarm ecosystem. This enables:

- **Operational Transparency**: Clear visibility into engine choices
- **Cost Management**: Detailed tracking of spending by engine
- **Performance Optimization**: Data-driven engine selection decisions
- **User Experience**: Intuitive, visually appealing interface

The implementation maintains full backward compatibility while providing powerful new capabilities for monitoring and optimizing the Black Swarm's AI inference operations.