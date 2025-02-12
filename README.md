# md_to_image

## 简介

`md_to_image` 是一个将 Markdown 文件转换为图像的工具。它使用现代 Web 技术和 Python 库来渲染 Markdown 内容，并生成高质量的图像文件。

## 技术栈

- **Python**: 核心编程语言。
- **Playwright**: 用于自动化浏览器操作，渲染 HTML 内容。
- **MarkdownIt**: 用于解析和渲染 Markdown 内容。
- **Pygments**: 用于代码块的语法高亮。
- **mdit-py-plugins**: 提供额外的 Markdown 功能，如脚注和任务列表。

## 使用方法

### 环境准备

1. 确保已安装 Python 3.7 或更高版本。
2. 安装所需的 Python 库：
   ```bash
   pip install -r requirements.txt
   ```

### 运行程序
1.将 Markdown 文件放置在项目目录中。
2.运行 md_to_image.py 脚本，指定 Markdown 文件路径
```bash
python md_to_image.py ./your_markdown_file.md
```
3.转换后的图像将保存在 output_images 目录中。