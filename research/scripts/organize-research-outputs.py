"""
CC-Switch organize_research_outputs.py
Cross-platform version with Windows/macOS/Linux support.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def detect_platform() -> str:
    import platform
    system = platform.system().lower()
    if system == "windows" or os.name == "nt":
        return "windows"
    return "posix"


def get_codex_base() -> Path:
    """Get the .codex base directory."""
    env_base = os.environ.get("CODEX_BASE", "")
    if env_base:
        return Path(env_base)
    home = Path.home()
    if (home / ".claude").exists():
        return home / ".claude"
    return home / ".codex"


def resolve_workspace_path(base: str | Path) -> Path:
    if isinstance(base, str):
        base = Path(base)
    if base.is_absolute():
        return base
    return (get_codex_base() / base).resolve()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_legacy_outputs(workspace: Path) -> list[Path]:
    """Find scattered output files in legacy paper/ directory."""
    legacy_dir = workspace / "outputs" / "paper"
    if not legacy_dir.exists():
        return []

    # Find loose .md files that should be in a project
    loose_files = []
    for pattern in ["*.md", "*.json"]:
        loose_files.extend(legacy_dir.glob(pattern))

    return loose_files


def infer_project_key(files: list[Path]) -> str:
    """Infer project key from file names."""
    for f in files:
        name = f.stem.lower()
        if "brief" in name:
            return "project_brief"
        if "draft" in name:
            return "draft_zh"
        if "review" in name:
            return "review_loop"
    return "legacy"


def organize_scattered(workspace: Path, dry_run: bool = False) -> dict[str, Any]:
    """Organize scattered output files into proper project structure."""
    legacy_dir = workspace / "outputs" / "paper"

    if not legacy_dir.exists():
        return {"status": "no_legacy", "message": "No legacy directory found"}

    loose_files = find_legacy_outputs(workspace)
    if not loose_files:
        return {"status": "clean", "message": "No loose files found"}

    project_key = infer_project_key(loose_files)
    project_dir = workspace / "outputs" / "projects" / project_key / "paper"

    if not dry_run:
        project_dir.mkdir(parents=True, exist_ok=True)

        for f in loose_files:
            dest = project_dir / f.name
            if dest.exists():
                # Backup existing
                backup = project_dir / f"{f.stem}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}{f.suffix}"
                shutil.copy2(dest, backup)
            shutil.copy2(f, dest)

        # Update ACTIVE_PROJECT
        active_json = workspace / "outputs" / "ACTIVE_PROJECT.json"
        active_data = {
            "project_key": project_key,
            "paper_dir": str(project_dir),
            "migrated_at": datetime.now().isoformat(),
        }
        save_json(active_json, active_data)

    return {
        "status": "organized",
        "project_key": project_key,
        "files_moved": len(loose_files),
        "destination": str(project_dir),
    }


def sync_projects(workspace: Path) -> dict[str, Any]:
    """Sync projects index."""
    projects_dir = workspace / "outputs" / "projects"
    if not projects_dir.exists():
        return {"status": "no_projects", "projects": []}

    projects = []
    for proj_dir in projects_dir.iterdir():
        if proj_dir.is_dir():
            paper_dir = proj_dir / "paper"
            projects.append({
                "key": proj_dir.name,
                "path": str(proj_dir),
                "has_paper": paper_dir.exists(),
                "files": [f.name for f in paper_dir.glob("*")] if paper_dir.exists() else [],
            })

    # Update PROJECT_INDEX
    index_file = workspace / "outputs" / "PROJECT_INDEX.json"
    index_data = {
        "updated_at": datetime.now().isoformat(),
        "projects": projects,
    }
    save_json(index_file, index_data)

    return {"status": "synced", "projects": len(projects)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Organize research outputs")
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--Command", choices=["sync", "organize", "check"], default="sync")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.workspace:
        workspace = resolve_workspace_path(args.workspace)
    else:
        workspace = get_codex_base() / "research-workspace"

    if args.Command == "organize":
        result = organize_scattered(workspace, dry_run=args.dry_run)
    elif args.Command == "check":
        loose = find_legacy_outputs(workspace)
        result = {"status": "check", "loose_files": len(loose), "files": [str(f) for f in loose]}
    else:
        # sync
        org_result = organize_scattered(workspace, dry_run=args.dry_run)
        idx_result = sync_projects(workspace)
        result = {"organize": org_result, "sync": idx_result}

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
