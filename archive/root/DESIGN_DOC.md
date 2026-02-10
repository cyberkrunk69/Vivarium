# DESIGN_DOC.md
## Overview
The **Interdimensional Radio – 60‑Second TikTok Cut** demo consists of two
artifacts:

1. **`demo_scripts/tiktok_60s.json`** – a data‑only description of the scripted
   conversation.  It contains an ordered list of dialogue entries, each with:
   - `character`: Name of the speaker (e.g., “Host”, “Zane”, “Luna”, “Bot”, “Narrator”).
   - `line`: The exact text that should appear on screen.
   - `delay`: Seconds to wait **before** printing this line.  The delays are
     tuned so the whole script runs for roughly 60 seconds.

2. **`run_tiktok_demo.py`** – a tiny Python driver that:
   - Loads the JSON script.
   - Sleeps for the configured `delay`.
   - Prints each line with a bold speaker label.
   - Ends with the mandated “Link in bio” CTA.
   - Prints a start‑up banner and a final elapsed‑time summary.

The script is deliberately self‑contained (standard‑library only) and
auto‑plays without any user interaction, making it ideal for a screen‑recording
session.

## Scripted Conversation Highlights
- **Multiple characters** (5 distinct voices) give the demo a lively, radio‑show
  feel.
- **Natural interruptions** are simulated by short delays (e.g., a character
  cutting in mid‑sentence).
- **Humor & personality** are woven in via witty one‑liners and quirky
  inter‑dimensional references.
- The **“wow” moment** occurs when the AI Bot reveals an impossible fact,
  prompting an exaggerated gasp from the Host.
- The final line is the required **“Link in bio”** call‑to‑action.

## Timing Strategy
The JSON contains a cumulative delay of ~58 seconds; a final 2‑second pause
is left before the “Link in bio” line to hit the 60‑second target without
hard‑coding a final sleep in the Python driver.

## Usage