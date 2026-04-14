# Adaptive Stages

## Overview

Adaptive stages allow the research workflow to dynamically adjust review depth and round limits based on project complexity. Inspired by ARIS's configurable `MAX_ROUNDS` and checkpoint system.

## When to Use Adaptive Modes

Enable adaptive stages when project has one or more of:

| Complexity Indicator | Example | Adaptive Action |
|---------------------|---------|-----------------|
| High evidence volume | 20+ experiments | Expand evidence review depth |
| Cross-domain | ML + HCI + theory | Increase related work coverage |
| Theoretical component | Theorems, proofs | Add theoretical soundness dimension |
| Multiple figure types | 8+ figures | Extend paper-figure phase |
| Controversial claims | Challenging existing methods | Increase reviewer scrutiny |
| Multi-author | 5+ authors | Add coordination overhead |

## Adaptive Configuration

```yaml
# In project config or ACTIVE_PROJECT.md
adaptive:
  enabled: true          # Global toggle
  evidence_depth: high   # normal / high / exhaustive
  review_rigor: strict   # normal / strict / very_strict
  max_rounds: 6          # Override MAX_ROUNDS (default 4)
  checkpoints:
    - idea_selection
    - architecture_approved
    - draft_v1
    - review_passed
```

## Stage Adaptation Rules

### paper-intake

| Complexity | Duration | Extra Checks |
|------------|----------|--------------|
| Normal | 1 round | Standard claims matrix |
| High | 2 rounds | Literature gap analysis added |
| Exhaustive | 3 rounds | Related work coverage map |

### paper-architecture

| Complexity | Duration | Extra Outputs |
|------------|----------|---------------|
| Normal | 1 round | outline_zh.md |
| High | 2 rounds | + narrative_report_zh.md (required) |
| Exhaustive | 2-3 rounds | + section_dependencies.md + method_comparison.md |

### paper-draft

| Complexity | Pre-flight Check |
|------------|------------------|
| Normal | outline vs brief coverage |
| High | + technical soundness review |
| Exhaustive | + reproduciblity checklist |

### paper-review-loop

| Mode | Max Rounds | Round Focus |
|------|-----------|-------------|
| Normal | 4 | Standard 4-dimension review |
| Strict | 5 | + reviewer objection pre-emption |
| Very Strict | 6 | + adversarial reviewer simulation |

### paper-figure

| Figure Volume | Phase Duration | Coordination |
|---------------|----------------|--------------|
| < 4 figures | 1 round | Inline with draft |
| 4-8 figures | 1-2 rounds | Dedicated figure phase |
| > 8 figures | 2-3 rounds | Separate figure review |

### paper-supplement

| Supplement Volume | Phase Duration |
|-------------------|----------------|
| < 3 items | 1 round (combined with figure) |
| 3-6 items | 1 round (dedicated) |
| > 6 items | 2 rounds |

## Checkpoint System

Inspired by ARIS's `human checkpoint` + `AUTO_PROCEED` system:

### Available Checkpoints

| Checkpoint | Stops Before | Resume Point |
|------------|--------------|--------------|
| `idea_selection` | Entering paper-intake | After user selects idea |
| `architecture_approved` | Entering paper-draft | After user approves outline |
| `draft_v1` | Entering review loop | After user reviews first draft |
| `review_round_2` | Round 2 of review | After user reviews round 1 feedback |
| `figure_approved` | Entering supplement | After user approves figures |
| `final_export` | paper-export-en | After user confirms export |

### Checkpoint File Format

```json
{
  "checkpoint": "architecture_approved",
  "status": "waiting",
  "created": "2026-04-10T14:30:00Z",
  "resume_after": "user_approval",
  "artifacts": {
    "outline_zh.md": "/path/to/outline",
    "claims_evidence_matrix.md": "/path/to/matrix"
  }
}
```

## State Persistence

For long-running review loops, maintain `REVIEW_STATE.json`:

```json
{
  "project_key": "...",
  "current_round": 2,
  "max_rounds": 4,
  "last_review_file": "review_round_02.md",
  "pending_fixes": [
    "Add statistical power analysis",
    "Soften claim in Section 3.2"
  ],
  "score_history": [5.0, 6.5, 6.8],
  "checkpoint": null,
  "last_updated": "2026-04-10T15:00:00Z"
}
```

**Recovery**: If context window fills mid-loop, read `REVIEW_STATE.json` and resume from last checkpoint.

## Round Progression Guidelines

| Round | Focus | Expected Improvement |
|-------|-------|---------------------|
| 0 | Baseline | N/A |
| 1 | Low-hanging fruit | +1.0-1.5 points |
| 2 | Core argument refinement | +0.5-1.0 points |
| 3 | Deep issues (if needed) | +0.3-0.5 points |
| 4+ | Diminishing returns | Manual intervention |

**Stagnation Rule**: If improvement < 0.3 between rounds, check for:
- Systematic issue not being addressed
- Reviewer and executor misalignment
- Unrecoverable fundamental flaw

## Cross-Platform Checkpoint Behavior

| Platform | Checkpoint Behavior |
|----------|-------------------|
| Claude Codex | Pauses session, waits for user input |
| GitHub Copilot Chat | Writes checkpoint file, resumes on next session |
| API-only | Requires external state management |

In Copilot Chat mode, checkpoints write to `~/.codex/research-workspace/checkpoints/` and resume requires explicit `/research resume` command.
