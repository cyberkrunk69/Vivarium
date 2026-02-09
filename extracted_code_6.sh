# File: /app/scripts/install_git_hooks.sh
#!/usr/bin/env bash
HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"
cat <<'EOF' > "$HOOKS_DIR/pre-push"
#!/usr/bin/env bash
# Placeholder hook – does nothing
exit 0
EOF
chmod +x "$HOOKS_DIR/pre-push"
echo "Pre‑push hook installed."