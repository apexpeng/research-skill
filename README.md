# Research Skills

中文优先的科研写作与论文审查 skill 集，围绕“四角色协作 + 文件驱动产物 + 分阶段 workflow”组织，当前仓库提供两个清晰分工的主入口：

- `research`：v1，面向**论文写作与迭代审查的全流程编排**
- `research_2`：v2，面向**投稿前深度审查的增强型入口**

本仓库当前更准确的定位是：**科研写作与论文审查 skill 集**，而不是通用意义上的“全自动科研系统”。

## 核心特性

- 🤖 **四角色工作流**：Coordinator（调度）、Executor（执行）、Reviewer（审查）、Supervisor（监督）
- 📝 **中文优先**：针对中文期刊/会议与中文科研写作场景优化
- 🔄 **迭代审查**：支持多轮 review loop 与门禁推进
- 📊 **图表与补充材料衔接**：支持 figure / supplement 阶段组织
- 🧩 **双入口结构**：v1 负责写作编排，v2 负责严格审查
- 🌐 **跨平台兼容设计**：面向 Claude Codex / GitHub Copilot Chat 的文件驱动 workflow

## 技能列表

### 主入口

| 技能 | 定位 | 适用场景 |
|------|------|----------|
| `research` | v1：四角色论文写作工作流 | 从立项、起草到常规审查 |
| `research_2` | v2：论文审查增强版 | 投稿前严格审查、创新性/空白点复核 |

### 通用子技能

| 技能 | 说明 |
|------|------|
| `research-intake` | 立项阶段：生成 `project_brief.md` 与 `claims_evidence_matrix.md` |
| `research-draft` | 起草阶段：基于大纲生成中文初稿 |
| `research-review` | 外部审查（基于 ARIS） |
| `auto-review-loop-llm` | 多轮自主审查循环 |
| `feishu-notify` | 飞书通知集成 |
| `paper-plan` | 英文论文规划（ARIS 原版） |
| `paper-plan-zh` | 中文论文规划 |
| `paper-write-zh` | 中文论文写作 |
| `paper-compile` | LaTeX 编译 |
| `paper-figure` | 图表生成（ARIS 原版） |
| `research-pipeline` | 端到端研究管线（偏 ARIS / dry-lab workflow） |

## 快速开始

### 1. 安装

```bash
git clone https://github.com/apexpeng/research-skill.git
cp -r research-skill/* ~/.claude/skills/
```

### 2. 配置环境变量

```bash
# 必需
export LONGCAT_API_KEY="your_longcat_key"   # Coordinator 模型
export MINIMAX_API_KEY="your_minimax_key"   # Executor 模型

# 可选
export ARIS_MAX_ROUNDS=4
export ARIS_POSITIVE_THRESHOLD=6.0
```

### 3. 选择入口

```bash
# v1：论文写作主流程
/research "您的研究主题"

# v2：针对已有草稿或稿件进行严格审查
/research_2 "深度审查草稿"

# 分阶段调用
/research-intake "研究材料描述"
/research-draft "生成中文初稿"
/research-review "审查草稿"
/paper-plan-zh "生成论文大纲"
/paper-write-zh "生成中文论文"
/paper-compile paper/
```

## 项目结构

```text
research-skill/
├── research/              # v1 核心 skill（四角色论文写作工作流）
│   ├── agents/            # 四角色定义
│   ├── config/            # 角色路由配置
│   ├── references/        # 参考文档
│   ├── scripts/           # 跨平台适配脚本
│   └── templates/         # 阶段模板
├── research_2/            # v2 审查增强入口
│   └── SKILL.md           # 六维审查标准
├── docs/                  # 文档
│   ├── USAGE.md
│   ├── configuration_guide.md
│   └── V1_V2_CONTRACT.md  # 双入口职责说明
├── research-intake/
├── research-draft/
├── research-review/
├── auto-review-loop-llm/
├── feishu-notify/
├── paper-plan/
├── paper-plan-zh/
├── paper-write-zh/
├── paper-compile/
├── paper-figure/
└── research-pipeline/
```

## v1 与 v2 的关系

### v1：`research`

适合：**从立项到初稿，再到常规审查的主流程**

```text
paper-intake → paper-draft → paper-review-loop → paper-figure → paper-supplement → paper-export-en
```

核心特点：

- 四角色编排
- 中文论文写作
- 最多 4 轮常规审查
- 负责“写”和“推进”

### v2：`research_2`

适合：**投稿前、返修前、答辩前的严格审查**

v2 不替代 v1，也**不会默认由 `/research` 自动切换进入**。  
当你需要更严格的审查时，应显式调用 `/research_2`。

v2 额外强化：

- 六维审查标准（新增创新性、研究空白）
- 证据深度溯源验证
- 可选的跨模型对抗性评审
- 最多 6 轮审查
- 负责“审”和“挑问题”

## 如何选择

| 场景 | 推荐 |
|------|------|
| 论文写作（从材料到初稿） | `/research` |
| 已有草稿，准备深度把关 | `/research_2` |
| 快速成稿 + 常规 review | `/research` |
| 投稿前严格审查 | `/research_2` |

## 文档

| 文档 | 说明 |
|------|------|
| [USAGE.md](docs/USAGE.md) | 完整使用指南，包括平台配置和模型选择 |
| [configuration_guide.md](docs/configuration_guide.md) | 详细配置说明 |
| [V1_V2_CONTRACT.md](docs/V1_V2_CONTRACT.md) | v1 / v2 边界、调用规则与推荐用法 |

## 与 ARIS 的区别

| 功能 | ARIS | 本项目 |
|------|------|-------|
| 语言 | 英文 | 中文优先 |
| 角色 | 英文 | Coordinator / Executor / Reviewer / Supervisor |
| 论文格式 | 西文期刊 | 中文期刊 / 会议优先 |
| 入口结构 | 单主线 | v1 写作 + v2 严格审查 |
| 审查重点 | 基础流程 | 审查增强、创新性与空白点复核 |

## 参考

- ARIS 原版: https://github.com/CNMarsCake/ARIS-fork
