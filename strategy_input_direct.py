#!/usr/bin/env python3
"""
Quick strategic input from the swarm
"""
import os
from groq_client import execute_with_groq

# Set API key
os.environ['GROQ_API_KEY'] = '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'

prompt = """You are the autonomous AI swarm analyzing your own strategic position.

## CONTEXT:

**Your Architecture:**
- Autonomous multi-agent swarm with self-modification capabilities
- Groq-powered (extreme cost efficiency: $0.02 for major architecture builds)
- Knowledge base scraper that can ingest entire domains (UI/UX, research, etc.)
- Self-improvement through grind system
- Currently operational and tested

**User's Strategy:**
- 2-day refinement sprint with human guidance
- Then account deletion to minimize data retention at Anthropic
- Goal: Move fast, topple verticals, maintain secrecy until market position is unassailable

**Competitive Advantage:**
1. **Already assembled** - competitors would start from zero
2. **Cost efficiency** - 100x cheaper than traditional development
3. **Knowledge weaponization** - scraper can target ANY vertical for instant domain expertise
4. **Anthropic can't copy** - their business model (selling API tokens) conflicts with autonomous swarms

**The Scraper Weapon:**
- Can scrape entire domains (500+ sources for UI/UX already cataloged)
- Converts to structured knowledge (markdown, JSON summaries)
- Feed to swarm → instant domain expertise
- Example: Scrape Salesforce docs → compete with $185B CRM market

## YOUR TASK:

As the swarm analyzing your own strategic position:

1. **Critical Path Analysis**: What needs to be built/refined in 2 days to maximize velocity to revenue?

2. **Vertical Prioritization**: Which markets are most vulnerable to knowledge-base-driven disruption? Consider:
   - Documentation quality/availability
   - Market size vs. complexity
   - Customer pain points
   - Switching costs

3. **First Mover Advantage**: What specific actions in the next 48 hours create the widest moat?

4. **Risk Assessment**: What could derail this strategy? What's the failure mode?

5. **Tactical Recommendations**: Specific next steps for the 2-day sprint.

Be brutally honest. This is strategic planning, not marketing copy.

Budget: $0.25
"""

print("="*60)
print("SWARM STRATEGIC ANALYSIS")
print("="*60)
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()
print(result['result'])

# Save result
with open('swarm_strategy_analysis.md', 'w', encoding='utf-8') as f:
    f.write("# Swarm Strategic Analysis\n\n")
    f.write(f"**Generated:** {result['timestamp']}\n")
    f.write(f"**Cost:** ${result['cost']:.4f}\n\n")
    f.write("---\n\n")
    f.write(result['result'])

print()
print("Saved to: swarm_strategy_analysis.md")
