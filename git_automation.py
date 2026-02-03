"""
Git Automation Module for Swarm System

Provides automated git integration for version control of swarm-generated changes.
Automatically commits successful tasks to appropriate branches based on context.
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import logging

# Set up logging
logger = logging.getLogger(__name__)

class GitAutomation:
    """Handles automated git operations for swarm-generated changes."""

    def __init__(self, workspace: Union[str, Path]):
        self.workspace = Path(workspace)
        self.ensure_git_repo()

    def ensure_git_repo(self) -> None:
        """Ensure workspace is a git repository."""
        if not (self.workspace / ".git").exists():
            raise ValueError(f"Workspace {self.workspace} is not a git repository")

    def run_git_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run git command in workspace directory."""
        full_cmd = ["git"] + cmd
        try:
            result = subprocess.run(
                full_cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(full_cmd)}")
            logger.error(f"Error: {e.stderr}")
            raise

    def get_current_branch(self) -> str:
        """Get current git branch name."""
        result = self.run_git_command(["branch", "--show-current"])
        return result.stdout.strip()

    def branch_exists(self, branch_name: str) -> bool:
        """Check if branch exists locally."""
        result = self.run_git_command(["branch", "--list", branch_name], check=False)
        return bool(result.stdout.strip())

    def create_branch(self, branch_name: str, from_branch: str = "master") -> None:
        """Create new branch from specified base branch."""
        if self.branch_exists(branch_name):
            logger.info(f"Branch {branch_name} already exists")
            return

        # Ensure we're on the base branch first
        self.run_git_command(["checkout", from_branch])
        self.run_git_command(["checkout", "-b", branch_name])
        logger.info(f"Created branch {branch_name} from {from_branch}")

    def switch_to_branch(self, branch_name: str) -> None:
        """Switch to specified branch, creating if needed."""
        if not self.branch_exists(branch_name):
            self.create_branch(branch_name)

        current = self.get_current_branch()
        if current != branch_name:
            self.run_git_command(["checkout", branch_name])

    def get_pending_changes(self) -> Dict[str, List[str]]:
        """Get current git status - staged, unstaged, and untracked files."""
        # Get status in porcelain format for parsing
        result = self.run_git_command(["status", "--porcelain=v1"])

        staged = []
        unstaged = []
        untracked = []

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            # Porcelain format: XY filename
            # X = staged status, Y = unstaged status
            status = line[:2]
            filename = line[3:]

            if status[0] not in [' ', '?']:  # Staged changes
                staged.append(filename)
            if status[1] not in [' ', '?'] or status == '??':  # Unstaged or untracked
                if status == '??':
                    untracked.append(filename)
                else:
                    unstaged.append(filename)

        return {
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked
        }

    def get_diff_summary(self) -> Dict[str, str]:
        """Get git diff summary for staged and unstaged changes."""
        # Get staged diff
        staged_result = self.run_git_command(["diff", "--cached", "--stat"], check=False)
        staged_diff = staged_result.stdout.strip()

        # Get unstaged diff
        unstaged_result = self.run_git_command(["diff", "--stat"], check=False)
        unstaged_diff = unstaged_result.stdout.strip()

        return {
            "staged_diff": staged_diff,
            "unstaged_diff": unstaged_diff
        }

    def stage_files(self, files: Optional[List[str]] = None) -> None:
        """Stage specified files or all changes if files is None."""
        if files:
            for file in files:
                self.run_git_command(["add", file])
        else:
            # Stage all changes
            self.run_git_command(["add", "."])

    def auto_commit(self,
                   message: str,
                   files: Optional[List[str]] = None,
                   target_branch: str = "swarm-changes",
                   commit_type: str = "task") -> Dict[str, Union[str, bool]]:
        """
        Automatically commit changes to specified branch.

        Args:
            message: Commit message
            files: Optional list of specific files to commit
            target_branch: Branch to commit to (default: swarm-changes)
            commit_type: Type of commit (task, experiment, core, etc.)

        Returns:
            Dict with commit info and success status
        """
        try:
            # Get initial state
            original_branch = self.get_current_branch()
            changes_before = self.get_pending_changes()

            if not any(changes_before.values()):
                return {
                    "success": False,
                    "message": "No changes to commit",
                    "commit_hash": None,
                    "branch": target_branch
                }

            # Switch to target branch
            self.switch_to_branch(target_branch)

            # Stage files
            if files:
                self.stage_files(files)
            else:
                # Stage all changes
                self.stage_files()

            # Create commit with enhanced message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            enhanced_message = f"[{commit_type.upper()}] {message}\n\nAuto-committed by swarm system at {timestamp}"

            commit_result = self.run_git_command(["commit", "-m", enhanced_message])

            # Get commit hash
            hash_result = self.run_git_command(["rev-parse", "HEAD"])
            commit_hash = hash_result.stdout.strip()

            # Return to original branch if different
            if original_branch != target_branch:
                self.run_git_command(["checkout", original_branch])

            logger.info(f"Auto-committed to {target_branch}: {commit_hash[:8]}")

            return {
                "success": True,
                "message": f"Committed to {target_branch}",
                "commit_hash": commit_hash,
                "branch": target_branch,
                "files_committed": files or "all_changes"
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"Auto-commit failed: {e}")
            return {
                "success": False,
                "message": f"Commit failed: {e.stderr}",
                "commit_hash": None,
                "branch": target_branch
            }

    def create_pr(self,
                  source_branch: str,
                  target_branch: str = "master",
                  title: str = None,
                  body: str = None) -> Dict[str, Union[str, bool]]:
        """
        Create a pull request using GitHub CLI.

        Args:
            source_branch: Branch with changes
            target_branch: Target branch for PR
            title: PR title
            body: PR description

        Returns:
            Dict with PR info and success status
        """
        try:
            # Check if gh CLI is available
            gh_check = subprocess.run(["gh", "--version"], capture_output=True, text=True)
            if gh_check.returncode != 0:
                return {
                    "success": False,
                    "message": "GitHub CLI (gh) not available",
                    "pr_url": None
                }

            # Default title and body
            if not title:
                title = f"Swarm changes from {source_branch}"

            if not body:
                body = f"""# Swarm-generated changes

This PR contains changes automatically generated by the swarm system.

**Source branch:** `{source_branch}`
**Target branch:** `{target_branch}`
**Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Changes
- Auto-generated by swarm task execution
- Validated by quality metrics
- Ready for review

**Note:** This is an automated PR created by the swarm system.
"""

            # Create PR using gh CLI
            pr_cmd = [
                "gh", "pr", "create",
                "--base", target_branch,
                "--head", source_branch,
                "--title", title,
                "--body", body
            ]

            result = subprocess.run(
                pr_cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                check=True
            )

            # Extract PR URL from output
            pr_url = result.stdout.strip()

            logger.info(f"Created PR: {pr_url}")

            return {
                "success": True,
                "message": "Pull request created successfully",
                "pr_url": pr_url,
                "source_branch": source_branch,
                "target_branch": target_branch
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"PR creation failed: {e}")
            return {
                "success": False,
                "message": f"PR creation failed: {e.stderr}",
                "pr_url": None
            }

    def get_dashboard_data(self) -> Dict:
        """Get git status and diff data for dashboard display."""
        try:
            current_branch = self.get_current_branch()
            pending_changes = self.get_pending_changes()
            diff_summary = self.get_diff_summary()

            # Get recent commits (last 5)
            log_result = self.run_git_command([
                "log", "--oneline", "-5", "--pretty=format:%h|%s|%an|%ar"
            ], check=False)

            recent_commits = []
            if log_result.stdout.strip():
                for line in log_result.stdout.strip().split('\n'):
                    parts = line.split('|', 3)
                    if len(parts) == 4:
                        recent_commits.append({
                            "hash": parts[0],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3]
                        })

            # Check for swarm branches
            branch_result = self.run_git_command(["branch", "--list", "*swarm*", "*experiment*", "*pending*"], check=False)
            swarm_branches = [b.strip().lstrip('* ') for b in branch_result.stdout.split('\n') if b.strip()]

            return {
                "current_branch": current_branch,
                "pending_changes": pending_changes,
                "diff_summary": diff_summary,
                "recent_commits": recent_commits,
                "swarm_branches": swarm_branches,
                "total_changed_files": len(pending_changes["staged"]) + len(pending_changes["unstaged"]),
                "has_uncommitted_changes": bool(pending_changes["staged"] or pending_changes["unstaged"] or pending_changes["untracked"])
            }

        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {
                "error": str(e),
                "current_branch": "unknown",
                "pending_changes": {"staged": [], "unstaged": [], "untracked": []},
                "diff_summary": {"staged_diff": "", "unstaged_diff": ""},
                "recent_commits": [],
                "swarm_branches": [],
                "total_changed_files": 0,
                "has_uncommitted_changes": False
            }


