# Runtime Defaults

## Auto Review Loop

| Constant | Default | Meaning |
|---|---|---|
| `MAX_ROUNDS` | `4` | Max review -> revise -> re-review rounds |
| `ADAPTIVE_ROUNDS` | `false` | Enable adaptive max rounds (up to 6) |
| `POSITIVE_THRESHOLD` | `6/10` | Default pass threshold |

## Research Literature

| Constant | Default | Meaning |
|---|---|---|
| `PAPER_LIBRARY` | `papers/, literature/` | Local PDF scan locations |
| `MAX_LOCAL_PAPERS` | `50` | Max local PDFs to scan (increased from 20) |
| `ARXIV_DOWNLOAD` | `false` | Download arXiv PDFs during lit survey |

## Codex Defaults

| Constant | Default | Meaning |
|---|---|---|
| `REVIEWER_MODEL` | `session default (current Codex model)` | Default reviewer model in native Codex mode |

## Runtime Role Routing

| Role | Runtime Model | Execution Mode |
|---|---|---|
| `Coordinator` | `LongCat-Flash-Chat` | Real external API worker |
| `Executor` | `MiniMax-M2.7` | Real external API worker |
| `Reviewer` | `session default / Codex` | Native Codex/OpenAI |
| `Supervisor` | `session default / Codex` | Native Codex/OpenAI |

## Workspace and Output Routing

Fixed workspace (Codex):

`~/.codex/research-workspace`

Fixed workspace (Copilot Chat / Cross-platform):

`~/.codex/research-workspace`

Output pointers:

- `~/.codex/research-workspace/outputs/ACTIVE_PROJECT.json`
- `~/.codex/research-workspace/outputs/ACTIVE_PROJECT.md`
- `~/.codex/research-workspace/outputs/PROJECT_INDEX.json`
- `~/.codex/research-workspace/outputs/projects/`

Organizer wrapper:

```powershell
# Codex
~/.codex/skills/research/scripts/organize-research-outputs.ps1 -Command sync

# Copilot Chat
python ~/.codex/skills/research/scripts/invoke_research_role.py --workspace ~/.codex/research-workspace --role supervisor --user-request "organize"
```

## External Worker Paths

- Worker script: `~/.codex/skills/research/scripts/invoke_research_role.py`
- Organizer core: `~/.codex/skills/research/scripts/organize_research_outputs.py`

For Copilot Chat, use POSIX paths:
- `~/.codex/skills/research/scripts/invoke_research_role.py`
- `~/.codex/skills/research/scripts/organize_research_outputs.py`

## Adaptive Configuration

| Config Key | Default | Description |
|---|---|---|
| `ADAPTIVE_WEIGHTS` | `false` | Enable dimension weight adjustment |
| `FIGURE_ENABLED` | `true` | Enable paper-figure stage |
| `SUPPLEMENT_ENABLED` | `true` | Enable paper-supplement stage |
| `HUMAN_CHECKPOINT` | `false` | Pause at checkpoints for approval |

## Feishu Integration (Optional)

| Config Key | Default | Description |
|---|---|---|
| `FEISHU_MODE` | `off` | off / push / interactive |
| `FEISHU_WEBHOOK_URL` | `null` | Webhook URL for push mode |
| `FEISHU_BRIDGE_URL` | `null` | Bridge URL for interactive mode |

## State Persistence

| File | Purpose |
|---|---|
| `REVIEW_STATE.json` | Review loop round tracking + pending fixes |
| `review_scores.json` | Score progression history |
| `checkpoints/*.json` | Human approval checkpoint queue |

## Cross-Platform Path Detection

```python
import os
from pathlib import Path

def detect_platform():
    if os.name == 'nt':
        return 'windows'  # Codex on Windows
    elif Path.home() / ".claude" exists:
        return 'copilot'  # GitHub Copilot Chat
    else:
        return 'unix'  # Linux/macOS terminal

def resolve_workspace():
    platform = detect_platform()
    if platform == 'windows':
        base = Path.home() / ".codex"
    else:
        base = Path.home() / ".codex"
    return base / "research-workspace"
```

## Alternative Model Combinations (ARIS-Inspired)

| Executor | Reviewer | Provider Config |
|---|---|---|
| Claude Opus | GPT-5.4 (Codex MCP) | Default |
| GLM-5 | GPT-5.4 (Codex MCP) | Z.ai API |
| MiniMax-M2.7 | MiniMax-M2.5 | MiniMax API |
| Any | Any OpenAI-compatible | llm-chat MCP |

See `docs/LLM_API_MIX_MATCH_GUIDE.md` for setup (ARIS documentation).
