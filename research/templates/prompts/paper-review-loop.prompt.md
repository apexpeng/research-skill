# paper-review-loop 提示词

```text
请按 research workflow 进入 paper-review-loop。

采用多角色接力，而不是单角色自审自改：
- Coordinator：宣布当前轮次、目标文件、通过条件
- Reviewer：以审稿人视角独立审查 draft_zh.md，并输出 review_round_01.md
- Executor：根据 review_round_01.md 定向修订 draft_zh.md
- Supervisor：判断本轮是否通过，或是否进入下一轮

重点检查：
- 逻辑链是否闭合
- claim 与 evidence 是否匹配
- 是否存在过度因果化与过度推断
- 是否缺少关键对照、关键解释或边界说明
- 是否有 reviewer 一眼可抓的薄弱点

默认参数：
- MAX_ROUNDS = 4
- POSITIVE_THRESHOLD = 6/10
- REVIEWER_MODEL = 会话当前默认模型（Codex）
```
