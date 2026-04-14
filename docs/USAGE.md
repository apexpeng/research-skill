# Research Skills 使用指南

## 支持的平台

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| Claude Code (Windows) | ✅ 完整支持 | 使用 Codex 原生 skills |
| GitHub Copilot Chat | ✅ 完整支持 | 使用 Copilot Chat 扩展 |
| VS Code Copilot | ✅ 完整支持 | 通用兼容 |
| 其他 AI 工具 | ⚠️ 部分支持 | 需适配调用方式 |

---

## Claude Code 使用方法

### 1. 安装 Skills

**方式一：直接克隆到 skills 目录**
```bash
git clone https://github.com/ApexPeng/research-skills.git
cp -r research-skills/* ~/.claude/skills/
```

**方式二：复制单个 skill**
```bash
# 只安装 research 核心技能
cp -r research-skills/research ~/.claude/skills/

# 安装论文写作相关
cp -r research-skills/paper-plan ~/.claude/skills/
cp -r research-skills/paper-figure ~/.claude/skills/
cp -r research-skills/paper-write ~/.claude/skills/
cp -r research-skills/paper-compile ~/.claude/skills/
```

### 2. 配置环境变量

在终端或 `~/.claude/settings.local.json` 中设置：

```bash
# 必需：外部 API Keys
export LONGCAT_API_KEY="your_longcat_key"    # Coordinator 模型
export MINIMAX_API_KEY="your_minimax_key"      # Executor 模型

# 可选：自定义模型
export ARIS_COORDINATOR_MODEL="LongCat-Flash-Chat"
export ARIS_EXECUTOR_MODEL="MiniMax-M2.7"

# 可选：运行时配置
export ARIS_MAX_ROUNDS=4
export ARIS_POSITIVE_THRESHOLD=6.0
export ARIS_FIGURE_ENABLED=true
export ARIS_SUPPLEMENT_ENABLED=true
```

### 3. 启动工作流

在 Claude Code 中直接输入：

```bash
# 完整研究流程
/research "您的研究主题描述"

/research-intake "研究材料或主题"
/research-draft "生成中文初稿"
/research-review "审查草稿"
/paper-plan-zh "生成论文大纲"
/paper-write-zh "生成中文论文"
/paper-compile paper/
```

### 4. 使用子 Skills

```bash
# 只进行立项阶段
/research-intake "研究主题"

# 只进行论文规划
/paper-plan-zh "基于已有研究材料"

# 只进行审查
/research-review "paper.pdf"

# 使用多轮审查循环
/auto-review-loop-llm "审查草稿"
```

---

## GitHub Copilot Chat 使用方法

### 1. 安装 Skills

```bash
# 克隆到 Copilot Chat 的 skills 目录
git clone https://github.com/ApexPeng/research-skills.git
cp -r research-skills/* ~/.github/copilot/skills/
```

### 2. 配置环境变量

```bash
export LONGCAT_API_KEY="your_key"
export MINIMAX_API_KEY="your_key"
```

### 3. 使用命令

在 Copilot Chat 中使用相同的命令：

```bash
/research "研究主题"
/paper-plan-zh "生成大纲"
/paper-write-zh "生成论文"
```

---

## 模型配置

### 默认模型配置

| 角色 | 默认模型 | 提供商 | 用途 |
|------|---------|-------|------|
| Coordinator | LongCat-Flash-Chat | LongCat API | 流程调度 |
| Executor | MiniMax-M2.7 | MiniMax API | 内容生成 |
| Reviewer | session-default | 当前会话 | 审查评分 |
| Supervisor | session-default | 当前会话 | 门禁判定 |

### 修改模型配置

编辑 `research/config/role-model-routing.json`：

```json
{
    "roles": {
        "coordinator": {
            "provider": "longcat",
            "model": "LongCat-Flash-Chat"  // 可改为其他支持的模型
        },
        "executor": {
            "provider": "minimax",
            "model": "MiniMax-M2.7"  // 可改为 MiniMax-M2.5
        }
    }
}
```

### 支持的模型提供商

