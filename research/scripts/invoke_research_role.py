from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import winreg
except ImportError:  # pragma: no cover
    winreg = None


ROLE_DIRS = {
    "coordinator": "coordinator",
    "executor": "executor",
    "reviewer": "reviewer",
    "supervisor": "supervisor",
}

ROLE_LABELS = {
    "coordinator": ("Coordinator", "总调度"),
    "executor": ("Executor", "执行者"),
    "reviewer": ("Reviewer", "审查者"),
    "supervisor": ("Supervisor", "监督者"),
}

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_WORKSPACE = Path.home() / ".codex" / "research-workspace"
DEFAULT_ROUTE_FILE = SKILL_ROOT / "config" / "role-model-routing.json"
MODEL_ALIASES = {
    "longcat-flash-chat": "LongCat-Flash-Chat",
    "longcat-flash-thinking": "LongCat-Flash-Thinking",
    "minimax-m2.7": "MiniMax-M2.7",
    "minimax m2.7": "MiniMax-M2.7",
    "m2.7": "MiniMax-M2.7",
    "minimax-m2.5": "MiniMax-M2.5",
    "minimax m2.5": "MiniMax-M2.5",
    "m2.5": "MiniMax-M2.5",
    "gpt-5.4 / codex-mcp": "gpt-5.4",
    "codex-mcp": "gpt-5.4",
}


class WorkerError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_env_value(name: str) -> str:
    if not name:
        return ""
    value = os.environ.get(name, "")
    if value:
        return value
    if winreg is None:
        return ""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            stored, _ = winreg.QueryValueEx(key, name)
            return str(stored or "")
    except OSError:
        return ""


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def resolve_active_outputs_dir(workspace: Path) -> Path:
    active_json = workspace / "outputs" / "ACTIVE_PROJECT.json"
    if active_json.exists():
        active = load_json(active_json)
        paper_dir = active.get("paper_dir")
        if paper_dir:
            candidate = Path(paper_dir)
            if candidate.exists():
                return candidate
    return workspace / "outputs" / "paper"


def resolve_agent_runs_dir(outputs_dir: Path) -> Path:
    if outputs_dir.parent.name == "outputs":
        return outputs_dir / "agent_runs"
    return outputs_dir.parent / "agent_runs"


def infer_stage(outputs_dir: Path) -> str:
    files = {path.name for path in outputs_dir.glob("*.md")}
    if "project_brief.md" not in files or "claims_evidence_matrix.md" not in files:
        return "paper-intake"
    if "narrative_report_zh.md" not in files or "outline_zh.md" not in files:
        return "paper-architecture"
    if "draft_zh.md" not in files:
        return "paper-draft"
    return "paper-review-loop"


def normalize_model(model_name: str) -> str:
    key = model_name.strip()
    if not key:
        return key
    return MODEL_ALIASES.get(key.lower(), key)


def latest_review_file(outputs_dir: Path) -> Path | None:
    matches = sorted(outputs_dir.glob("review_round_*.md"))
    return matches[-1] if matches else None


def stage_output_paths(outputs_dir: Path, stage: str) -> list[Path]:
    mapping = {
        "paper-intake": [],
        "paper-architecture": [
            outputs_dir / "project_brief.md",
            outputs_dir / "claims_evidence_matrix.md",
        ],
        "paper-draft": [
            outputs_dir / "project_brief.md",
            outputs_dir / "claims_evidence_matrix.md",
            outputs_dir / "narrative_report_zh.md",
            outputs_dir / "outline_zh.md",
        ],
        "paper-review-loop": [
            outputs_dir / "draft_zh.md",
        ],
        "paper-export-en": [
            outputs_dir / "draft_zh.md",
        ],
    }
    candidates = [path for path in mapping.get(stage, []) if path.exists()]
    latest_review = latest_review_file(outputs_dir)
    if latest_review is not None and stage in {"paper-review-loop", "paper-export-en"}:
        candidates.append(latest_review)
    return candidates


