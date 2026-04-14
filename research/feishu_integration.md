# Feishu Integration for Research Workflow

## Overview

本文档描述如何将飞书通知整合到 research 工作流中。

## 飞书通知 Skill

使用现有的 `feishu-notify` skill，路径：
`~/.codex/skills/feishu-notify/SKILL.md`

## 配置文件

创建 `~/.claude/feishu.json`：

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID"
}
```

或交互模式：
```json
{
  "mode": "interactive",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID",
  "interactive": {
    "bridge_url": "http://localhost:5000",
    "timeout_seconds": 300
  }
}
```

## Research Workflow 中的事件

### 事件列表

| 事件 | 触发时机 | 内容 |
|------|---------|------|
| `review_scored` | 每轮审查完成后 | 轮次、评分、结论 |
| `checkpoint` | 阶段切换时 | 当前阶段、待处理 |
| `intake_complete` | project_brief 生成完成 | 项目标题、贡献数 |
| `draft_complete` | draft_zh.md 生成完成 | 阶段完成 |
| `figure_complete` | figure_draft 生成完成 | figure 数量 |
| `supplement_complete` | supplement 生成完成 | 补充材料数 |
| `export_complete` | paper-export-en 完成 | 输出路径 |
| `error` | 工作流出错 | 错误信息 |
| `pipeline_done` | 全流程完成 | 最终状态 |

### 咚咚审查事件格式

```
/feishu-notify "review_scored: Round 1 - Score 6.5/10 - Proceed - 主要问题：证据链不完整"
```

### Supervisor门禁事件格式

```
/feishu-notify "checkpoint: paper-review-loop 进入 Round 2，等待咚咚审查"
```

## 整合方式

在其他 skill 中添加：

```markdown
### Feishu Notification (if configured)

检查 `~/.claude/feishu.json` 是否存在且 mode 不是 "off"：
- 如果 mode 是 "push"：发送 webhook 通知
- 如果 mode 是 "interactive"：发送通知并等待用户回复
- 如果文件不存在或 mode 是 "off"：跳过（无操作）
```

## 本地 feishu-notify 使用

```
/feishu-notify "review_scored: Round 1 - 6.5/10 - Proceed"
```

## 注意事项

- 推送模式是"发后不理"——发送后立即返回
- 交互模式超时后自动继续（auto-proceed）
- 飞书不可达时不能阻塞工作流
