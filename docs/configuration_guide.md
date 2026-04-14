# Research Skill 配置说明

## 更新日期

2026-04-14

---

## 一、Skill 生态概览

### 1.1 完整 Skill 列表

```
research skill 生态 (共 14 个)
├── 核心工作流
│   ├── research              # 主 skill，协调者
│   ├── research-intake       # 立项阶段
│   ├── research-draft       # 起草阶段
│   ├── research-review      # ARIS 原版，外部审查
│   └── research-pipeline     # 全流程编排
│
├── 审查相关
│   ├── auto-review-loop-llm  # 多 LLM 审查（新建）
│   └── feishu-notify         # 飞书通知（已有）
│
├── 论文写作
│   ├── paper-plan            # ARIS 原版，英文规划
│   ├── paper-plan-zh         # 中文规划（新建）
│   ├── paper-write-zh        # 中文写作（新建）
│   └── paper-compile         # 编译（新建）
│
├── 图表生成
│   └── paper-figure          # ARIS 原版
│
└── 辅助工具
    ├── cc_switch_adapter.py  # 跨平台适配（新建）
    └── organize-research-outputs.py  # 输出整理（新建）
```

### 1.2 四角色体系

| 角色 | 名称 | 功能 | 默认模型 |
|------|------|------|---------|
| Coordinator | Coordinator | 阶段判定、任务分配 | LongCat-Flash-Chat |
| Executor | Executor | 执行写作、修订 | MiniMax-M2.7 |
| Reviewer | Reviewer | 独立审查、评分 | session-default |
| Supervisor | Supervisor | 门禁判定、完整性检查 | session-default |

---

## 二、目录结构

### 2.1 研究工作区

```
~/.codex/research-workspace\
├── outputs/
│   ├── ACTIVE_PROJECT.md      # 当前激活项目标记
│   ├── ACTIVE_PROJECT.json     # 项目配置
│   ├── PROJECT_INDEX.json      # 项目索引
│   ├── paper/                  # 旧式收件箱（临时）
│   └── projects/
│       └── <project_key>/
│           ├── paper/          # 论文相关文件
│           ├── agent_runs/     # 外部 worker 运行记录
│           ├── figures/        # 图表
│           ├── supplements/     # 补充材料
│           └── REVIEW_STATE.json  # 审查循环状态
```

### 2.2 Skill 安装目录

```
~/.codex/skills\
├── research/                    # 核心 research skill
│   ├── SKILL.md               # 主配置文件
│   ├── SKILL_ECOSYSTEM.md    # 生态说明
│   ├── feishu_integration.md  # 飞书整合指南
│   ├── agents/
│   │   ├── coordinator/agent.md
│   │   ├── executor/agent.md
│   │   ├── reviewer/agent.md
│   │   └── supervisor/
│   │       ├── agent.md
│   │       └── memory.md
│   ├── config/
│   │   └── role-model-routing.json  # 角色模型路由
│   ├── references/
│   │   ├── quality-baseline.md
│   │   ├── adaptive-stages.md
│   │   ├── workflow-map.md
│   │   ├── runtime-defaults.md
│   │   └── external-workers.md
│   ├── templates/
│   │   ├── prompts/
│   │   │   ├── paper-figure.prompt.md
│   │   │   ├── paper-supplement.prompt.md
│   │   │   └── paper-export-en.prompt.md
│   │   └── outputs/
│   │       ├── project_brief.template.md
│   │       └── ...
│   └── scripts/
│       ├── cc_switch_adapter.py
│       ├── organize-research-outputs.py
│       └── invoke_research_role.py
│
├── research-intake/
│   └── SKILL.md
├── research-draft/
│   └── SKILL.md
├── research-review/           # ARIS 原版
│   └── SKILL.md
├── research-pipeline/          # ARIS 原版
│   └── SKILL.md
├── auto-review-loop-llm/
│   └── SKILL.md
├── feishu-notify/
│   └── SKILL.md
├── paper-plan/
│   └── SKILL.md               # ARIS 原版（英文）
├── paper-plan-zh/
│   └── SKILL.md
├── paper-write-zh/
│   └── SKILL.md
├── paper-compile/
│   └── SKILL.md
├── paper-figure/              # ARIS 原版
│   └── SKILL.md
└── 其他 skills...
```