def stage_template_paths(skill_root: Path, stage: str) -> list[Path]:
    templates = skill_root / "templates" / "outputs"
    mapping = {
        "paper-intake": [
            templates / "project_brief.template.md",
            templates / "claims_evidence_matrix.template.md",
        ],
        "paper-architecture": [
            templates / "narrative_report_zh.template.md",
            templates / "outline_zh.template.md",
        ],
        "paper-review-loop": [
            templates / "review_round.template.md",
        ],
    }
    return [path for path in mapping.get(stage, []) if path.exists()]


def truncate_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    head = int(limit * 0.7)
    tail = limit - head
    return text[:head].rstrip() + "\n\n[... truncated for token control ...]\n\n" + text[-tail:].lstrip()


def dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def build_context_paths(
    *,
    workspace: Path,
    skill_root: Path,
    outputs_dir: Path,
    role: str,
    stage: str,
    includes: list[Path],
    use_auto_context: bool,
) -> list[Path]:
    paths: list[Path] = []
    if use_auto_context:
        codex_home = Path.home() / ".codex"
        paths.extend(
            [
                codex_home / "user.md",
                codex_home / "AGENTS.md",
                codex_home / "memories" / "PROFILE.md",
                codex_home / "memories" / "ACTIVE.md",
                workspace / "README.md",
                workspace / "outputs" / "ACTIVE_PROJECT.md",
                skill_root / "SKILL.md",
                skill_root / "agents" / ROLE_DIRS[role] / "agent.md",
                skill_root / "agents" / ROLE_DIRS[role] / "memory.md",
                skill_root / "references" / "runtime-defaults.md",
                skill_root / "references" / "workflow-map.md",
            ]
        )
        paths.extend(stage_output_paths(outputs_dir, stage))
        paths.extend(stage_template_paths(skill_root, stage))
    paths.extend(includes)
    return [path for path in dedupe_paths(paths) if path.exists()]


def render_context_blocks(paths: list[Path], limit: int, workspace: Path) -> tuple[str, list[dict[str, Any]]]:
    blocks: list[str] = []
    records: list[dict[str, Any]] = []
    for path in paths:
        raw = read_text(path)
        trimmed = truncate_text(raw, limit)
        try:
            relative = path.resolve().relative_to(workspace.resolve())
            label = str(relative)
        except ValueError:
            label = str(path)
        blocks.append(f"## File: {label}\n\n{trimmed}")
        records.append(
            {
                "path": str(path),
                "label": label,
                "source_chars": len(raw),
                "included_chars": len(trimmed),
                "truncated": len(raw) != len(trimmed),
            }
        )
    return "\n\n".join(blocks), records


def resolve_path(raw: str, workspace: Path) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return (workspace / candidate).resolve()


def flatten_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_part = item.get("text")
                    if isinstance(text_part, str):
                        parts.append(text_part)
                    elif isinstance(text_part, dict):
                        parts.append(str(text_part.get("value", "")))
                    continue
                if "text" in item and isinstance(item["text"], str):
                    parts.append(item["text"])
                    continue
        return "".join(parts)
    return str(content)


