# External Workers

Use the bundled worker when `/research` needs real third-party model calls.

## Execution Split

| Role | Model | Execution Mode |
|------|-------|----------------|
| `Coordinator / coordinator` | LongCat-Flash-Chat | External API worker |
| `Executor / executor` | MiniMax-M2.7 | External API worker |
| `Reviewer / reviewer` | session default / Codex | Native Codex/OpenAI |
| `Supervisor / supervisor` | session default / Codex | Native Codex/OpenAI |

## Worker Script

Path (Codex):

`~/.codex/skills/research/scripts/invoke_research_role.py`

Path (Copilot Chat / Cross-platform):

`~/.codex/skills/research/scripts/invoke_research_role.py`

The script:
- reads route config from `~/.codex/skills/research/config/role-model-routing.json`
- resolves API keys from environment variables
- loads context from fixed workspace
- uses OpenAI-compatible chat completions for LongCat
- uses Anthropic-compatible messages for MiniMax
- writes JSON run records into active project `agent_runs`

## Typical Usage

### Codex (Windows)

```powershell
python ~/.codex/skills/research/scripts/invoke_research_role.py `
  --role coordinator `
  --stage paper-intake `
  --user-request "分析当前输入，判断阶段并给出下一步任务单"
```

### Copilot Chat / Cross-Platform

```bash
python ~/.codex/skills/research/scripts/invoke_research_role.py \
  --workspace ~/.codex/research-workspace \
  --role executor \
  --stage paper-draft \
  --user-request "根据 outline_zh.md 生成 draft_zh.md"
```

## API Key Configuration

| Provider | Env Variable | Notes |
|----------|-------------|-------|
| LongCat | `LONGCAT_API_KEY` | Official LongCat OpenAI-compatible endpoint |
| MiniMax | `MINIMAX_API_KEY` | Official MiniMax Anthropic-compatible endpoint |

For China-issued MiniMax keys:
```
MINIMAX_BASE_URL=https://api.minimaxi.com/anthropic
```

## Alternative Model Combinations (ARIS-Inspired)

### Using llm-chat MCP Server

If using the `llm-chat` MCP server (for any OpenAI-compatible API as reviewer):

```bash
# Install llm-chat MCP server
npm install -g @modelcontextprotocol/server-llm-chat

# Configure in settings
claude mcp add llm-chat -s user -- llm-chat \
  --api-key YOUR_KEY \
  --base-url https://api.example.com/v1
```

### Supported Combinations

| Executor | Reviewer | Setup |
|----------|----------|-------|
| Claude | GPT-5.4 | Codex MCP |
| GLM-5 | GPT-5.4 | Z.ai API |
| MiniMax-M2.7 | MiniMax-M2.5 | MiniMax API |
| Any | Any OpenAI-compatible | llm-chat MCP |

## Notes

- Do not claim coordinator/executor external calls occurred if worker was not actually run
- Keep API keys in environment variables only
- For Copilot Chat mode, external worker calls may be slower due to Python subprocess overhead
- If external worker fails, workflow gracefully degrades to native session execution

## State Recovery

For long loops, worker creates `agent_runs/*.json` records for audit trail:

```json
{
  "timestamp": "2026-04-14T10:30:00+08:00",
  "role": "executor",
  "stage": "paper-draft",
  "model": "MiniMax-M2.7",
  "response_text": "...",
  "usage": {...}
}
```

These records are immutable and used for debugging + compliance.