---

## 三、配置文件详解

### 3.1 角色模型路由配置

**文件**: `config/role-model-routing.json`

```json
{
    "updated_at": "2026-04-14",
    "providers": {
        "longcat": {
            "transport": "openai-chat-completions",
            "base_url": "https://api.longcat.chat/openai/v1",
            "api_key_env": "LONGCAT_API_KEY"
        },
        "minimax": {
            "transport": "anthropic-messages",
            "base_url": "https://api.minimax.io/anthropic",
            "api_key_env": "MINIMAX_API_KEY"
        },
        "openai-codex": {
            "transport": "native-codex"
        }
    },
    "roles": {
        "coordinator": {
            "name": "Coordinator",
            "provider": "longcat",
            "model": "LongCat-Flash-Chat"
        },
        "executor": {
            "name": "Executor",
            "provider": "minimax",
            "model": "MiniMax-M2.7"
        },
        "reviewer": {
            "name": "Reviewer",
            "provider": "openai-codex",
            "worker_mode": "native-codex"
        },
        "supervisor": {
            "name": "Supervisor",
            "provider": "openai-codex",
            "worker_mode": "native-codex"
        }
    }
}
```

### 3.2 飞书通知配置

**文件**: `~/.claude/feishu.json`

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID",
  "interactive": {
    "bridge_url": "http://localhost:5000",
    "timeout_seconds": 300
  }
}
```

**mode 选项**:
- `"off"` 或文件不存在: 关闭（默认）
- `"push"`: 仅推送通知
- `"interactive"`: 双向交互（需 bridge）

### 3.3 环境变量配置

**Windows (Codex 模式)**:

```bash
# 必需
set LONGCAT_API_KEY=your_longcat_key
set MINIMAX_API_KEY=your_minimax_key

# 可选
set ARIS_MAX_ROUNDS=4
set ARIS_POSITIVE_THRESHOLD=6.0
set ARIS_FIGURE_ENABLED=true
set ARIS_SUPPLEMENT_ENABLED=true
set ARIS_ADAPTIVE_ROUNDS=false

# 中国区 MiniMax
set MINIMAX_BASE_URL=https://api.minimaxi.com/anthropic
```

**macOS/Linux (Copilot Chat 模式)**:

```bash
# 必需
export LONGCAT_API_KEY=your_longcat_key
export MINIMAX_API_KEY=your_minimax_key

# 可选
export ARIS_MAX_ROUNDS=4
export ARIS_POSITIVE_THRESHOLD=6.0
```

---

## 四、工作流程

### 4.1 标准阶段流程

```
paper-intake
    ↓ [project_brief.md + claims_evidence_matrix.md]
paper-architecture
    ↓ [outline_zh.md]
paper-draft
    ↓ [draft_zh.md]
paper-review-loop (最多 4 轮)
    ↓ [评分 ≥ 6/10]
paper-figure (可选)
    ↓
paper-supplement (可选)
    ↓
paper-export-en
    ↓
[投稿准备]
```

### 4.2 四角色协作模式

```
用户输入
    ↓
Coordinator（调度）
    ↓ 分配任务
Executor（执行） → 生成文件
    ↓ 提交审查
Reviewer（审查） → 输出评分 + 问题清单
    ↓ 门禁判定
Supervisor（监督） → 通过/阻塞
    ↓
Coordinator → 下一阶段或结束
```

### 4.3 多轮审查循环

```
Round N
    ├── Coordinator宣布目标
    ├── Reviewer独立审查 → review_round_0X.md
    ├── Executor修订 draft_zh.md
    ├── Supervisor门禁判定
    └── 评分 ≥ 6? → 结束
         评分 < 6 且 N < 4 → 继续下一轮
         评分 < 6 且 N = 4 → 需人工决策
