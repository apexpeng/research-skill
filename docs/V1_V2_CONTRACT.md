# V1 / V2 Contract

本文档用于说明 `research` 与 `research_2` 的职责边界，避免 README、主 skill 和子 skill 之间出现调用契约不一致。

## 1. 入口规则

- `research`：v1 主入口，负责写作主流程
- `research_2`：v2 独立入口，负责审查增强
- 当前仓库中，**不得默认假设 `/research` 会自动切换到 v2**

## 2. 推荐调用方式

```text
/research "研究主题"       # 用于立项、起草、常规审查
/research_2 "深度审查草稿" # 用于投稿前严格复核
```

## 3. 边界划分

### `research`

负责：

- 立项
- 大纲
- 起草
- 常规审查
- figure / supplement / export 阶段推进

不负责：

- 默认接管严格审查
- 自动启用对抗性评审
- 隐式切换到 v2

### `research_2`

负责：

- 六维审查
- 创新性评估
- 研究空白识别
- 证据深度验证
- 可选的跨模型对抗性审查

不负责：

- 替代完整写作流程
- 重新定义前面各阶段的输出结构
- 冒充“通用全自动科研系统”

## 4. 产物兼容性

v2 审查建议复用 v1 的产物作为输入，例如：

- `project_brief.md`
- `claims_evidence_matrix.md`
- `outline_zh.md`
- `draft_zh.md`

v2 可新增：

- `evidence_validation.md`
- `innovation_assessment.md`
- `review_risk_register.md`

## 5. 文档一致性要求

以下位置必须保持同一契约：

- `README.md`
- `research/SKILL.md`
- `research_2/SKILL.md`
- 相关子 skill 文档

若后续修改调用方式，应同步更新上述文件。