# Convenience functions for easy import
def auto_commit(workspace: Union[str, Path],
               message: str,
               files: Optional[List[str]] = None,
               target_branch: str = "swarm-changes",
               commit_type: str = "task") -> Dict[str, Union[str, bool]]:
    """Convenience function for auto-committing changes."""
    git_auto = GitAutomation(workspace)
    return git_auto.auto_commit(message, files, target_branch, commit_type)


def create_pr(workspace: Union[str, Path],
              source_branch: str,
              target_branch: str = "master",
              title: str = None,
              body: str = None) -> Dict[str, Union[str, bool]]:
    """Convenience function for creating pull requests."""
    git_auto = GitAutomation(workspace)
    return git_auto.create_pr(source_branch, target_branch, title, body)


def get_pending_changes(workspace: Union[str, Path]) -> Dict[str, List[str]]:
    """Convenience function for getting pending changes."""
    git_auto = GitAutomation(workspace)
    return git_auto.get_pending_changes()


def get_dashboard_data(workspace: Union[str, Path]) -> Dict:
    """Convenience function for getting dashboard data."""
    git_auto = GitAutomation(workspace)
    return git_auto.get_dashboard_data()


# Branch routing logic
def determine_target_branch(task_description: str, quality_score: float = 0.0) -> str:
    """
    Determine appropriate target branch based on task type and quality.

    Args:
        task_description: Description of the task performed
        quality_score: Quality score from critic (0.0-1.0)

    Returns:
        Target branch name
    """
    task_lower = task_description.lower()

    # Core code changes requiring approval
    core_keywords = [
        "fix critical", "security", "breaking change", "api", "database",
        "authentication", "authorization", "payment", "production"
    ]

    # Experimental changes
    experiment_keywords = [
        "experiment", "prototype", "test", "poc", "proof of concept",
        "research", "exploration", "draft"
    ]

    # Check for core changes
    if any(keyword in task_lower for keyword in core_keywords):
        return "pending-review"

    # Check for experiments
    if any(keyword in task_lower for keyword in experiment_keywords):
        return "experiments"

    # High quality changes can go to main swarm branch
    if quality_score >= 0.8:
        return "swarm-changes"

    # Lower quality changes need review
    if quality_score < 0.6:
        return "pending-review"

    # Default to swarm-changes branch
    return "swarm-changes"


def commit_task_success(workspace: Union[str, Path],
                       task_description: str,
                       files_modified: List[str],
                       quality_score: float = 0.0,
                       session_id: int = 0) -> Dict[str, Union[str, bool]]:
    """
    Auto-commit successful task completion with intelligent branch routing.

    Args:
        workspace: Workspace directory
        task_description: Description of completed task
        files_modified: List of files that were modified
        quality_score: Quality score from critic
        session_id: Session ID for tracking

    Returns:
        Commit result info
    """
    target_branch = determine_target_branch(task_description, quality_score)

    commit_message = f"Complete: {task_description[:60]}..."
    if len(task_description) > 60:
        commit_message += f"\n\nFull task: {task_description}"

    commit_message += f"\n\nSession: {session_id}\nQuality: {quality_score:.2f}\nFiles: {len(files_modified)}"

    return auto_commit(
        workspace=workspace,
        message=commit_message,
        files=files_modified if files_modified else None,
        target_branch=target_branch,
        commit_type="task"
    )