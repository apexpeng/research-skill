---
name: research
description: 四角色研究写作工作流（跨平台版：支持 Claude Codex / GitHub Copilot Chat）。提供中文优先的论文撰写、迭代审查与输出管理。
allowed-tools: Bash, Read, Write, Glob, Grep, WebSearch, WebFetch, Agent, TodoWrite
---

# Research（跨平台版）

## 平台兼容性

本 skill 经过设计，可在以下平台运行：

| 平台 | 支持状态 | 备注 |
|------|---------|------|
| **Claude Codex** | ✅ 完整支持 | 使用内置 external worker 脚本调用 LongCat/MiniMax |
| **GitHub Copilot Chat** | ✅ 完整支持 | 使用相同文件结构，仅 external worker 调用方式需通过 `bash -c` 或内联 Python |
| **纯 API 会话** | ⚠️ 部分支持 | external worker 需手动适配，端点需用户配置 |

跨平台核心原则：
- 所有路径使用 `Path` 对象兼容 Windows/macOS/Linux
- 外部 API 调用通过 `invoke_research_role.py` 统一封装
- 文件系统操作依赖绝对路径，不依赖 cwd
- PowerShell 脚本提供 `-Command` 参数，bash 脚本提供 `-c` 兼容写法

## 概述

本 skill 为自包含研究工作流，不依赖任何旧项目目录。

事实来源：
- 当前 Codex/Copilot 会话
- 固定工作区 `C:\Users\18711\.codex\research-workspace`（Copilot 模式下为 `~/.codex/research-workspace`）
- Skill 打包的配置/模板/角色文档

## 角色

工作流由四个独立角色构成，有明确的交接边界：

- `Coordinator` — 调度者（Coordinator）
- `Executor` — 执行者（Executor）
- `Reviewer` — 审查者（Reviewer）
- `Supervisor` — 监督者（Supervisor）

默认运行时路由：

| 角色 | 主要模型 | 备选模型 | 执行方式 |
|------|---------|---------|---------|
| Coordinator | LongCat-Flash-Chat | session-default | External API worker |
| Executor | MiniMax-M2.7 | session-default | External API worker |
| Reviewer | session-default | Claude 4.6 | 原生会话 / 子代理 |
| Supervisor | session-default | Claude 4.6 | 原生会话 / 子代理 |

## 必须读取

Skill 触发时优先读取：

1. `~/.codex/user.md`
2. `~/.codex/AGENTS.md`
3. `~/.codex/memories/PROFILE.md`
4. `~/.codex/memories/ACTIVE.md`
5. `C:\Users\18711\.codex\skills\research\SKILL.md`
6. `~/.codex/skills/research/agents/coordinator/agent.md`
7. `~/.codex/skills/research/agents/executor/agent.md`
8. `~/.codex/skills/research/agents/reviewer/agent.md`
9. `~/.codex/skills/research/agents/supervisor/agent.md`
10. `~/.codex/research-workspace/outputs/ACTIVE_PROJECT.md`（若存在）

## 激活项目规则

禁止将不同项目混合到同一根输出目录。

1. 若 `...\research-workspace\outputs\ACTIVE_PROJECT.md` 存在，以该项目 `paper` 目录为活跃输出目录。
2. 若输出散落在 `...\research-workspace\outputs\paper\`，由 `Supervisor` 执行整理。

3. 已归档项目位于：

```
~/.codex/research-workspace/outputs/projects/<project_key>/
```

## 阶段判定

按当前输出状态决定阶段：

| 条件 | 阶段 |
|------|------|
| 缺少 `project_brief.md` 或 `claims_evidence_matrix.md` | `paper-intake` |
| brief 存在但缺少 `outline_zh.md` | `paper-architecture` |
| outline 存在但缺少 `draft_zh.md` | `paper-draft` |
| 中文草稿存在 | `paper-review-loop` |
| 草稿通过审查（评分 ≥ 6/10） | `paper-figure` |
| figure 完成 | `paper-supplement` |
| supplement 完成 | `paper-export-en` |

## 外部 Worker 调用规则

需要真实多模型协作时：

1. 使用 `~/.codex/skills/research/scripts/invoke_research_role.py`
2. Coordinator → LongCat
3. Executor → MiniMax
4. 运行记录保存到活跃项目 `agent_runs`

## 聊天规则

- 保持工作流本地化和文件驱动
- 优先创建/更新实际文件，而非抽象建议
- 缺少模板时使用 `~\skills\research\templates` 下的模板
- 默认输出语言为严谨学术中文
- 角色交接必须明确标注

## 运行时默认值

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `MAX_ROUNDS` | `4` | 最大审查→修订→再审查轮次 |
| `POSITIVE_THRESHOLD` | `6/10` | 通过阈值 |
| `PAPER_LIBRARY` | `papers/, literature/` | 本地 PDF 扫描位置 |
| `MAX_LOCAL_PAPERS` | `50` | 最大扫描本地 PDF 数 |
| `ADAPTIVE_ROUNDS` | `false` | 是否启用自适应轮次 |
| `FIGURE_ENABLED` | `true` | 是否启用 figure 整合阶段 |
| `SUPPLEMENT_ENABLED` | `true` | 是否启用补充材料阶段 |

## 多智能体审查契约

`paper-review-loop` 最低序列：

1. `Coordinator` 宣布当前轮次和目标
2. `Reviewer` 执行独立审查并写入 `review_round_0X.md`
3. `Executor` 基于审查意见修订 `draft_zh.md`
4. `Supervisor` 门禁判定并检查完整性
5. `Coordinator` 决定下一轮或阶段推进

硬性规则：
- 执行者不能自我批准
- 审查者不能先改稿再给自己的改稿评分
- 监督者不能绕过缺失的独立审查记录
- 第 4 轮仍不通过时输出 `需人工决策`

## 输出结构

推荐输出结构：

```
~/.codex/research-workspace/outputs/projects/<project_key>/paper/
~/.codex/research-workspace/outputs/projects/<project_key>/agent_runs/
~/.codex/research-workspace/outputs/projects/<project_key>/figures/
~/.codex/research-workspace/outputs/projects/<project_key>/supplements/
```

核心输出文件：

| 文件 | 阶段 | 说明 |
|------|------|------|
| `project_brief.md` | paper-intake | 项目简介与目标 |
| `claims_evidence_matrix.md` | paper-intake | 主张-证据矩阵 |
| `outline_zh.md` | paper-architecture | 论文大纲 |
| `draft_zh.md` | paper-draft | 中文初稿 |
| `review_round_0X.md` | paper-review-loop | 审查记录 |
| `figure_draft_*.md` | paper-figure | 图表描述 |
| `supplement_*.md` | paper-supplement | 补充材料 |

## Skill 组合

本 skill 支持调用以下子 skills：

| Skill | 说明 | 触发 |
|-------|------|------|
| `research-intake` | 立项阶段 | `/research-intake` |
| `research-draft` | 起草阶段 | `/research-draft` |
| `research-review` | ARIS 原版外部审查 | `/research-review` |
| `feishu-notify` | 飞书通知 | `/feishu-notify` |
| `paper-figure` | ARIS 原版图表生成 | `/paper-figure` |

## 边界

- 本 skill 支持写作/审查工作流编排，不支持自主实验室执行
- 本 skill 现已独立于旧项目根目录，即使旧目录被删除仍可稳定运行
- 跨平台兼容性通过路径抽象和统一 worker 脚本保障
