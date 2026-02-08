# Black Swarm Orchestrator

Minimal orchestrator for controlling the Black Swarm running at `http://127.0.0.1:8420`.

Quick start:
- `python brain.py grind --budget 0.10` to trigger a grind with a $0.10 budget
- `python brain.py health` to check swarm status

All runs are logged to `runs.json`.

## Gameplay + community systems (highlights)

**Hats (prompt overlays, infinite resource)**
- Hats augment behavior without changing identity.
- Includes the **Hat of Objectivity** for dispute mediation.
- Hat quality rules prevent identity override language.

**Guilds (formerly teams)**
- Join requests require **blind approval votes with reasons**.
- Guild leaderboards track bounties and earnings.
- Guild refund pools reward collective performance.

**Bounties + rivalry**
- Guilds and individuals can claim/compete on bounties.
- Control panel shows competing guild submissions.

**Journal economy (community reviewed)**
- Blind voting with required reasons.
- Refunds range from **50% to 2x** attempt cost.
- Gaming flags trigger temporary penalties.

**Dispute recourse**
- Vote outcomes can be disputed at personal risk.
- Disputes open a dedicated chatroom with an objective mediator.
- Upheld disputes can suspend privileges (e.g., Sunday bonus).

**Physics (immutable rules)**
- Reward scaling, punishment, and gravity constants are immutable.
- Prevents incentive tampering and maintains system reality.

## Key modules
- `swarm_enrichment.py` — tokens, guilds, bounties, journals, disputes
- `hats.py` — hat library + quality enforcement
- `control_panel.py` — bounty UI, chatrooms
