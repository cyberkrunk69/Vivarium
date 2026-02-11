"""Artifacts blueprint: list and view files created by residents."""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("artifacts", __name__, url_prefix="/api")


def _get_workspace():
    return current_app.config["WORKSPACE"]


@bp.route("/artifact/view")
def api_view_artifact():
    """View contents of a file artifact."""
    file_path = request.args.get("path", "")
    if not file_path:
        return jsonify({"success": False, "error": "No path provided"})
    WORKSPACE = _get_workspace()
    try:
        if not os.path.isabs(file_path):
            full_path = WORKSPACE / file_path
        else:
            full_path = Path(file_path)
        full_path = full_path.resolve()
        if not str(full_path).startswith(str(WORKSPACE.resolve())):
            return jsonify({"success": False, "error": "Access denied: path outside workspace"})
        if not full_path.exists():
            return jsonify({"success": False, "error": "File not found"})
        if not full_path.is_file():
            return jsonify({"success": False, "error": "Not a file"})
        if full_path.stat().st_size > 500 * 1024:
            return jsonify({"success": False, "error": "File too large (>500KB)"})
        ext = full_path.suffix.lower()
        file_type_map = {
            ".py": "python", ".js": "javascript", ".ts": "typescript", ".json": "json",
            ".md": "markdown", ".html": "html", ".css": "css", ".yaml": "yaml", ".yml": "yaml",
            ".sh": "bash", ".sql": "sql", ".txt": "text", ".log": "text",
        }
        file_type = file_type_map.get(ext, "text")
        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = full_path.read_text(encoding="latin-1")
        return jsonify({
            "success": True,
            "path": str(full_path.relative_to(WORKSPACE)),
            "filename": full_path.name,
            "content": content,
            "file_type": file_type,
            "size": full_path.stat().st_size,
            "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat(),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@bp.route("/artifacts/list")
def api_list_artifacts():
    """List recent artifacts (files created/modified by the swarm)."""
    WORKSPACE = _get_workspace()
    try:
        artifacts_by_path = {}

        def add_artifact(path_obj: Path, artifact_type: str) -> None:
            try:
                rel_path = str(path_obj.relative_to(WORKSPACE))
                modified = datetime.fromtimestamp(path_obj.stat().st_mtime).isoformat()
            except Exception:
                return
            existing = artifacts_by_path.get(rel_path)
            if not existing or str(existing.get("modified", "")) < modified:
                artifacts_by_path[rel_path] = {
                    "path": rel_path, "name": path_obj.name,
                    "type": artifact_type, "modified": modified,
                }

        journals_dir = WORKSPACE / ".swarm" / "journals"
        if journals_dir.exists():
            for f in sorted(journals_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                add_artifact(f, "journal")
        library_dir = WORKSPACE / "library" / "creative_works"
        if library_dir.exists():
            for f in sorted(library_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                add_artifact(f, "creative_work")
        community_root = WORKSPACE / "library" / "community_library"
        if community_root.exists():
            docs_dir = community_root / "swarm_docs"
            if docs_dir.exists():
                for f in sorted(docs_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                    add_artifact(f, "community_doc")
            suggestions_dir = community_root / "resident_suggestions"
            if suggestions_dir.exists():
                for f in sorted(suggestions_dir.glob("**/*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                    add_artifact(f, "community_doc")
        skills_dir = WORKSPACE / "skills"
        if skills_dir.exists():
            for f in sorted(skills_dir.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
                add_artifact(f, "skill")

        artifacts = sorted(
            artifacts_by_path.values(),
            key=lambda item: str(item.get("modified") or ""),
            reverse=True,
        )
        return jsonify({"success": True, "artifacts": artifacts[:120]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
