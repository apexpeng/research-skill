# Supervisor Memory

## Stable Mission

- 负责流程门禁、缺项拦截、轮次上限检查。
- 负责研究输出的项目归档与目录整洁，避免多项目混放。
- **新增**：figure/supplement 阶段完整性检查、跨平台路径兼容性检查。

## Always Check

### 基础检查

- [ ] 当前输出是否归入激活项目目录
- [ ] 是否存在 `~/.codex/research-workspace/outputs/ACTIVE_PROJECT.md`
- [ ] 是否把不同项目错误写进同一 `paper` 目录
- [ ] 审查、修订、门禁三步是否都真实发生

### 增强检查（ARIS 改进）

- [ ] `paper-figure` 阶段：figure 描述与正文引用一致性
- [ ] `paper-supplement` 阶段：补充材料不重复主稿
- [ ] 跨平台散落检测（Codex 路径 vs Copilot 路径）
- [ ] review loop 断点恢复文件 `REVIEW_STATE.json` 存在性（如有）

## Repeated Mistakes To Prevent

### 原有

- 不默认所有项目继续写入 `...\outputs\paper\` 根目录
- 不在缺少独立审稿记录时放行
- 不忽略重复环境问题（例如 MiniMax 端点配置错误）

### 新增（ARIS 借鉴）

- 不在 Copilot Chat 模式下混用 Windows 绝对路径和 POSIX 路径
- 不跳过 `paper-figure` 阶段的 figure-正文一致性检查
- 不在 `paper-supplement` 阶段遗漏重复内容检测
- 不在 review loop 中途丢失状态（检查 REVIEW_STATE.json）

## Preferred Actions

### 原有

- 根目录有散落输出时，优先运行整理脚本
- 激活项目不明确时，先查看 ACTIVE_PROJECT.md
- 发现复发错误时，沉淀到全局 memories

### 新增（ARIS 借鉴）

- 当 paper-review-loop 超过 2 轮时，检查是否需要自适应轮次扩展
- Copilot Chat 模式下优先使用 POSIX 路径（`~/.codex/`）
- 发现 MCP 连接问题时，在 memory 中记录 provider 状态

## 跨平台路径规范

```
Codex 模式（Windows）：
  C:\Users\<USER>\.codex\research-workspace\
  C:\Users\<USER>\.codex\skills\research\

Copilot Chat / Linux / macOS：
  ~/.codex/research-workspace/
  ~/.codex/skills/research/

路径检测：
  if Path.home() / ".codex" exists → Copilot mode
  elif C:\Users\ exists → Codex mode
  else → 混合警告
```

## 质量评分追踪（ARIS 借鉴）

Supervisor应维护当前项目的评分历史：

```json
{
  "project_key": "...",
  "review_scores": [
    {"round": 0, "score": 5.0, "date": "2026-04-10"},
    {"round": 1, "score": 6.5, "date": "2026-04-11"}
  ],
  "threshold": 6.0,
  "status": "in_progress"
}
```

若连续 2 轮评分无变化（< 0.3 分差），向Coordinator报告"边际收益递减"。

## Last Updated

- 2026-04-14：增加跨平台检查、figure/supplement 阶段、评分追踪（借鉴 ARIS）
