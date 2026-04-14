---
name: auto-review-loop-llm
description: 自主多轮研究审查循环。使用任意 OpenAI 兼容 LLM API 进行审查。触发："自动审查"、"llm审查"、"review loop llm"。
argument-hint: [topic-or-scope]
allowed-tools: Bash, Read, Write, Glob, Grep, TodoWrite, Agent
---

# Auto Review Loop (LLM): 自主研究改进

自主迭代：审查 → 实施修复 → 再次审查，直到外部审查者给出积极评价或达到最大轮次。

## 常量

- MAX_ROUNDS = 4
- POSITIVE_THRESHOLD: score >= 6/10 或 verdict 包含 "accept"、"sufficient"、"ready"
- REVIEW_DOC: `AUTO_REVIEW.md`
- HUMAN_CHECKPOINT = false

## LLM 配置

### 环境变量配置

```bash
# MiniMax (推荐)
export MINIMAX_API_KEY="your_key"

# DeepSeek
export DEEPSEEK_API_KEY="your_key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
```

## 状态持久化

```json
{
  "round": 2,
  "status": "in_progress",
  "last_score": 5.0,
  "timestamp": "2026-04-14T10:00:00"
}
```

## 工作流程

### Phase A: 审查

生成审查 prompt 并发送给外部 LLM。

### Phase B: 解析评估

提取 score、verdict、action items。

**停止条件**：score >= 6 且 verdict 包含 "ready" 或 "almost"

### Phase C: 实施修复

优先级：量化指标补充 > 重新表述 > 新实验

### Phase D: 记录轮次

更新 `REVIEW_STATE.json`

## 关键规则

- 先实施修复再审查
- 记录一切
- 轮次 2+ 需要包含前一轮上下文

## 调用示例

```
/auto-review-loop-llm "审查 draft_zh.md"
```
