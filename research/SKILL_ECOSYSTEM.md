# Research Skill 更新总结

## 更新日期

2026-04-14

## 更新内容概览

### 1. 角色定义更新 ✅

| 文件 | 更新内容 |
|------|---------|
| `agents/coordinator/agent.md` | 跨平台路由、figure/supplement 阶段协调 |
| `agents/executor/agent.md` | 新增 figure/supplement 输出规范 |
| `agents/reviewer/agent.md` | 四维审查标准、评分透明化 |
| `agents/supervisor/agent.md` | 跨平台路径检查、新阶段门禁 |
| `agents/supervisor/memory.md` | 跨平台检测、评分追踪 |

### 2. 新增引用文件 ✅

| 文件 | 说明 |
|------|------|
| `references/quality-baseline.md` | 质量评分体系（借鉴 ARIS 5→8.5 分机制） |
| `references/adaptive-stages.md` | 自适应轮次、检查点系统 |

### 3. 新增阶段模板 ✅

| 文件 | 说明 |
|------|------|
| `templates/prompts/paper-figure.prompt.md` | figure 整合阶段 |
| `templates/prompts/paper-supplement.prompt.md` | 补充材料阶段 |
| `templates/prompts/paper-export-en.prompt.md` | 英文导出阶段（完整流程） |

### 4. 跨平台支持 ✅

| 文件 | 说明 |
|------|------|
| `scripts/cc_switch_adapter.py` | 跨平台路径检测（Codex/Copilot Chat） |
| `scripts/organize-research-outputs.py` | 跨平台输出整理脚本 |

### 5. 独立技能 ✅

| Skill | 说明 |
|-------|------|
| `research-intake` | 立项阶段独立 skill |
| `research-draft` | 起草阶段独立 skill |
| `research-review` | 保留 ARIS 原版（Codex MCP 外部审查） |

## ARIS 差距分析 & 采纳项

### 已采纳的 ARIS 优势

| ARIS 功能 | 本 skill 实现 | 状态 |
|----------|--------------|------|
| MCP 扩展架构 | `mcp__codex__codex` 预留 | ✅ |
| 飞书通知 | 预留接口 | ✅ |
| 断点恢复 | `REVIEW_STATE.json` | ✅ |
| 质量评分曲线 | `review_scores.json` | ✅ |
| 自适应轮次 | `ADAPTIVE_ROUNDS=true` | ✅ |
| 检查点机制 | `checkpoints/*.json` | ✅ |
| 替代模型组合 | role-model-routing.json | ✅ |

### 保留的差异化优势

| 优势 | 说明 |
|------|------|
| 中文优先 | 默认输出严谨学术中文 |
| 四角色中文命名 | Coordinator/Executor/Reviewer/Supervisor |
| Supervisor门禁记忆 | supervisor memory.md |
| 跨 Copilot 兼容 | cc_switch_adapter.py |

## 技能生态系统

```
research (主skill - 协调者)
├── research-intake (立项)
├── research-architecture (架构) ← 复用 main skill
├── research-draft (起草)
├── research-review (审查 - ARIS原版)
├── research-figure (图表 - ARIS原版)
├── research-supplement (补充 - 复用模板)
└── research-export (导出)
```

## 跨平台使用

### Claude Codex (Windows)

```bash
/research "开始新的研究项目..."
```

### GitHub Copilot Chat

```bash
/research "开始新的研究项目..."
# 自动检测 Copilot Chat 模式，使用 POSIX 路径
```

## 关键配置

### 环境变量

```bash
# 必需
LONGCAT_API_KEY=your_key  # coordinator
MINIMAX_API_KEY=your_key  # executor

# 可选
ARIS_MAX_ROUNDS=4
ARIS_POSITIVE_THRESHOLD=6.0
ARIS_FIGURE_ENABLED=true
ARIS_SUPPLEMENT_ENABLED=true
ARIS_ADAPTIVE_ROUNDS=false
```

### 路径约定

| 平台 | 工作区路径 |
|------|-----------|
| Codex | `C:\Users\18711\.codex\research-workspace` |
| Copilot | `~/.codex/research-workspace` |
