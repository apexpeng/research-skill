# paper-supplement 阶段提示词

## 阶段目标

生成补充材料（Supplementary Materials），包括额外数据、Methods 细节、稳定性分析、补充图表等。

## 触发条件

- `draft_zh.md` 通过 paper-review-loop
- `figure_draft_*.md` 完成（如 FIGURE_ENABLED=true）
- `SUPPLEMENT_ENABLED = true`
- `project_brief.md` 中包含 supplement 需求

## 产出文件

| 文件 | 说明 |
|------|------|
| `supplement_01.md` | 补充材料 1 |
| `supplement_02.md` | 补充材料 2（如有） |
| `supplement_figures/` | 补充图表目录 |
| `supplement_table_*.md` | 补充表格 |
| `supplement_checklist.md` | 完整性自检清单 |

## supplement_*.md 模板

```markdown
# Supplement A: [标题]

## 补充内容类型
[额外实验 / Methods 细节 / 稳定性分析 / 理论证明 / 额外可视化]

## 与主稿关系
- 对应主稿 section：[?]
- 补充而非重复的理由：[说明为何放补充而非主稿]

## 内容

[详细补充内容...]

## 主稿引用方式
在主稿相应位置添加：
> "[具体引用文字]（见补充材料 A）"

## 独立可读性
[是 / 否，说明理由]
```

## supplement_checklist.md 模板

```markdown
# Supplement Completeness Checklist

## 基本检查
- [ ] 补充材料总数：[X]
- [ ] 每个 supplement 在主稿中有引用
- [ ] 每个 supplement 有独立可读性
- [ ] 无内容与主稿重复

## 格式检查
- [ ] 补充图表格式与主稿一致
- [ ] 表格有表注
- [ ] 引用编号连续（A, B, C...）

## 内容检查
- [ ] 所有实验数据完整
- [ ] 所有统计检验报告
- [ ] 额外 baseline 比较完整
- [ ] 稳定性/消融实验覆盖

## Venue 要求检查
- [ ] 补充材料页数符合要求（如有）
- [ ] 补充材料格式符合要求
```

## Executor任务清单

1. 阅读 `draft_zh.md` 和 `project_brief.md`，识别需要补充的内容
2. 识别补充材料的类型：
   - 额外实验数据
   - Methods 细节（伪代码、推导过程）
   - 稳定性分析（不同种子、不同配置）
   - 对立证据处理
   - 理论证明/补充
3. 对每类补充材料生成 `supplement_*.md`
4. 生成 `supplement_checklist.md`
5. 创建/放置补充图表到 `supplement_figures/` 目录

## 咚咚审查重点

1. **非重复性**：补充材料内容是否真的需要补充，而非主稿已有内容
2. **完整性**：实验细节是否足够他人复现
3. **引用一致性**：主稿中的引用标记是否准确

## Supervisor检查清单

- [ ] 每个 `supplement_*.md` 在 `draft_zh.md` 中有引用
- [ ] `draft_zh.md` 中没有把补充材料内容复制到主稿
- [ ] supplement figures 目录结构正确
- [ ] 所有补充材料已归档到 `projects/<key>/supplements/`

## 注意事项

- **不重复原则**：补充材料不是"放不下所以放这里"，而是"对主稿理解重要但不影响主稿连贯性的额外细节"
- **独立可读**：补充材料应该能独立被理解，不需要反复对照主稿
- **格式一致**：补充图表的样式应与主稿 figure 风格一致
