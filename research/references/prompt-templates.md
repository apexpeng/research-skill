# Prompt Templates

These are starter prompts for chat-first usage.

## Start Workflow

```text
/research 课题：[你的课题]。目标：[先出中文主线/继续改稿/进入审稿循环]。已有材料：[结果/图/草稿/笔记]。
请显式展示Coordinator、Reviewer、Executor、Supervisor的接力流程。
可选覆盖：review rounds: 4, positive threshold: 6/10, reviewer model: session default (current Codex model)
```

## Intake Prompt

```text
请按 research workflow 进入 paper-intake。
基于我已有材料，输出 project_brief.md 与 claims_evidence_matrix.md。
要求：标出证据已支持结论与仅可推测结论，不要直接跳到整篇写作。
```

## Architecture Prompt

```text
请按 research workflow 进入 paper-architecture。
基于 project_brief 与 claims_evidence_matrix 生成 narrative_report_zh.md 和 outline_zh.md。
要求：先主线后章节，每条 claim 对应证据，明确最可能被 reviewer 质疑点。
```

## Draft Prompt

```text
请按 research workflow 进入 paper-draft。
根据 narrative_report_zh 与 outline_zh 生成 draft_zh.md。
要求：学术中文、每段单一核心信息、讨论写清限制与替代解释。
```

## Review Loop Prompt

```text
请按 research workflow 进入 paper-review-loop，并保持角色分离：
1) Coordinator宣布轮次与目标；
2) Reviewer独立审查并产出 review_round_01.md；
3) Executor按问题单修订 draft_zh.md；
4) Supervisor做门禁判定。
默认参数：MAX_ROUNDS=4，POSITIVE_THRESHOLD=6/10，REVIEWER_MODEL=会话当前默认模型（Codex）。
```