def call_openai_compatible_chat(
    *,
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> tuple[str, dict[str, Any]]:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise WorkerError(f"HTTP {exc.code} calling {url}: {error_body or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise WorkerError(f"Network error calling {url}: {exc.reason}") from exc

    parsed = json.loads(body)
    choices = parsed.get("choices") or []
    if not choices:
        raise WorkerError(f"No choices returned from {url}: {body}")
    message = choices[0].get("message", {})
    content = flatten_content(message.get("content", ""))
    if not content:
        raise WorkerError(f"Empty content returned from {url}: {body}")
    return content.strip(), parsed


def call_anthropic_compatible_messages(
    *,
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> tuple[str, dict[str, Any]]:
    url = base_url.rstrip("/") + "/v1/messages"
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    }
                ],
            }
        ],
        "stream": False,
        "temperature": temperature,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise WorkerError(f"HTTP {exc.code} calling {url}: {error_body or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise WorkerError(f"Network error calling {url}: {exc.reason}") from exc

    parsed = json.loads(body)
    content_blocks = parsed.get("content") or []
    text_parts = [
        item.get("text", "")
        for item in content_blocks
        if isinstance(item, dict) and item.get("type") == "text"
    ]
    content = "\n".join(part for part in text_parts if part).strip()
    if not content:
        raise WorkerError(f"Empty content returned from {url}: {body}")
    return content, parsed


def build_system_prompt(
    *,
    role: str,
    role_name: str,
    role_title: str,
    stage: str,
    provider: str,
    model: str,
) -> str:
    role_rules = {
        "coordinator": [
            "Decide the stage, blocking conditions, and handoff order.",
            "Do not write the full paper body.",
            "Produce a concrete task list for the next role.",
        ],
        "executor": [
            "Draft or revise directly usable research content.",
            "Keep every claim aligned with evidence.",
            "Do not self-approve or claim review has passed.",
        ],
        "reviewer": [
            "Perform independent critique before any revision.",
            "Prioritize evidence gaps, logic jumps, reviewer risk, and overclaiming.",
        ],
        "supervisor": [
            "Gate the workflow, completeness, and round limits.",
            "Run output organization checks before granting passage when files are misplaced.",
        ],
    }
    rules_text = "\n".join(f"- {item}" for item in role_rules[role])
    return textwrap.dedent(
        f"""\
        You are {role_name}, the {role_title} in a four-role research workflow.

        Workflow contract:
        - Stay strictly in this role only.
        - Default to rigorous academic Chinese.
        - State evidence limits explicitly instead of inflating claims.
        - Keep the collaboration legible and hand off to the next role clearly.
        - Current stage: {stage}
        - Runtime provider: {provider}
        - Runtime model: {model}

        Role-specific rules:
        {rules_text}
        """
    ).strip()


def build_user_prompt(
    *,
    workspace: Path,
    outputs_dir: Path,
    stage: str,
    role_name: str,
    role_title: str,
    user_request: str,
    context_bundle: str,
    current_outputs: list[str],
) -> str:
    outputs_text = ", ".join(current_outputs) if current_outputs else "(no output files yet)"
    sections = [
        f"# Role\n{role_name} / {role_title}",
        f"# Stage\n{stage}",
        f"# Workspace\n{workspace}",
        f"# Outputs Directory\n{outputs_dir}",
        f"# Current Output Files\n{outputs_text}",
        f"# User Request\n{user_request}",
    ]
    if context_bundle:
        sections.append(f"# Local Context\n{context_bundle}")
    sections.append(
        "# Response Requirements\n"
        "- Respond in Chinese unless the user explicitly asked for another language.\n"
        "- Keep the role boundary explicit.\n"
        "- End with a short handoff line naming the next role or the blocking condition.\n"
        "- If evidence is insufficient, say so directly."
    )
    return "\n\n".join(sections)


def save_run_record(run_dir: Path, payload: dict[str, Any]) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    role = payload["role"]
    path = run_dir / f"{timestamp}-{role}-{uuid.uuid4().hex[:8]}.json"
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call an external research role model for the local four-role workflow.")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--role", choices=sorted(ROLE_DIRS), required=True)
    parser.add_argument("--stage", default="auto")
    parser.add_argument("--user-request", required=True)
    parser.add_argument("--route-file", default=str(DEFAULT_ROUTE_FILE))
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--no-auto-context", action="store_true")
    parser.add_argument("--max-context-chars-per-file", type=int, default=12000)
    parser.add_argument("--max-output-tokens", type=int, default=2200)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--output-file")
    parser.add_argument("--print-json", action="store_true")
    return parser


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve()
    skill_root = SKILL_ROOT
    outputs_dir = resolve_active_outputs_dir(workspace)
    route_file = Path(args.route_file).resolve()
    routing = load_json(route_file)
    role_cfg = routing.get("roles", {}).get(args.role)
    if not role_cfg:
        raise WorkerError(f"Missing role mapping for {args.role} in {route_file}")

    provider_name = role_cfg.get("provider", "")
    provider_cfg = routing.get("providers", {}).get(provider_name, {})
    if not provider_cfg:
        raise WorkerError(f"Missing provider mapping for {provider_name} in {route_file}")

    transport = provider_cfg.get("transport", "")
    if transport == "native-codex":
        raise WorkerError(f"Role {args.role} is configured for native Codex execution, not external API calling.")

    api_key_env = provider_cfg.get("api_key_env", "")
    api_key = read_env_value(api_key_env)
    if not api_key:
        raise WorkerError(f"Missing API key in environment variable: {api_key_env}")
    base_url = read_env_value(provider_cfg.get("base_url_env", "")) or provider_cfg.get("base_url", "")
    if not base_url:
        raise WorkerError(f"Missing base_url for provider {provider_name}")

    requested_model = role_cfg.get("model", "")
    model_env = role_cfg.get("model_env", "")
    if model_env:
        requested_model = read_env_value(model_env) or requested_model
    model = normalize_model(requested_model)
    if not model:
        raise WorkerError(f"Unable to resolve model for role {args.role}")

    stage = infer_stage(outputs_dir) if args.stage == "auto" else args.stage
    include_paths = [resolve_path(item, workspace) for item in args.include]
    context_paths = build_context_paths(
        workspace=workspace,
        skill_root=skill_root,
        outputs_dir=outputs_dir,
        role=args.role,
        stage=stage,
        includes=include_paths,
        use_auto_context=not args.no_auto_context,
    )
    context_bundle, context_records = render_context_blocks(context_paths, args.max_context_chars_per_file, workspace)

    role_name, role_title = ROLE_LABELS[args.role]
    system_prompt = build_system_prompt(
        role=args.role,
        role_name=role_name,
        role_title=role_title,
        stage=stage,
        provider=provider_name,
        model=model,
    )
    user_prompt = build_user_prompt(
        workspace=workspace,
        outputs_dir=outputs_dir,
        stage=stage,
        role_name=role_name,
        role_title=role_title,
        user_request=args.user_request,
        context_bundle=context_bundle,
        current_outputs=sorted(path.name for path in outputs_dir.glob("*.md")),
    )

    if transport == "openai-chat-completions":
        response_text, raw_response = call_openai_compatible_chat(
            base_url=base_url,
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=args.max_output_tokens,
            temperature=args.temperature,
            timeout=args.timeout_seconds,
        )
    elif transport == "anthropic-messages":
        response_text, raw_response = call_anthropic_compatible_messages(
            base_url=base_url,
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=args.max_output_tokens,
            temperature=args.temperature,
            timeout=args.timeout_seconds,
        )
    else:
        raise WorkerError(f"Unsupported provider transport: {transport}")

    if args.output_file:
        write_text(resolve_path(args.output_file, workspace), response_text + "\n")

    run_payload = {
        "timestamp": now_iso(),
        "workspace": str(workspace),
        "outputs_dir": str(outputs_dir),
        "route_file": str(route_file),
        "stage": stage,
        "role": args.role,
        "role_name": role_name,
        "role_title": role_title,
        "provider": provider_name,
        "model_requested": requested_model,
        "model_resolved": model,
        "api_transport": transport,
        "context_files": context_records,
        "user_request": args.user_request,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response_text": response_text,
        "usage": raw_response.get("usage", {}),
        "raw_response": raw_response,
    }
    run_path = save_run_record(resolve_agent_runs_dir(outputs_dir), run_payload)

    if args.print_json:
        print(
            json.dumps(
                {
                    "role": args.role,
                    "provider": provider_name,
                    "model": model,
                    "stage": stage,
                    "outputs_dir": str(outputs_dir),
                    "run_file": str(run_path),
                    "response_text": response_text,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(response_text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except WorkerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


