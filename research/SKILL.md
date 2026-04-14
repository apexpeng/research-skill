---
name: research
description: 四角色研究写作工作流（v1）。支持论文撰写、常规审查与输出管理。
allowed-tools: Bash, Read, Write, Glob, Grep, WebSearch, WebFetch, Agent, TodoWrite
---

# Research（v1：跨平台论文写作工作流）

## 平台兼容性

本 skill 经过设计，可在以下平台运行：

| 平台 | 支持状态 | 备注 |
|------|---------|------|
| **Claude Codex** | ✅ 完整支持 | 使用内置 external worker 脚本调用 LongCat / MiniMax |
| **GitHub Copilot Chat** | ✅ 完整支持 | 使用相同文件结构，external worker 需通过 `bash -c` 或内联 Python 适配 |
| **纯 API 会话** | ⚠️ 部分支持 | external worker 需手动适配，端点需用户配置 |

跨平台原则：

- 所有路径使用 `Path` 对象兼容 Windows / macOS / Linux
- 外部 API 调用通过 `invoke_research_role.py` 统一封装
- 文件系统操作优先使用绝对路径，不依赖当前工作目录

## 概述

本 skill 是一个**写作主流程入口**，负责将研究材料组织为论文工作流产物。

事实来源包括：

- 当前 Codex / Copilot 会话
- 默认工作区 `~/.codex/research-workspace`
- skill 打包的配置、模板与角色文档

Windows 常见对应路径可为：

```text
C:\Users\<USER>\.codex\research-workspace
```

## 角色

工作流由四个独立角色构成，有明确交接边界：

- `Coordinator` — 调度者
- `Executor` — 执行者
- `Reviewer` — 审查者
- `Supervisor` — 监督者

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
5. `~/.codex/skills/research/SKILL.md`
6. `~/.codex/skills/research/agents/coordinator/agent.md`
7. `~/.codex/skills/research/agents/executor/agent.md`
8. `~/.codex/skills/research/agents/reviewer/agent.md`
9. `~/.codex/skills/research/agents/supervisor/agent.md`
10. `~/.codex/research-workspace/outputs/ACTIVE_PROJECT.md`（若存在）

## 激活项目规则

禁止将不同项目混合到同一根输出目录。

1. 若 `.../research-workspace/outputs/ACTIVE_PROJECT.md` 存在，以该项目 `paper` 目录为活跃输出目录。
2. 若输出散落在 `.../research-workspace/outputs/paper/`，由 `Supervisor` 执行整理。
3. 已归档项目位于：

```text
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

## 与 `research_2` 的关系

- `research` 是 v1 主入口，负责“写”和“推进”
- `research_2` 是 v2 审查增强入口，负责“审”和“严格把关”
- 当前 v1 **不会自动切换**到 `research_2`
- 如需使用六维审查标准，应显式调用：

```bash
/research_2 "深度审查草稿"
```

## 外部 Worker 调用规则

需要真实多模型协作时：

1. 使用 `~/.codex/skills/research/scripts/invoke_research_role.py`
2. Coordinator → LongCat
3. Executor → MiniMax
4. 运行记录保存到活跃项目 `agent_runs/`

## 聊天规则

- 保持工作流本地化和文件驱动
- 优先创建 / 更新实际文件，而非只给抽象建议
- 缺少模板时使用 `~/.codex/skills/research/templates` 下的模板
- 默认输出语言为严谨学术中文
- 角色交接必须明确标注

## 运行时默认值

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `MAX_ROUNDS` | `4` | 最大审查 → 修订 → 再审查轮次 |
| `POSITIVE_THRESHOLD` | `6/10` | 通过阈值 |
| `PAPER_LIBRARY` | `papers/, literature/` | 本地 PDF 扫描位置 |
| `MAX_LOCAL_PAPERS` | `50` | 最大扫描本地 PDF 数 |
| `ADAPTIVE_ROUNDS` | `false` | 是否启用自适应轮次 |
| `FIGURE_ENABLED` | `true` | 是否启用 figure 阶段 |
| `SUPPLEMENT_ENABLED` | `true` | 是否启用补充材料阶段 |

## 多智能体审查契约

`paper-review-loop` 最低序列：

1. `Coordinator` 宣布当前轮次与目标
2. `Reviewer` 执行独立审查并写入 `review_round_0X.md`
3. `Executor` 基于审查意见修订 `draft_zh.md`
4. `Supervisor` 做门禁判定与完整性检查
5. `Coordinator` 决定下一轮或阶段推进

硬性规则：

- 执行者不能自我批准
- 审查者不能先改稿再给自己的改稿评分
- 监督者不能绕过缺失的独立审查记录
- 第 4 轮仍不通过时输出 `需人工决策`

## 输出结构

推荐输出结构：

```text
~/.codex/research-workspace/outputs/projects/<project_key>/paper/
~/.codex/research-workspace/outputs/projects/<project_key>/agent_runs/
~/.codex/research-workspace/outputs/projects/<project_key>/figures/
~/.codex/research-workspace/outputs/projects/<project_key>/supplements/
```

核心输出文件：

| 文件 | 阶段 | 说明 |
|------|------|------|
| `project_brief.md` | paper-intake | 项目简介与目标 |
| `claims_evidence_matrix.md` | paper-intake | 主张—证据矩阵 |
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
| `paper-figure` | 图表生成 | `/paper-figure` |

## 边界

- 本 skill 负责写作 / 常规审查工作流编排，不支持自主实验室执行
- 本 skill 现已独立于旧项目根目录，即使旧目录被删除仍可稳定运行
- 若需要投稿前更严格的把关，请改用 `research_2`