```

---

## 五、跨平台支持

### 5.1 平台检测

CC-Switch Adapter 自动检测当前平台：

| 平台 | 检测依据 | 工作区路径 |
|------|---------|-----------|
| Codex (Windows) | `os.name == 'nt'` | `~/.codex/` |
| Copilot Chat | `GITHUB_COPILOT_CHAT` 环境变量 | `~/.codex/` |
| WSL | `WSL_DISTRO_NAME` 环境变量 | `~/.codex/` |

### 5.2 路径解析

```python
# 自动选择正确的路径
from cc_switch_adapter import get_workspace_base, get_research_workspace

base = get_workspace_base()  # 自动适配当前平台
workspace = get_research_workspace()
```

---

## 六、输出文件规范

### 6.1 核心文件

| 文件 | 阶段 | 说明 |
|------|------|------|
| `project_brief.md` | intake | 项目简介 |
| `claims_evidence_matrix.md` | intake | 主张-证据矩阵 |
| `outline_zh.md` | architecture | 论文大纲 |
| `draft_zh.md` | draft | 中文初稿 |
| `review_round_0X.md` | review | 审查记录 |
| `figure_draft_*.md` | figure | 图表描述 |
| `supplement_*.md` | supplement | 补充材料 |

### 6.2 状态文件

| 文件 | 说明 |
|------|------|
| `ACTIVE_PROJECT.json` | 当前项目配置 |
| `REVIEW_STATE.json` | 审查循环断点恢复 |
| `review_scores.json` | 评分历史追踪 |

---

## 七、ARIS 原版 vs 中文增强版对比

| 功能 | ARIS 原版 | 中文增强版 | 优势 |
|------|----------|----------|------|
| 审查模型 | Codex MCP (GPT-5.4) | 环境变量配置 | 更灵活 |
| 四角色 | 英文角色 | Coordinator/Executor/Reviewer/Supervisor | 中文用户友好 |
| 论文规划 | paper-plan (英文) | paper-plan-zh | 中文输出 |
| 论文写作 | paper-write (英文) | paper-write-zh | 中文输出 |
| 跨平台 | 无 | CC-Switch Adapter | Codex + Copilot |

---

## 八、快速开始

### 8.1 基本使用

```
# 启动研究工作流
/research "您研究的主题或方向"

/research-intake "研究材料或主题描述"

/research-draft "基于 outline_zh.md 生成草稿"

/research-review "审查 draft_zh.md"

/paper-plan-zh "生成中文论文大纲"

/paper-write-zh "基于大纲生成中文论文"

/paper-compile paper/  # 编译论文
```

### 8.2 飞书通知开启

1. 创建飞书群机器人
2. 获取 Webhook URL
3. 创建 `~/.claude/feishu.json`
4. 设置 `"mode": "push"` 或 `"interactive"`

### 8.3 外部 LLM 配置

```bash
# MiniMax (推荐)
export MINIMAX_API_KEY=your_key

# DeepSeek
export DEEPSEEK_API_KEY=your_key
export DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

---

## 九、故障排除

### 9.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 外部 worker 调用失败 | API Key 未设置 | 检查环境变量 |
| 路径错误 | 跨平台路径不兼容 | 使用 cc_switch_adapter.py |
| 飞书通知不工作 | 配置文件缺失或 mode=off | 检查 feishu.json |
| 审查循环无限 | 评分持续低于阈值 | 4轮后需人工决策 |

### 9.2 调试命令

```bash
# 检查平台检测
python cc_switch_adapter.py

# 检查项目状态
python organize-research-outputs.py --Command check

# 测试飞书连接
curl -s -X POST "YOUR_WEBHOOK_URL" -H "Content-Type: application/json" -d '{"msg_type":"text","content":{"text":"test"}}'
```

---

## 十、附录

### 10.1 相关资源

- ARIS 原版: https://github.com/CNMarsCake/ARIS-fork
- CC-Switch 适配器: 内置于 `scripts/cc_switch_adapter.py`
- 飞书机器人配置: `feishu-notify/SKILL.md`

### 10.2 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-04-14 | v2.0 | 全面更新，支持 CC-Switch 跨平台 |
| 2026-04-08 | v1.0 | 初始版本 |
