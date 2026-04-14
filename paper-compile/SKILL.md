---
name: paper-compile
description: 编译 LaTeX 到 PDF，自动修复错误，提交就绪检查。使用中文 LaTeX 支持。触发："编译"、"latex"、"编译pdf"。
argument-hint: [paper-directory]
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Paper Compile: LaTeX 编译与 PDF 生成

编译 LaTeX 论文到 PDF：**$ARGUMENTS**

## 常量

- **LATEXMK = `latexmk`** — 编译命令
- **PDFINFO = `pdfinfo`** — 页数检查
- **MAX_ERRORS = 3** — 允许的最大错误数（超过则停止）

## 输入

期望 `paper/` 目录包含：
- `main.tex` — 主文件
- `*.cls` 或 `*.sty` — 模板文件
- `sections/` — 章节文件（如有）
- `figures/` — 图表文件（如有）
- `references.bib` — 参考文献

## 工作流程

### Step 1: 检测环境

```bash
# 检测 latexmk 是否可用
latexmk --version

# 检测 pdftotext/pdfinfo 是否可用
pdfinfo -v
```

### Step 2: 编译

```bash
# 完整编译流程
cd paper/
latexmk -pdf main.tex

# 或带自动修复
latexmk -pdf -interaction=nonstopmode main.tex
```

### Step 3: 解析错误

解析 `.log` 文件，分类错误：

| 错误类型 | 严重程度 | 修复方式 |
|---------|---------|---------|
| `Undefined reference` | 高 | 检查 `\ref{}` 对应 `\label{}` |
| `Missing $` | 高 | 检查数学模式 |
| `File not found` | 高 | 检查文件路径 |
| `Overfull hbox` | 中 | 调整内容或使用 `\small` |
| `Underfull hbox` | 低 | 可忽略 |
| `Font not found` | 中 | 安装字体或使用替代 |

### Step 4: 自动修复

尝试自动修复常见错误：

1. **Undefined reference**：
   ```bash
   # 列出所有 undefined
   grep "Undefined reference" main.log
   # 检查对应 label
   grep -n "label{" main.tex sections/*.tex
   ```

2. **Font not found**：
   ```bash
   # 尝试使用默认字体
   # 或安装缺失字体
   ```

3. **Overfull hbox**：
   - 添加 `\small` 或 `\footnotesize`
   - 调整表格宽度

### Step 5: 重新编译

修复后重新编译：

```bash
latexmk -C  # 清理临时文件
latexmk -pdf main.tex
```

### Step 6: 页数检查

```bash
pdfinfo main.pdf | grep Pages
```

验证是否在页数限制内：
- 中文期刊：通常 8-10 页正文
- EI会议：通常 4-6 页
- ICLR/NeurIPS：9 页正文

### Step 7: 最终检查清单

- [ ] `latexmk` 编译成功（0 errors）
- [ ] 无 undefined references
- [ ] Overfull hbox < 3 处
- [ ] 页数符合限制
- [ ] 摘要长度符合要求
- [ ] 引用格式正确

## 常见问题修复

### 中文编译问题

如果使用中文 LaTeX：

```bash
# 使用 xelatex
latexmk -pdf -xelatex main.tex

# 或使用 lualatex
latexmk -pdf -lualatex main.tex
```

### 字体问题

```bash
# 查找缺失字体
grep "Font" main.log | grep "not found"

# 安装字体
# Ubuntu: apt install texlive-fonts-extra
# macOS: 默认包含
# Windows: 检查 MikTeX 字体包
```

### 图表路径问题

确保 `main.tex` 中的图表路径正确：

```latex
\usepackage{graphicx}
\graphicspath{{figures/}}
```

## 输出

```
paper/
├── main.pdf          # 最终 PDF
├── main.log          # 编译日志
├── main.aux          # 辅助文件
└── main.fls          # 文件列表
```

## 关键规则

- **最多重试 3 次**编译 — 避免无限循环
- **报告未解决的错误** — 不要隐藏问题
- **清理临时文件** — 使用 `latexmk -C`
- **验证页数** — 检查是否超限

## 调用示例

```
/paper-compile paper/          # 编译 paper/ 目录
/paper-compile                 # 编译当前目录的 paper/
```
