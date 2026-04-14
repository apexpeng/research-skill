---
name: research-draft
description: 研究写作工作流 - 起草阶段。基于 outline_zh.md 生成 draft_zh.md 中文初稿。使用中文输出，严格主张-证据对齐。
argument-hint: [outline_zh.md 或 project_brief.md]
allowed-tools: Bash, Read, Write, Glob, Grep, TodoWrite, Agent, mcp__codex__codex
---

# Research Draft: 起草阶段

## 阶段目标

基于 `outline_zh.md` 生成完整中文初稿 `draft_zh.md`。

## 输入要求

- `project_brief.md` — 项目目标
- `claims_evidence_matrix.md` — 主张-证据矩阵
- `outline_zh.md` — 论文大纲（若无，参考 paper-plan）

## 输出文件

```
research-workspace/outputs/projects/<project_key>/paper/
└── draft_zh.md  # 中文初稿
```

## draft_zh.md 结构要求

```markdown
# [论文标题]

## Abstract
[150-250字，结构：问题→方法→结果→影响]

## 1. Introduction
[1-1.5页：问题动机→研究空白→核心贡献]

## 2. Related Work
[0.5-1页：分类综述→本文定位]

## 3. Methods
[1.5-2页：问题形式化→方法描述→技术细节]

## 4. Experiments
[2-3页：实验设置→主实验→消融实验]

## 5. Conclusion
[0.5页：总结→局限性→未来方向]

## References
[仅引用正文涉及的文献]
```

## 写作规则

### 证据对齐规则

| 规则 | 说明 |
|------|------|
| 主张必须有证据 | 每条 [C#] 主张对应 [E#] 证据 |
| 推测必须标注 | 无法确定的机制 → [推测] 或 [待验证] |
| 避免因果混淆 | 相关性 ≠ 因果性，除非有消融实验 |
| 量化优先 | 用具体数字，少用"显著改善"等模糊词 |

### 禁止事项

- ❌ 把"可能"写成"确定"
- ❌ 跳过消融实验直接声称因果
- ❌ 使用"首次"、"最优"等无法证伪的表述
- ❌ 忽略对立证据或局限性

### Figure 标记

在正文适当位置插入 `[FIGURE 1]`、`[FIGURE 2]` 等标记，指向待生成图表。

## 工作流程

### Step 1: Executor - 读取输入

1. 读取 `outline_zh.md`，理解章节结构
2. 读取 `claims_evidence_matrix.md`，理解证据分布
3. 识别 Figure 需求（几个图、什么类型）

### Step 2: Executor - 分节起草

按顺序生成各 section：
1. **Abstract** — 高度浓缩，4 句话覆盖全部贡献
2. **Introduction** — 漏斗式：宽泛问题 → 具体挑战 → 本文贡献
3. **Related Work** — 不是文献列表，是综合分析
4. **Methods** — 技术细节充分，但不过度
5. **Experiments** — 表格化结果优先，描述为辅
6. **Conclusion** — 诚实局限性，不过度泛化

### Step 3: Executor - 自检

生成后自检：
- [ ] 每条主张有证据支撑？
- [ ] 推测已标注？
- [ ] Figure 引用位置合理？
- [ ] 无过度声明？

### Step 4: Supervisor - 门禁

- [ ] `draft_zh.md` 存在且 > 1000 字
- [ ] 包含所有必需 section
- [ ] [FIGURE X] 标记数量与 outline 一致

## 与 ARIS paper-write 的区别

| 方面 | ARIS paper-write | 本 skill |
|------|------------------|---------|
| 输出语言 | 英文 LaTeX | 中文 Markdown |
| 模板 | ICLR/NeurIPS | 中文期刊/会议 |
| Figure | 生成 matplotlib | 仅描述标记 |
| LaTeX | 直接输出 | 仅草案，需后续转换 |

## 调用示例

```
/research-draft "基于 outline_zh.md 生成中文初稿"
```
