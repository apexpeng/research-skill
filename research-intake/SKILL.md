---
name: research-intake
description: 研究写作工作流 - 立项阶段。生成 project_brief.md 和 claims_evidence_matrix.md。使用中文输出，Coordinator/Executor/Reviewer/Supervisor 四角色体系。
argument-hint: [用户提供的研究材料或主题描述]
allowed-tools: Bash, Read, Write, Glob, Grep, WebSearch, WebFetch, TodoWrite, Agent
---

# Research Intake: 立项阶段

## 阶段目标

接收用户输入，生成标准化项目文档：

- `project_brief.md` — 项目简介与研究目标
- `claims_evidence_matrix.md` — 主张-证据矩阵

## 工作角色

| 角色 | 功能 | 调用方式 |
|------|------|---------|
| Coordinator | 调度者，分析输入，分配任务 | 原生会话 |
| Executor | 执行者，生成文档 | 原生会话或 external worker |
| Reviewer | 审查者，检查完整性 | 原生会话 |
| Supervisor | 监督者，门禁判定 | 原生会话 |

## 输入

- 用户提供的：研究主题 / 草稿 / 实验结果 / 图表 / 背景材料
- 现有 `ACTIVE_PROJECT.md`（如有）

## 输出文件

```text
research-workspace/outputs/projects/<project_key>/paper/
├── project_brief.md           # 项目简介
├── claims_evidence_matrix.md  # 主张-证据矩阵
└── ACTIVE_PROJECT.md          # 激活项目标记
```

## 工作流程

### Step 1: Coordinator - 输入分析

读取用户输入，判断：

- 输入类型（纯文本 / 已有草稿 / 实验数据 / 图表）
- 复杂度评估（简单想法 / 复杂项目）
- 输出语言（中文 / 英文，默认中文）

### Step 2: Executor - 生成文档

使用模板生成：

**project_brief.md 模板：**

```markdown
# Project Brief

## 项目标题
[Working title]

## 研究问题
[1-2 句话描述核心问题]

## 主要贡献点
1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]

## 数据/实验来源
- [实验批次/数据来源]
- [已有结果摘要]

## 目标会议/期刊
[如：ICLR 2026 / NeurIPS / Nature]

## 特殊要求
[用户约束/偏好]
```

**claims_evidence_matrix.md 模板：**

```markdown
# Claims-Evidence Matrix

## 核心主张

| # | 主张 | 证据 | 状态 | 备注 |
|---|------|------|------|------|
| C1 | [主张] | [对应实验/数据] | 支持/待验证/缺失 | |
| C2 | ... | ... | ... | |

## 证据列表

| E# | 证据描述 | 数据来源 | 对应主张 |
|----|---------|---------|---------|
| E1 | | | C1 |
```

### Step 3: Reviewer - 审查

检查：

- [ ] `project_brief.md` 是否清晰描述问题与贡献
- [ ] `claims_evidence_matrix.md` 是否为每条主张提供对应证据
- [ ] 缺失证据是否已明确标注

### Step 4: Supervisor - 门禁

检查：

- [ ] 两个文件都存在且非空
- [ ] claims 有对应 evidence，无悬空主张
- [ ] 输出到正确项目目录

门禁通过 → 输出“可进入 `paper-architecture`”

## 跨平台注意

- Windows 常见路径：`C:\Users\<USER>\.codex\research-workspace`
- Copilot Chat / 通用路径：`~/.codex/research-workspace`
- 使用 `cc_switch_adapter.py` 自动检测路径

## 调用示例

```text
/research-intake "研究主题：基于 Transformer 的遥感图像时序分析，已有实验结果在 results/ 目录"
```
