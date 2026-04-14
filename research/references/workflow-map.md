# Workflow Map

## Purpose

This reference maps the four-role workflow onto concrete files in:

`~/.codex/research-workspace`

Or on Copilot Chat / cross-platform:

`~/.codex/research-workspace`

Role separation is mandatory:

- `Coordinator` routes
- `Executor` drafts/revises
- `Reviewer` reviews independently
- `Supervisor` enforces gatekeeping

## File Targets

Expected output files in active paper directory:

| File | Stage | Required |
|------|-------|----------|
| `project_brief.md` | paper-intake | Yes |
| `claims_evidence_matrix.md` | paper-intake | Yes |
| `narrative_report_zh.md` | paper-architecture | Optional (complex projects) |
| `outline_zh.md` | paper-architecture | Yes |
| `draft_zh.md` | paper-draft | Yes |
| `review_round_0X.md` | paper-review-loop | Yes (per round) |
| `figure_draft_*.md` | paper-figure | Optional |
| `figure_caption_draft.md` | paper-figure | Optional |
| `supplement_*.md` | paper-supplement | Optional |
| `review_scores.json` | All stages | Auto-generated |

Templates at: `~\skills\research\templates\outputs\`

## Stage Map

### paper-intake

Outputs: `project_brief.md`, `claims_evidence_matrix.md`

Flow:
1. `Coordinator` decides stage/task split
2. `Executor` drafts files
3. `Supervisor` checks completeness

### paper-architecture

Outputs: `narrative_report_zh.md` (optional), `outline_zh.md`

Flow:
1. `Coordinator` routes
2. `Executor` drafts
3. `Reviewer` pressure-tests logic

### paper-draft

Output: `draft_zh.md`

Flow:
1. `Coordinator` confirms readiness
2. `Executor` drafts
3. `Supervisor` checks preconditions

### paper-review-loop

Outputs: `review_round_0X.md`, updated `draft_zh.md`

Mandatory sequence:
1. `Coordinator` announces round + target
2. `Reviewer` reviews first, writes review record
3. `Executor` revises after review complete
4. `Supervisor` decides pass/fail for current round
5. `Coordinator` starts next round or advances stage

Hard rules:
- no self-approval by executor
- no blended review+revision by reviewer
- no supervisor bypass when review record is missing
- round 4 fail (or adaptive round 6) => `需人工决策`

### paper-figure (NEW)

Outputs: `figure_draft_*.md`, `figure_caption_draft.md`

Flow:
1. `Coordinator` confirms draft passed review, checks figure needs
2. `Executor` generates figure descriptions and captions
3. `Supervisor` validates figure-text alignment
4. Optional: call `paper-figure` skill for final rendering

### paper-supplement (NEW)

Outputs: `supplement_*.md`, `supplement_table_*.md`

Flow:
1. `Coordinator` identifies supplement scope
2. `Executor` drafts supplement materials
3. `Reviewer` checks completeness + non-duplication
4. `Supervisor` final archive check

### paper-export-en

Output: English LaTeX paper

Flow:
1. `Coordinator` confirms all Chinese drafts pass review
2. `Executor` coordinates translation (if needed)
3. `Reviewer` final content review
4. `Supervisor` format compliance check

## Project Organization

```
research-workspace/
├── outputs/
│   ├── ACTIVE_PROJECT.md          # Current active project marker
│   ├── paper/                      # Legacy inbox (should migrate)
│   └── projects/
│       └── <project_key>/
│           ├── paper/
│           │   ├── project_brief.md
│           │   ├── claims_evidence_matrix.md
│           │   ├── draft_zh.md
│           │   └── review_round_*.md
│           ├── figures/             # NEW: figure outputs
│           ├── supplements/         # NEW: supplement outputs
│           ├── agent_runs/          # External worker run records
│           └── REVIEW_STATE.json    # NEW: review loop state
```

## Cross-Platform Path Resolution

```python
def resolve_workspace_path(base: str) -> Path:
    if base == "~" or base.startswith("~/"):
        return Path.home() / ".codex" / base[2:] if base != "~" else Path.home() / ".codex"
    return Path(base)

WORKSPACE = resolve_workspace_path("~/.codex/research-workspace")
SKILL_ROOT = resolve_workspace_path("~/.codex/skills/research")
```

## Workflow Composition (ARIS-Inspired)

For full end-to-end pipeline:

```
/research-lit → /idea-creator → /novelty-check → implement →
/auto-review-loop → /paper-plan → /paper-figure → /paper-write →
/paper-compile → /auto-paper-improvement-loop → submit
```

This research skill covers the `/paper-*` portion. Use other skills (idea-discovery, auto-review-loop) for upstream phases.
