# Engine Visibility Specification

## Overview
This specification outlines the implementation of per-node engine and model visibility in the Black Swarm Command Center dashboard. The enhancement provides real-time tracking of which inference engine and model each worker is using, along with selection reasoning and cost analytics.

## Implementation Details

### 1. Per-Worker Engine Display

Each worker card now displays:
- **Engine Type Badge**: Visual indicator showing CLAUDE 🧠, GROQ ⚡, or AUTO 🔄
- **Model Information**: Specific model being used (e.g., claude-sonnet-4, llama-3.3-70b)
- **Selection Reason**: Why this engine was chosen for the task

#### Visual Design
```html
<div class="worker-card">
    <div class="worker-header">
        <div class="worker-id">Worker 1</div>
        <div class="engine-badge engine-claude">
            🧠 CLAUDE
        </div>
    </div>
    <div class="worker-model">Model: claude-sonnet-4</div>
    <div class="worker-status">running</div>
    <div class="worker-task">Analyzing code patterns</div>
    <div class="worker-reason">Complex reasoning task</div>
</div>
```

#### Engine Badge Styling
- **Claude**: Orange background (#FF8C42), brain icon 🧠
- **Groq**: Blue background (#00D4FF), lightning icon ⚡
- **Auto**: Purple background (#8A2BE2), cycle icon 🔄

### 2. Engine Statistics Panel

New dedicated panel showing:
- **Claude Usage Percentage**: % of requests using Claude
- **Groq Usage Percentage**: % of requests using Groq
- **Total Cost**: Combined cost across engines
- **Average Response Time**: Mean response time in milliseconds
- **Cost Breakdown Bar**: Visual representation of cost distribution

#### Panel Layout
```html
<div class="panel engine-stats">
    <h2>Engine Statistics</h2>
    <div class="engine-metrics">
        <div class="engine-metric claude-metric">
            <div class="metric-value">65%</div>
            <div class="metric-label">Claude Usage</div>
        </div>
        <div class="engine-metric groq-metric">
            <div class="metric-value">35%</div>
            <div class="metric-label">Groq Usage</div>
        </div>
        <!-- Additional metrics... -->
    </div>
    <div class="cost-breakdown">
        <span class="cost-label">Claude</span>
        <div class="cost-bar">
            <div class="cost-bar-fill" style="width: 65%"></div>
        </div>
        <span class="cost-label">Groq</span>
    </div>
</div>
```

### 3. Real-Time Updates via SSE

The dashboard receives real-time updates containing:
```json
{
    "workers": [
        {
            "id": "1",
            "engine": "CLAUDE",
            "model": "claude-sonnet-4",
            "status": "running",
            "current_task": "Analyzing code patterns",
            "selection_reason": "Complex reasoning task"
        }
    ],
    "engine_stats": {
        "claude_usage_percent": 65,
        "groq_usage_percent": 35,
        "total_cost": 2.45,
        "avg_response_time": 1250,
        "claude_cost": 1.89,
        "groq_cost": 0.56
    }
}
```

### 4. Engine Selection Logic

The enhanced progress server implements intelligent engine detection based on:

#### Task Content Analysis
- **Claude Triggers**: "claude", "sonnet", "complex", "reasoning", "analysis", "creative"
- **Groq Triggers**: "groq", "llama", "fast", "quick", "simple", "extract", "format"

#### Selection Reasons
- `"Complex reasoning task"` - Claude for analytical work
- `"Speed optimization"` - Groq for fast processing
- `"Budget optimization"` - Groq for cost savings
- `"Creative/analytical task"` - Claude for creativity
- `"Simple processing"` - Groq for basic tasks

### 5. Cost Analytics

#### Real-Time Cost Tracking
- **Per-Engine Costs**: Separate tracking for Claude vs Groq
- **Usage Patterns**: Request count by engine type
- **Model Distribution**: Which models are used most frequently
- **Response Times**: Performance metrics per engine

#### Cost Estimation
- **Claude**: ~$0.015 per request (estimated average)
- **Groq**: ~$0.002 per request (estimated average)
- **Real-time Updates**: Cost accumulation shown in dashboard

### 6. Data Sources

#### Log File Analysis
The server analyzes grind logs to extract:
- Engine usage patterns from log entries
- Model information from task descriptions
- Performance metrics (response times)
- Cost accumulation over time

#### Enhanced Worker Data
```python
def get_enhanced_worker_data():
    """Get worker data enhanced with engine/model information."""
    # Analyze task content
    # Determine engine type
    # Extract model information
    # Add selection reasoning
    return enhanced_workers
```

### 7. API Endpoints

#### `/status` - Enhanced Status
Returns complete dashboard data including engine statistics:
```json
{
    "active_workers": {...},
    "engine_stats": {...},
    "workers": {...}
}
```

#### `/events` - Server-Sent Events
Real-time stream of updates including engine changes and cost updates.

### 8. Visual Enhancements

#### Color Scheme
- **Claude Orange**: `#FF8C42` - Warmth, intelligence
- **Groq Blue**: `#00D4FF` - Speed, efficiency
- **Auto Purple**: `#8A2BE2` - Flexibility, automation

#### Animations
- **Rainbow Border**: Running workers get animated rainbow border
- **Engine Badges**: Smooth hover effects and transitions
- **Cost Bar**: Animated width changes based on usage distribution

### 9. Responsive Design

#### Mobile Adaptations
- Engine badges remain visible on small screens
- Statistics panel adapts to single column
- Worker cards maintain engine visibility

#### Accessibility
- Engine badges include text labels and icons
- Color-blind friendly design with icons + text
- Proper ARIA labels for screen readers

### 10. Future Enhancements

#### Planned Features
- **Model Performance**: Response time by model type
- **Cost Predictions**: Projected costs based on usage patterns
- **Engine Recommendations**: Suggested engine for new tasks
- **Historical Analytics**: Long-term usage trend analysis

#### Integration Points
- **Live Model Switching**: Real-time engine changes during execution
- **Budget Alerts**: Warnings when approaching cost limits
- **Performance Optimization**: Automatic engine selection based on load

## Files Modified/Created

1. **dashboard_enhanced.html** - Enhanced dashboard with engine visibility
2. **progress_server_enhanced.py** - Server with engine tracking capabilities
3. **ENGINE_VISIBILITY_SPEC.md** - This specification document

## Testing & Validation

### Manual Testing
1. Start enhanced progress server: `python progress_server_enhanced.py`
2. Open dashboard at `http://localhost:8080`
3. Verify engine badges appear on worker cards
4. Check engine statistics panel updates
5. Confirm real-time updates via SSE

### Expected Behavior
- Worker cards show engine type with appropriate colors/icons
- Engine statistics panel displays usage percentages
- Cost breakdown bar reflects actual usage distribution
- Real-time updates maintain engine information consistency

## Performance Considerations

### Optimization Strategies
- **Efficient Log Parsing**: Only analyze recent log files
- **Cached Statistics**: Store computed stats to avoid recalculation
- **Selective Updates**: Only broadcast changes, not full state
- **Memory Management**: Limit response time history buffer

### Scalability Notes
- Dashboard supports up to 50 concurrent workers
- SSE connections automatically cleaned up on disconnect
- Log analysis limited to recent 20 files for performance

## Security & Safety

### Data Privacy
- No sensitive API keys exposed in dashboard
- Engine selection reasoning provides transparency
- Cost information aggregated, not detailed billing data

### Fail-Safe Behavior
- Defaults to "AUTO" engine if detection fails
- Graceful degradation if engine stats unavailable
- Fallback to standard dashboard if enhanced features fail

## Conclusion

The engine visibility enhancement provides critical transparency into the Black Swarm's inference engine usage, enabling better resource allocation, cost optimization, and performance monitoring. The implementation maintains backward compatibility while adding powerful new analytics capabilities.