# paper-figure 阶段提示词

## 阶段目标

为论文生成图表描述和图注，准备最终图表渲染所需的所有文本材料。

## 触发条件

- `draft_zh.md` 已通过 `paper-review-loop`（评分 ≥ 6/10）
- `outline_zh.md` 中包含 figure 需求
- `FIGURE_ENABLED = true`

## 产出文件

| 文件 | 说明 |
|------|------|
| `figure_draft_01.md` | Figure 1 描述（数据来源、图表类型、关键趋势） |
| `figure_draft_02.md` | Figure 2 描述（如有） |
| ... | ... |
| `figure_caption_draft.md` | 所有图的图注草稿 |
| `figure_layout_plan.md` | 多图排版建议（如有） |

## figure_draft_*.md 模板

```markdown
# Figure X: [标题]

## 图表类型
[柱状图 / 折线图 / 热力图 / 散点图 / 流程图 / 示意图]

## 数据来源
- 实验批次：[实验编号]
- 数据文件：[路径或引用]
- 生成方式：[自动生成 / 手动绘制]

## 预期内容
- X 轴：[变量 + 单位]
- Y 轴：[变量 + 单位]
- 图例：[如有，图例项]
- 关键趋势：[描述预期观察到的模式]

## 正文引用位置
- 首次引用：draft_zh.md 第 ? 段
- 相关引用：第 ? 段

## 渲染备注
- 颜色方案：[venue 要求或默认配色]
- 分辨率：[300dpi / 600dpi]
- 特殊要求：[如有]
```

## figure_caption_draft.md 模板

```markdown
# Figure Captions (图注草稿)

## Figure 1: [标题]
[自包含的图注描述，足以让读者不读正文就理解主要发现。150字以内。]

## Figure 2: [标题]
[...]

## Table X: [标题]
[自包含的表注描述。...]
```

## Executor任务清单

1. 阅读 `draft_zh.md`，识别所有 figure 引用标记 `[FIGURE X]`
2. 阅读 `outline_zh.md` 中的 figure plan（如有）
3. 对每个 figure 生成 `figure_draft_*.md`
4. 生成汇总的 `figure_caption_draft.md`
5. 检查 figure 数量与正文引用是否一致

## Supervisor检查清单

- [ ] 所有 figure_draft_*.md 与 draft_zh.md 中的 `[FIGURE X]` 标记数量一致
- [ ] 每个 figure_caption 在 draft_zh.md 中有对应引用
- [ ] figure 之间无内容重复
- [ ] 图注描述符合 venue 字数限制（如有）

## 注意事项

- **自动生成范围**：数据驱动图表（训练曲线、柱状图、热力图）可自动生成描述
- **手动绘制范围**：架构图、流程图、模型示意图等需手动创建，在 `figure_draft_*.md` 中标注 `[MANUAL]`
- **Figure 4.0**：如果需要真正的图表渲染，可调用 `paper-figure` skill 生成 matplotlib/seaborn 代码
