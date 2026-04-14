# Research Skills

基于 [ARIS](https://github.com/CNMarsCake/ARIS-fork) 的中文研究写作技能集，支持 Claude Codex 和 GitHub Copilot Chat 跨平台运行。

## 核心功能

- 🤖 **四角色工作流**：Coordinator（调度）、Executor（执行）、Reviewer（审查）、Supervisor（监督）
- 📝 **中文优先**：专为中文期刊/会议设计的论文写作流程
- 🔄 **迭代审查**：多轮审查循环，自动评分，持续改进
- 📊 **图表生成**：支持数据驱动图表的自动生成
- 🔔 **飞书通知**：可选的飞书集成，支持推送和交互模式
- 🌐 **跨平台**：支持 Claude Codex (Windows) 和 GitHub Copilot Chat

## 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| Claude Code (Windows) | ✅ | 使用 Codex 原生 skills |
| GitHub Copilot Chat | ✅ | 使用 Copilot Chat 扩展 |
| VS Code Copilot | ✅ | 通用兼容 |

## 技能列表

### 核心工作流

| 技能 | 说明 | 版本 |
|------|------|------|
| `research` | 主协调技能，管理四角色工作流 | v1 |
| `research_2` | 集百家之长的下一代研究工作流 | v2 |

### 子技能（v1 & v2 通用）

| 技能 | 说明 |
|------|------|
| `research-intake` | 立项阶段：生成 project_brief 和 claims_evidence_matrix |
| `research-draft` | 起草阶段：基于大纲生成中文初稿 |
| `research-review` | 外部审查（基于 ARIS） |

### 审查循环

| 技能 | 说明 |
|------|------|
| `auto-review-loop-llm` | 多轮自主审查循环 |
| `feishu-notify` | 飞书通知集成 |

### 论文写作

| 技能 | 说明 |
|------|------|
| `paper-plan` | 英文论文规划（ARIS 原版） |
| `paper-plan-zh` | 中文论文规划 |
| `paper-write-zh` | 中文论文写作 |
| `paper-compile` | LaTeX 编译 |
| `paper-figure` | 图表生成（ARIS 原版） |

### 全流程

| 技能 | 说明 |
|------|------|
| `research-pipeline` | 端到端研究管线（基于 ARIS） |

## 快速开始

### 1. 安装

```bash
git clone https://github.com/ApexPeng/research-skills.git
cp -r research-skills/* ~/.claude/skills/
```

### 2. 配置环境变量

```bash
# 必需
export LONGCAT_API_KEY="your_longcat_key"    # Coordinator 模型
export MINIMAX_API_KEY="your_minimax_key"      # Executor 模型

# 可选
export ARIS_MAX_ROUNDS=4
export ARIS_POSITIVE_THRESHOLD=6.0
```

### 3. 启动研究工作流

```bash
# 完整研究流程
/research "您的研究主题"

# 分阶段运行
/research-intake "研究材料描述"
/research-draft "生成中文初稿"
/research-review "审查草稿"
/paper-plan-zh "生成论文大纲"
/paper-write-zh "生成中文论文"
/paper-compile paper/
```

## 文档

| 文档 | 说明 |
|------|------|
| [USAGE.md](docs/USAGE.md) | 完整使用指南，包括平台配置和模型选择 |
| [configuration_guide.md](docs/configuration_guide.md) | 详细配置说明 |

## 工作流程

```
paper-intake → paper-draft → paper-review-loop → paper-plan-zh → paper-write-zh → paper-compile
    立项            起草           审查           规划            写作           编译
```

## 四角色协作

```
用户输入
    ↓
Coordinator（调度）→ 阶段判定、任务分配
    ↓
Executor（执行）→ 生成文件、内容写作
    ↓
Reviewer（审查）→ 独立审查、评分
    ↓
Supervisor（监督）→ 门禁判定、完整性检查
    ↓
循环直到达到投稿标准
```

## 模型配置

默认使用 LongCat + MiniMax 作为外部模型，Reviewer 和 Supervisor 使用当前会话模型。

**支持的模型提供商**：
- LongCat（Coordinator）
- MiniMax（Executor）
- Codex GPT-5.4（Reviewer/Supervisor）
- DeepSeek、GLM、Kimi 等（需配置）

详细配置请参考 [USAGE.md](docs/USAGE.md#模型配置)。

## 飞书通知（可选）

1. 创建飞书群机器人，获取 Webhook URL
2. 创建 `~/.claude/feishu.json`:

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID"
}
```

## 项目结构

```
research-skills/
├── research/              # v1 核心 skill（四角色论文写作工作流）
│   ├── agents/           # 四角色定义
│   ├── config/            # 角色路由配置
│   ├── references/        # 参考文档
│   ├── scripts/           # 跨平台适配脚本
│   └── templates/        # 阶段模板
├── research_2/           # v2 论文审查增强版
│   └── SKILL.md          # 六维审查标准
├── docs/                 # 文档
│   ├── USAGE.md          # 使用指南
│   └── configuration_guide.md  # 配置说明
├── research-intake/      # 立项阶段
├── research-draft/       # 起草阶段
├── research-review/      # 外部审查
├── auto-review-loop-llm/ # 多轮审查
├── feishu-notify/        # 飞书通知
├── paper-plan/           # 英文规划
├── paper-plan-zh/        # 中文规划
├── paper-write-zh/       # 中文写作
├── paper-compile/        # 编译
├── paper-figure/         # 图表生成
└── research-pipeline/    # 全流程管线
```

## 版本说明：v1 vs v2

本项目提供两个版本的研究技能，聚焦不同环节：

### v1: Research（基于 ARIS）

适合：**论文写作全流程**

```
paper-intake → paper-draft → paper-review-loop(4轮) → paper-figure → paper-supplement → paper-export-en
```

**核心特性：**
- 四角色工作流（Coordinator/Executor/Reviewer/Supervisor）
- 中文论文写作（paper-plan-zh / paper-write-zh）
- 迭代审查（最多 4 轮）
- 跨平台支持（Claude Codex / GitHub Copilot Chat）

### v2: Research_2（论文审查增强版）

适合：**深度论文审查**

v2 不追求全流程自动化，专注**审查这一个环节做到极致**。

**六维审查标准（v1 为四维）：**

| 维度 | v1 | v2 |
|------|----|----|
| 证据链完整性 | ✅ | ✅ |
| 逻辑严密性 | ✅ | ✅ |
| 审稿人风险 | ✅ | ✅ |
| 结构协调性 | ✅ | ✅ |
| 创新性评估 | ❌ | ✅ (+15%) |
| 研究空白识别 | ❌ | ✅ (+10%) |

**v2 独有特性：**
- 六维审查标准（+创新性、研究空白）
- 证据深度溯源验证
- 跨模型对抗性评审（可选）
- 最多 6 轮审查

### 如何选择

| 场景 | 推荐版本 |
|------|---------|
| 论文写作（从立项到初稿） | v1 |
| 深度审查（多轮、对抗性）| v2 |
| 快速写作+简单审查 | v1 |
| 高质量投稿前的严格审查 | v2 |

### 使用示例

```bash
# v1: 论文写作全流程
/research "论文写作"

/research-intake "研究材料"
/research-draft "生成初稿"
/research-review "审查草稿"

/research_2 "深度审查草稿"  # 启用六维审查
```

## 与 ARIS 的区别

| 功能 | ARIS | 本项目 |
|------|------|-------|
| 语言 | 英文 | 中文优先 |
| 角色 | 英文 | Coordinator/Executor/Reviewer/Supervisor |
| 论文格式 | 西文期刊 | 中文期刊/会议 |
| 跨平台 | 无 | Codex + Copilot |

## 参考

- ARIS 原版: https://github.com/CNMarsCake/ARIS-fork
- Claude Code: https://docs.anthropic.com/en/docs/claude-code
- GitHub Copilot Chat

## License

MIT
