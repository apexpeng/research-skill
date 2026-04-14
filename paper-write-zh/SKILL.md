---
name: paper-write-zh
description: 基于大纲生成中文 LaTeX 论文章节。使用中文输出。触发："写论文"、"中文latex"、"开始写"。
argument-hint: [venue-or-outline]
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, WebSearch, WebFetch
---

# Paper Write 中文版: 按章节生成中文 LaTeX

基于 **$ARGUMENTS** 生成中文 LaTeX 论文。

## 常量

- **TARGET_VENUE = `中文期刊/会议`** — 默认格式。支持的格式：中文期刊、EI会议、SCI期刊、中文模板
- **MAX_PAGES** — 正文页数限制（中文期刊通常 8-10 页）
- **OUTPUT_LANG = `zh-CN`**

## 输入

1. **PAPER_PLAN.md** — 含 claims-evidence matrix、章节计划、figure 计划（来自 `/paper-plan-zh`）
2. **draft_zh.md** — 中文草稿（主要内容来源）
3. **Generated figures** — PDF/PNG 文件在 `figures/`（来自 `/paper-figure`）
4. **中文 LaTeX 模板** — 期刊/会议提供的模板文件

如果不存在 PAPER_PLAN.md，询问用户先运行 `/paper-plan-zh` 或提供简要大纲。

## 项目结构

```
paper/
├── main.tex                    # 主文件
├── chinese_thesis.cls          # 或中文期刊模板 .cls
├── math_commands.tex           # 共享数学宏
├── references.bib              # 参考文献（仅引用条目）
├── sections/
│   ├── 0_abstract.tex          # 摘要
│   ├── 1_introduction.tex      # 引言
│   ├── 2_related.tex           # 相关工作
│   ├── 3_method.tex            # 方法
│   ├── 4_experiment.tex        # 实验
│   ├── 5_discussion.tex        # 讨论
│   ├── 6_conclusion.tex        # 结论
│   └── appendix.tex            # 附录（如有）
└── figures/                    # 图表文件
```

## 工作流程

### Step 0: 备份和清理

如果 `paper/` 已存在，备份到 `paper-backup-{timestamp}/` 再覆盖。

### Step 1: 初始化项目

1. 创建 `paper/` 目录
2. 使用中文期刊模板（如有用户提供的模板）
3. 生成 `math_commands.tex`（数学符号定义）
4. 创建章节文件（按 PAPER_PLAN 结构）

### Step 2: 生成数学命令文件

```latex
% math_commands.tex — 共享符号定义
\usepackage{amsmath,amssymb}
\newcommand{\R}{\mathbb{R}}
\newcommand{\E}{\mathbb{E}}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}
% 论文特定符号...
```

### Step 3: 逐节写作

按顺序处理各节：

**§0 摘要：**
- 结构：问题 → 方法 → 结果 → 意义
- 包含一个具体定量结果
- 150-300 字（检查期刊限制）
- 不含 `\begin摘要}` — 那是在 main.tex 中

**§1 引言：**
- 开头：1-2 句问题动机
- 研究缺口：现有方法的不足
- 贡献列表：编号，对应 claims-evidence matrix
- 结尾：简要 roadmap
- 目标：1-1.5 页

**§2 相关工作：**
- 按类别组织，使用 `\paragraph`
- 不是文献列表，是综合分析
- 最短 0.8-1 页

**§3 方法/实验设计：**
- 符号定义（引用 math_commands.tex）
- 问题形式化
- 方法描述
- 目标：1.5-2 页

**§4 实验结果：**
- 先给出实验设置（数据集、baseline、指标）
- 主实验结果表格/图表在前
- 然后消融实验
- 每个主张在引言中都有对应证据
- 目标：2-3 页

**§5 讨论：**
- 主要发现的深入分析
- 诚实局限性评估
- 目标：0.5-1 页

**§6 结论：**
- 总结贡献（不是从引言复制）
- 未来工作 1-2 个具体方向
- 目标：0.3-0.5 页

### Step 4: 构建参考文献

**关键：只包含正文中引用的条目。**

1. 扫描所有 `\citep{}` 和 `\citet{}`
2. 构建引用 key 列表
3. 检查现有 `.bib` 文件
4. 如果未找到，搜索正确信息
5. 写 `references.bib`（只含引用的条目）

### Step 5: 交叉引用检查

- 确保所有 `\ref{}` 和 `\label{}` 匹配
- 确保所有 `\citep{}` / `\citet{}` 有对应 BibTeX 条目

### Step 6: 最终检查

- [ ] 所有 `\ref{}` 和 `\label{}` 匹配（无 undefined references）
- [ ] 所有 `\citep{}` / `\citet{}` 有对应 BibTeX 条目
- [ ] Figure/table 编号正确
- [ ] 页数在 MAX_PAGES 内
- [ ] 无 TODO/FIXME/XXX 标记
- [ ] 摘要自包含

## 中文 LaTeX 模板示例

**中文期刊通用：**
```latex
\documentclass{ctexart}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
```

**中文会议：**
```latex
\documentclass[UTF8]{article}
\usepackage{ctex}
\usepackage{amsmath}
```

## 关键规则

- **不要生成作者信息** — 用占位符或匿名
- **输出完整章节，不是大纲** — 应该可编译
- **每个主张必须有证据引用** — 对照 claims-evidence matrix
- **可编译** — 输出应该可以用 latexmk 编译（除缺失图表外）
- **不过度声明** — 使用"表明"、"显示"等适度语言
- **页数限制** — 参考文献和附录不计数

## 与 ARIS paper-write 的区别

| 方面 | ARIS paper-write | 本 skill |
|------|-----------------|---------|
| 输出语言 | 英文 | **中文** |
| 默认模板 | ICLR/NeurIPS/ICML | **中文期刊/会议** |
| 章节结构 | 西文学术风格 | **中文期刊规范** |
| 引用格式 | natbib | **中文 GB/T 7714** |

## 调用示例

```
/paper-write-zh "基于 PAPER_PLAN.md 生成中文论文"
/paper-write-zh "sections: 1_introduction, 2_related"  # 只写特定章节
```
