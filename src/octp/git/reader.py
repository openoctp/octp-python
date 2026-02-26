from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass
import git


@dataclass
class RepoInfo:
    commit_hash: str
    repository: str
    branch: str
    root: Path


def read_repo(path: Path = Path(".")) -> RepoInfo:
    """Read current git repository state."""
    try:
        repo = git.Repo(path, search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        raise RuntimeError(
            "Not inside a git repository. Run octp from within a git project."
        )

    commit_hash = repo.head.commit.hexsha

    # Normalise remote URL to platform/org/repo format
    repository = _parse_remote(repo)

    branch = repo.active_branch.name if not repo.head.is_detached else "detached"
    root = Path(repo.working_dir)

    return RepoInfo(
        commit_hash=commit_hash,
        repository=repository,
        branch=branch,
        root=root,
    )


def _parse_remote(repo: git.Repo) -> str:
    """Extract platform/org/repo from remote URL."""
    try:
        remote_url = repo.remotes.origin.url
    except (AttributeError, IndexError):
        return "unknown/unknown/unknown"

    # Handle SSH: git@github.com:org/repo.git
    ssh = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", remote_url)
    if ssh:
        host = ssh.group(1)
        path = ssh.group(2)
        return f"{host}/{path}"

    # Handle HTTPS: https://github.com/org/repo.git
    https = re.match(r"https?://([^/]+)/(.+?)(?:\.git)?$", remote_url)
    if https:
        host = https.group(1)
        path = https.group(2)
        return f"{host}/{path}"

    return remote_url
