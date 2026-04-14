# paper-export-en 阶段提示词

## 阶段目标

将中文草稿转换为英文 LaTeX 论文，准备提交格式。

## 触发条件

- `draft_zh.md` 通过 paper-review-loop（评分 ≥ 8/10）
- `figure_draft_*.md` 完成（若 FIGURE_ENABLED=true）
- `supplement_*.md` 完成（若 SUPPLEMENT_ENABLED=true）
- 用户明确要求 export-en

## 产出文件

| 文件 | 说明 |
|------|------|
| `paper/main.tex` | LaTeX 主文件 |
| `paper/refs.bib` | 参考文献（仅引用条目） |
| `paper/figures/` | 图表文件 |
| `paper/supplements/` | 补充材料（如有） |
| `paper/*.sty` | 模板样式文件 |
| `paper/compile.log` | 编译日志 |

## 工作流程

### Step 1: 翻译协调

`Coordinator` 判断：
- 是否需要全文翻译（中文 → 英文）
- 或仅结构转换（中文已准备好结构）
- 或混合模式（核心内容英文化，Methods 保留中文参考）

### Step 2: 模板选择

`Executor` 选择 venue 模板：
- ICLR 2026
- NeurIPS 2026
- ICML 2026
- Nature / Science
- 自定义（用户提供 .sty）

### Step 3: LaTeX 生成

`Executor` 按 section 生成：
1. `main.tex`（主文件 + 各 section）
2. `refs.bib`（从 claims_evidence_matrix.md 提取引用）
3. Figure includes（从 figure_draft_*.md 提取渲染指令）

### Step 4: 编译检查

`Supervisor` 执行：
- `latexmk -pdf main.tex`
- 检查 .log 中的错误和警告
- 修复常见错误（undefined references, overfull hbox）

### Step 5: 格式检查

`Supervisor` 执行：
- 页数检查（是否在 venue limit 内）
- 字体嵌入检查
- 引用格式检查

## LaTeX 生成模板片段

```latex
\title{Your Title Here}

\author{
  Author One\textsuperscript{1} \and
  Author Two\textsuperscript{1,2} \\
  \textsuperscript{1}Institution One \\
  \textsuperscript{2}Institution Two \\
  correspondence@example.com
}

\begin{abstract}
Your English abstract here (150-300 words).
\end{abstract}

\section{Introduction}
\label{sec:intro}
...

\section{Related Work}
\label{sec:related}
...

\section{Methods}
\label{sec:methods}
...

\section{Experiments}
\label{sec:experiments}
...

\section{Conclusion}
\label{sec:conclusion}
...

\bibliography refs
\bibliographystyle{acl_natbib}
```

## Executor任务清单

1. 确认 venue 模板
2. 生成/更新 `main.tex`
3. 提取并清理 `refs.bib`（移除未引用条目）
4. 插入 figure 引用（`\ref{fig:1}` 等）
5. 运行首次编译
6. 修复编译错误
7. 生成最终 PDF

## Supervisor检查清单

- [ ] `latexmk` 编译成功（0 errors）
- [ ] 无 undefined references
- [ ] 无 overfull hbox（> 3 处）
- [ ] 页数符合 venue limit
- [ ] abstract 长度符合要求
- [ ] 引用格式符合 venue

## De-AI Polishing（可选）

在翻译/撰写后，可选执行去 AI 写作模式：
- 移除常见 AI 短语（"delve into", "pivotal", "landscape" 等）
- 简化过长句子
- 强化动词，避免 "is/are + adj" 结构

## 注意事项

- **翻译质量**：如果中文草稿质量高，翻译应保留学术严谨性，避免机器翻译腔
- **引用清理**：确保 .bib 只包含正文中引用的条目（可用 `latexmk -c` 清理）
- **路径兼容性**：Copilot Chat 模式下，确保所有文件路径使用相对路径
