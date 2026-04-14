"""
CC-Switch Adapter: Cross-Platform Path Resolution for Codex + Copilot Chat

Detects current platform and provides unified path resolution.
Works on: Windows (Codex), macOS/Linux (Copilot Chat), WSL
"""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Optional


def detect_platform() -> str:
    """Detect current platform environment."""
    system = platform.system().lower()

    # Check for Windows (Codex on Windows)
    if system == "windows" or os.name == "nt":
        return "codex_windows"

    # Check for WSL
    if "wsl" in platform.release().lower() or os.environ.get("WSL_DISTRO_NAME"):
        return "copilot_wsl"

    # Check for Copilot Chat indicators
    home = Path.home()
    if (home / ".claude").exists() or (home / ".codex").exists():
        # Check if running as Copilot Chat
        if os.environ.get("GITHUB_COPILOT_CHAT"):
            return "copilot_chat"
        # Check for Copilot CLI
        if os.environ.get("COPILOT_CLI"):
            return "copilot_cli"
        return "copilot_default"

    # Native macOS/Linux
    return "unix"


def get_workspace_base() -> Path:
    """Get the base workspace directory for the current platform."""
    platform_type = detect_platform()

    if platform_type.startswith("codex"):
        # Windows Codex - use CODEX_BASE env or default to ~/.codex
        base = Path(os.environ.get("CODEX_BASE", str(Path.home() / ".codex")))
        return base

    elif platform_type.startswith("copilot"):
        # Copilot Chat - use ~/.codex
        return Path.home() / ".codex"

    else:
        # Unix/macOS
        return Path.home() / ".codex"


def get_research_workspace() -> Path:
    """Get the research workspace directory."""
    return get_workspace_base() / "research-workspace"


def get_skill_root() -> Path:
    """Get the research skill root directory."""
    return get_workspace_base() / "skills" / "research"


def resolve_path(path: str | Path) -> Path:
    """
    Resolve a path that may use ~ or environment variables.
    Returns an absolute Path object for the current platform.
    """
    if isinstance(path, str):
        # Expand ~ and environment variables
        expanded = os.path.expanduser(os.path.expandvars(path))
        path = Path(expanded)

    if path.is_absolute():
        return path.resolve()

    # Relative to workspace
    return (get_workspace_base() / path).resolve()


def to_posix_path(path: Path) -> str:
    """Convert a Path to POSIX-style string (for display/logging)."""
    try:
        return str(path.as_posix())
    except ValueError:
        return str(path).replace("\\", "/")


def get_output_dir(project_key: Optional[str] = None) -> Path:
    """
    Get the output directory for the current project.

    Args:
        project_key: Optional project identifier. If None, uses ACTIVE_PROJECT.

    Returns:
        Path to the active paper output directory.
    """
    workspace = get_research_workspace()
    outputs_dir = workspace / "outputs"

    if project_key:
        return outputs_dir / "projects" / project_key / "paper"

    # Check for active project marker
    active_md = outputs_dir / "ACTIVE_PROJECT.md"
    active_json = outputs_dir / "ACTIVE_PROJECT.json"

    if active_json.exists():
        import json
        try:
            with open(active_json) as f:
                data = json.load(f)
            paper_dir = data.get("paper_dir")
            if paper_dir and Path(paper_dir).exists():
                return Path(paper_dir)
        except (json.JSONDecodeError, OSError):
            pass

    if active_md.exists():
        # Parse ACTIVE_PROJECT.md for project key
        try:
            with open(active_md) as f:
                content = f.read()
            for line in content.splitlines():
                if line.strip().startswith("project_key:"):
                    key = line.split(":", 1)[1].strip()
                    return outputs_dir / "projects" / key / "paper"
        except OSError:
            pass

    # Legacy fallback
    return outputs_dir / "paper"


def get_invoke_script_path() -> str:
    """Get the path to invoke_research_role.py as a string for shell invocation."""
    script_path = get_skill_root() / "scripts" / "invoke_research_role.py"

    # For POSIX compatibility
    return str(script_path).replace("\\", "/")


def build_python_invocation(
    role: str,
    stage: str,
    user_request: str,
    workspace: Optional[str] = None,
    extra_args: Optional[list[str]] = None,
) -> str:
    """
    Build a cross-platform Python invocation command.

    Args:
        role: coordinator | executor | reviewer | supervisor
        stage: paper-intake | paper-architecture | paper-draft | ...
        user_request: The user's request string
        workspace: Optional workspace override
        extra_args: Optional additional arguments

    Returns:
        Shell command string suitable for current platform
    """
    import json

    platform_type = detect_platform()

    # Build base command
    script = get_invoke_script_path()
    workspace_arg = workspace or str(get_research_workspace())

    # Quote the user request properly
    request_json = json.dumps(user_request)[1:-1]  # Remove surrounding quotes

    cmd_parts = [
        "python",
        f'"{script}"' if " " in script else script,
        "--workspace",
        f'"{workspace_arg}"' if " " in workspace_arg else workspace_arg,
        "--role",
        role,
        "--stage",
        stage,
        "--user-request",
        f'"{request_json}"',
    ]

    if extra_args:
        cmd_parts.extend(extra_args)

    cmd = " ".join(cmd_parts)

    # For Windows, wrap in PowerShell-compatible form
    if platform_type == "codex_windows":
        return f'python "{script}" --workspace "{workspace_arg}" --role {role} --stage {stage} --user-request "{request_json}"'

    return cmd


# Platform-specific environment variable helpers
def get_env_or_default(env_var: str, default: str) -> str:
    """Get environment variable or return default."""
    return os.environ.get(env_var, default)


def is_figure_enabled() -> bool:
    """Check if figure integration is enabled."""
    return os.environ.get("ARIS_FIGURE_ENABLED", "true").lower() == "true"


def is_supplement_enabled() -> bool:
    """Check if supplement integration is enabled."""
    return os.environ.get("ARIS_SUPPLEMENT_ENABLED", "true").lower() == "true"


def get_max_rounds() -> int:
    """Get maximum review rounds."""
    return int(os.environ.get("ARIS_MAX_ROUNDS", "4"))


def get_positive_threshold() -> float:
    """Get positive assessment threshold."""
    return float(os.environ.get("ARIS_POSITIVE_THRESHOLD", "6.0"))


if __name__ == "__main__":
    # Test/diagnostic output
    import json

    info = {
        "platform": detect_platform(),
        "workspace_base": str(get_workspace_base()),
        "research_workspace": str(get_research_workspace()),
        "skill_root": str(get_skill_root()),
        "invoke_script": get_invoke_script_path(),
        "output_dir": str(get_output_dir()),
        "figure_enabled": is_figure_enabled(),
        "supplement_enabled": is_supplement_enabled(),
        "max_rounds": get_max_rounds(),
        "positive_threshold": get_positive_threshold(),
    }

    print(json.dumps(info, indent=2, ensure_ascii=False))
