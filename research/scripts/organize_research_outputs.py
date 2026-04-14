from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_WORKSPACE = Path.home() / ".codex" / "research-workspace"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def outputs_root(workspace: Path) -> Path:
    return workspace / "outputs"


def legacy_paper_dir(workspace: Path) -> Path:
    return outputs_root(workspace) / "paper"


def projects_dir(workspace: Path) -> Path:
    return outputs_root(workspace) / "projects"


def active_project_json_path(workspace: Path) -> Path:
    return outputs_root(workspace) / "ACTIVE_PROJECT.json"


def active_project_md_path(workspace: Path) -> Path:
    return outputs_root(workspace) / "ACTIVE_PROJECT.md"


def project_index_path(workspace: Path) -> Path:
    return outputs_root(workspace) / "PROJECT_INDEX.json"


def audit_log_path(workspace: Path) -> Path:
    return workspace / "logs" / "project_organizer_audit.jsonl"


def extract_project_title(project_brief_path: Path) -> str:
    if not project_brief_path.exists():
        return ""
    text = read_text(project_brief_path)
    patterns = [
        r"^##\s*课题名称\s*$\s*([^\r\n#]+)",
        r"^##\s*项目名称\s*$\s*([^\r\n#]+)",
        r"^- \s*项目名[：:]\s*([^\r\n#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match:
            candidate = match.group(1).strip()
            if candidate:
                return candidate
    return ""


def sanitize_project_key(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).strip()
    normalized = re.sub(r"[<>:\"/\\\\|?*\x00-\x1F]", "-", normalized)
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    normalized = normalized.strip("._-")
    if not normalized:
        normalized = "project-" + datetime.now().strftime("%Y%m%d")
    return normalized[:80]


def infer_stage_from_dir(paper_dir: Path) -> str:
    files = {path.name for path in paper_dir.glob("*.md")}
    if "project_brief.md" not in files or "claims_evidence_matrix.md" not in files:
        return "paper-intake"
    if "narrative_report_zh.md" not in files or "outline_zh.md" not in files:
        return "paper-architecture"
    if "draft_zh.md" not in files:
        return "paper-draft"
    return "paper-review-loop"


def ensure_project_dirs(workspace: Path, project_title: str) -> dict[str, str]:
    key = sanitize_project_key(project_title)
    root = projects_dir(workspace) / key
    paper_dir = root / "paper"
    runs_dir = root / "agent_runs"
    metadata_dir = root / "metadata"
    for path in (paper_dir, runs_dir, metadata_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "project_key": key,
        "project_title": project_title,
        "project_root": str(root),
        "paper_dir": str(paper_dir),
        "agent_runs_dir": str(runs_dir),
        "metadata_dir": str(metadata_dir),
    }


def write_active_project_files(workspace: Path, payload: dict[str, Any]) -> None:
    dump_json(active_project_json_path(workspace), payload)
    write_text(
        active_project_md_path(workspace),
        "# Active Project\n\n"
        f"- 项目名：{payload['project_title']}\n"
        f"- 项目标识：{payload['project_key']}\n"
        f"- 论文目录：{payload['paper_dir']}\n"
        f"- 运行记录目录：{payload['agent_runs_dir']}\n"
        f"- 更新时间：{payload['updated_at']}\n",
    )


def sync_root_into_project(workspace: Path, project_title: str | None = None) -> dict[str, Any]:
    root_paper = legacy_paper_dir(workspace)
    inferred_title = project_title or extract_project_title(root_paper / "project_brief.md")
    if not inferred_title:
        raise RuntimeError("Cannot infer project title from outputs/paper/project_brief.md. Provide --project-title.")

    record = ensure_project_dirs(workspace, inferred_title)
    project_paper = Path(record["paper_dir"])
    project_runs = Path(record["agent_runs_dir"])

    moved_markdown: list[str] = []
    moved_runs: list[str] = []

    for path in sorted(root_paper.glob("*.md")):
        destination = project_paper / path.name
        if destination.exists():
            destination.unlink()
        shutil.move(str(path), str(destination))
        moved_markdown.append(path.name)

    root_runs = root_paper / "agent_runs"
    if root_runs.exists():
        for path in sorted(root_runs.glob("*.json")):
            destination = project_runs / path.name
            if destination.exists():
                destination.unlink()
            shutil.move(str(path), str(destination))
            moved_runs.append(path.name)

    payload = {
        **record,
        "stage": infer_stage_from_dir(project_paper),
        "managed_markdown_files": moved_markdown,
        "managed_agent_run_files": moved_runs,
        "updated_at": now_iso(),
    }

    dump_json(Path(record["metadata_dir"]) / "project.json", payload)
    index = load_json(project_index_path(workspace), {"projects": {}})
    index.setdefault("projects", {})
    index["projects"][payload["project_key"]] = payload
    index["updated_at"] = now_iso()
    dump_json(project_index_path(workspace), index)
    write_active_project_files(workspace, payload)

    append_jsonl(
        audit_log_path(workspace),
        {
            "timestamp": now_iso(),
            "action": "sync",
            "project_key": payload["project_key"],
            "project_title": payload["project_title"],
            "managed_markdown_files": moved_markdown,
            "managed_agent_run_files": moved_runs,
        },
    )
    return payload


def activate_project(workspace: Path, project_key: str) -> dict[str, Any]:
    index = load_json(project_index_path(workspace), {"projects": {}})
    project = index.get("projects", {}).get(project_key)
    if not project:
        raise RuntimeError(f"Unknown project key: {project_key}")
    project["updated_at"] = now_iso()
    write_active_project_files(workspace, project)
    append_jsonl(
        audit_log_path(workspace),
        {
            "timestamp": now_iso(),
            "action": "activate",
            "project_key": project_key,
            "project_title": project["project_title"],
        },
    )
    return project


def status_payload(workspace: Path) -> dict[str, Any]:
    return {
        "active_project": load_json(active_project_json_path(workspace), {}),
        "projects": load_json(project_index_path(workspace), {"projects": {}}).get("projects", {}),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Organize research outputs into project-specific folders.")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--project-title")

    activate_parser = subparsers.add_parser("activate")
    activate_parser.add_argument("--project-key", required=True)

    subparsers.add_parser("status")
    return parser


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve()

    if args.command == "sync":
        print(json.dumps(sync_root_into_project(workspace, project_title=args.project_title), ensure_ascii=False, indent=2))
        return 0
    if args.command == "activate":
        print(json.dumps(activate_project(workspace, args.project_key), ensure_ascii=False, indent=2))
        return 0
    if args.command == "status":
        print(json.dumps(status_payload(workspace), ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
