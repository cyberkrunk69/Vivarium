# Diagram Source Workflow

These architecture visuals are maintained as **draw.io source files** and exported
to committed SVG assets for stable GitHub rendering.

## Source of truth

- `docs/assets/diagrams/src/system-design.drawio`
- `docs/assets/diagrams/src/quest-lifecycle.drawio`
- `docs/assets/diagrams/src/task-review-state-machine.drawio`

## Exported artifacts

- `docs/assets/diagrams/system-design.svg`
- `docs/assets/diagrams/quest-lifecycle.svg`
- `docs/assets/diagrams/task-review-state-machine.svg`

## Update process

1. Edit the `.drawio` source file in diagrams.net or draw.io desktop.
2. Export fresh SVG files:

   ```bash
   make diagrams-export
   ```

3. Validate source/artifact integrity:

   ```bash
   make diagrams-validate
   ```

4. Commit both source (`src/*.drawio`) and exported SVG (`*.svg`) changes together.

## If draw.io CLI is unavailable

Run manual exports from diagrams.net:

- Open each file under `docs/assets/diagrams/src/`
- Export as **SVG**
- Save to matching filename in `docs/assets/diagrams/`

Keep filenames unchanged so README links remain stable.