| 提供商 | 模型 | 配置方式 |
|-------|------|---------|
| **LongCat** | LongCat-Flash-Chat, LongCat-Flash-Thinking | `LONGCAT_API_KEY` |
| **MiniMax** | MiniMax-M2.7, MiniMax-M2.5 | `MINIMAX_API_KEY` |
| **DeepSeek** | deepseek-chat, deepseek-reasoner | 环境变量配置 |
| **GLM (Z.ai)** | glm-4, glm-4-plus | 环境变量配置 |
| **Kimi** | moonshot-v1-8k | 环境变量配置 |

### 使用 Codex MCP 作为 Reviewer

如果你有 Codex CLI 配置：

1. 安装 Codex：
```bash
npm install -g @openai/codex
codex setup  # 选择 gpt-5.4 模型
```

2. 在 Claude Code 中添加 MCP：
```bash
claude mcp add codex -s user -- codex mcp-server
```

3. Reviewer 将自动使用 Codex GPT-5.4

---

## 工作流程详解

### 四角色协作

```
用户输入
    ↓
Coordinator → 阶段判定、任务分配
    ↓
Executor → 生成文件、内容写作
    ↓
Reviewer → 独立审查、评分
    ↓
Supervisor → 门禁判定、完整性检查
    ↓
循环直到达到投稿标准
```

### 阶段流程

```
paper-intake     → project_brief.md + claims_evidence_matrix.md
    ↓
paper-draft     → draft_zh.md
    ↓
paper-review-loop → review_round_0X.md（最多4轮）
    ↓
paper-plan-zh    → PAPER_PLAN.md
    ↓
paper-figure     → figures/*.pdf（可选）
    ↓
paper-write-zh   → paper/main.tex
    ↓
paper-compile   → paper/main.pdf
```

### 审查评分标准

| 分数 | 含义 | 行动 |
|------|------|------|
| 8-10 | 优秀 | 可投稿 |
| 6-7 | 良好 | 小修后投稿 |
| 4-5 | 一般 | 大修后重审 |
| 0-3 | 较差 | 返回起草阶段 |

---

## 飞书通知配置（可选）

1. 创建飞书群机器人
2. 获取 Webhook URL
3. 创建 `~/.claude/feishu.json`：

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID"
}
```

4. 模式说明：
   - `"off"` 或文件不存在：禁用
   - `"push"`：仅推送通知
   - `"interactive"`：双向交互（需额外配置 bridge）

---

## 常见问题

### Q: 如何切换不同的审查模型？

编辑 `research/config/role-model-routing.json`，将 Reviewer 的 provider 改为支持的模型。

### Q: 外部 API 调用失败怎么办？

检查：
1. API Key 是否正确设置
2. 网络连接是否正常
3. API 配额是否充足

### Q: 如何跳过某些阶段？

直接在命令中指定目标阶段：
```bash
/research "主题" --skip-intake  # 跳过立项
```

### Q: 如何恢复中断的工作流？

工作流状态保存在：
- `REVIEW_STATE.json` - 审查循环状态
- `ACTIVE_PROJECT.json` - 当前项目配置

### Q: 支持中文期刊格式吗？

是的，使用 `paper-plan-zh` 和 `paper-write-zh` 生成中文论文。

---

## 高级配置

### 自定义角色模型

创建 `~/.claude/research-custom-routing.json`：

```json
{
  "roles": {
    "coordinator": {
      "provider": "custom",
      "base_url": "https://your-api.com/v1",
      "api_key_env": "YOUR_API_KEY",
      "model": "your-model"
    }
  }
}
```

### 启用自适应审查轮次

```bash
export ARIS_ADAPTIVE_ROUNDS=true  # 复杂项目可自动扩展到6轮
```

### 禁用可选阶段

```bash
export ARIS_FIGURE_ENABLED=false
export ARIS_SUPPLEMENT_ENABLED=false
```

---

## 技术支持

- GitHub Issues: https://github.com/ApexPeng/research-skills/issues
- ARIS 原版: https://github.com/CNMarsCake/ARIS-fork
