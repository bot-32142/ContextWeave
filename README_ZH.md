**中文** | [English](README.md)

# 上下文感知翻译（CAT）

CAT 是一个适合长篇小说、书籍、PDF、扫描文档、漫画和字幕的**全自动**桌面翻译工具。它的目标是在尽量保留源文件格式的同时，让整部作品的术语和翻译风格保持一致。

[高级文档](https://bot-32142.github.io/context-aware-translation/) 介绍术语记忆、前文注入、格式保留、CLI 自动化和高级用例。

## 适合谁使用

- 小说、网文和轻小说翻译
- 需要保持名称和术语一致的长书或长文档
- 需要先 OCR 再翻译的扫描书、PDF 和漫画
- 想使用桌面工作流，而不是手动维护提示词的人

## 为什么用 CAT

- 可以从源材料自动构建术语表
- 会跨章节和页面持续带入上下文，并把有用摘要随术语表一起提供给翻译模型
- 对原生文本文件保留原始格式
- 文本、EPUB、PDF、扫描页、漫画和字幕可以用同一个应用处理

## 安装

当前桌面版构建没有签名，所以第一次启动时系统可能会弹出安全提示。

### macOS

- 下载最新的 `.dmg`
- 打开后把 `CAT-UI.app` 拖到 `Applications`
- 从 `Applications` 启动 `CAT-UI.app`
- 如果 macOS 因为开发者无法验证而阻止启动，打开 `系统设置` -> `隐私与安全性`
- 在 `安全性` 区域里为 `CAT-UI.app` 点击 `仍要打开`，然后再确认 `打开`

### Windows

- 下载最新的 `.zip`
- 解压到任意目录
- 运行 `CAT-UI.exe`
- 如果 Windows SmartScreen 提示应用无法识别，点击 `更多信息` -> `仍要运行`

<details>
<summary><strong>设置</strong></summary>

### 1. 打开项目首页，然后点击 `设置向导`

这里是项目首页。第一次使用时，直接点 `设置向导` 就行。

![项目首页](docs/screenshots/CN/latest_projects_overview.png)

### 2. 选择服务商并填入 API key

向导会先收集需要的连接。对大多数用户来说，`DeepSeek` + `Gemini` 是最实用的起点。

![设置向导服务商选择](docs/screenshots/CN/latest_setup_wizard_provider_selection.png)

### 3. 检查工作流配置档案

这个步骤会展示每个流程步骤实际会使用哪个连接和模型。

![工作流配置档案检查](docs/screenshots/CN/latest_setup_wizard_workflow_profile_review.png)

`质量优先` 会非常非常贵，除非你只用 `DeepSeek`。`均衡` 适合作为默认选择。`预算优先` 适合优先压低成本。

</details>

## 翻译

### 1. 新建项目

填写项目名、目标语言和工作流配置档案。

![新建项目对话框](docs/screenshots/CN/latest_new_project_dialog.png)

### 2. 打开项目工作页

按阅读顺序导入文件，这样术语和上下文才能在整本书里保持一致，然后点击翻译并导出开始翻译。双击文件如果你想手动审查每一步的结果或者修图。

![项目工作页](docs/screenshots/CN/latest_project_work_overview.png)

### 3. 可选：导入现成术语翻译

打开 `术语` 页，如果你已经有术语表，就用 `导入术语` 直接导入。最简单的 JSON 形式就是 `{"original": "translated"}`。

![术语总览](docs/screenshots/CN/latest_terms_overview.png)

## 示例 EPUB

这个示例 EPUB 是直接从 Project Gutenberg 上的法语《基督山伯爵》第一卷 EPUB [17989](https://www.gutenberg.org/ebooks/17989) 用 `翻译并导出` 一键生成的。模型为 `DeepSeek`。

如果换成 `Gemini` 或 `GPT`，质量通常会明显更好，但成本也会显著上升。

- [基督山伯爵.epub](demo/基督山伯爵.epub) - 简体中文版，每本成本不到 `18 元人民币`。

## CLI

CAT 也包含一个小型 CLI，可用于配置驱动的一次性翻译和基础书库管理。从源码目录运行时使用 `uv run cat-cli`；安装成包后使用 `cat-cli`。

```bash
cat-cli config path
cat-cli config init
cat-cli config validate

cat-cli run ./book.epub --output ./translated/book.epub
cat-cli run ./chapter.txt --output ./translated/chapter.txt --json
cat-cli run ./episode.srt --output ./translated/episode.srt --no-polish

cat-cli books list
cat-cli books show BOOK_ID
cat-cli books delete BOOK_ID --yes
```

CLI 会依次从 `--config`、`CAT_CONFIG`、向上查找最近的 `cat.yaml`/`.cat.yaml`，以及 `cat-cli config path` 显示的平台默认路径读取配置。配置结构与设置界面对应：`connections` 定义服务商端点，`workflow_profiles` 决定每个翻译步骤使用哪条模型路线。建议使用 `api_key_env`，让 API key 留在环境变量中，而不是写入配置文件或任务快照。一次性运行需要跳过润色时可使用 `--no-polish`，这对时间轴敏感的字幕输出很有用。

带注释的起始配置可参考 [docs/examples/cat-cli.yaml](docs/examples/cat-cli.yaml)。

## 使用前需要知道

- 目前主要测试过的是 `DeepSeek` + `Gemini` 的向导配置路径。`Claude` 和 `GPT` 应该也能工作得很好，但不建议使用低于 `DeepSeek` 水平的模型。
- 图片编辑成本很高，而且仍然容易出现幻觉。
- OCR 不会保留 PDF 和扫描书的原始排版，而是根据识别出的内容重建输出。漫画是例外。
- 如果你希望术语和上下文持续累积，请按阅读顺序导入。
- 由于跨格式测试成本较高，目前样本仍然有限。欢迎报告 bug。

## 支持格式

| 类型 | 导入 | 导出 | 翻译前是否需要 OCR |
| --- | --- | --- | --- |
| 文本 | `.txt`, `.md` | `txt` | 否 |
| PDF | `.pdf` | `epub`, `md` | 是 |
| 扫描书籍 | 图片文件或文件夹 | `epub`, `md` | 是 |
| 漫画 | `.cbz`、图片文件夹 | `cbz` | 是 |
| EPUB | `.epub` | `epub`, `md`, `docx`, `html` | 否，但支持图片 OCR |
| 字幕 | `.srt`, `.vtt`, `.ass`, `.ssa` | `srt`, `vtt`, `ass`, `ssa` | 否 |
