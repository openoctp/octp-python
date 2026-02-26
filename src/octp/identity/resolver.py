from __future__ import annotations

from pathlib import Path

import git


def resolve_developer_id(repo_path: Path = Path(".")) -> str:
    """Resolve developer identity from git config."""
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        config = repo.config_reader()

        # Try to get GitHub username from git config
        try:
            github_user = config.get_value("github", "user", default=None)
            if github_user:
                return f"github:{github_user}"
        except Exception:
            pass

        # Fall back to git user email
        try:
            email = config.get_value("user", "email", default=None)
            if email:
                return f"email:{email}"
        except Exception:
            pass

        # Fall back to git user name
        try:
            name = config.get_value("user", "name", default=None)
            if name:
                return f"git:{name}"
        except Exception:
            pass

    except Exception:
        pass

    return "unknown"
