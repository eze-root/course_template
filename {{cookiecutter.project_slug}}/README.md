# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

- 课程代码：`{{ cookiecutter.course_code }}`
- 开课学期：{{ cookiecutter.semester }}
- 课程负责人：{{ cookiecutter.author_name }}
- 站点地址：[{{ cookiecutter.site_url }}]({{ cookiecutter.site_url }})

## 开始使用

需要 Python {{ cookiecutter.python_version }}+、[uv](https://docs.astral.sh/uv/) 和 Node.js 20+。

```bash
uv sync
npm install
uv run make dirhtml
```

生成结果位于 `build/dirhtml/`。本地实时预览：

```bash
bash scripts/dev.sh
```

默认访问 <http://localhost:8000>。首次安装生成的 `uv.lock` 与 `package-lock.json` 应提交到版本库。

## 编写课程内容

课程页面都放在 `source/` 下：

- `lectures/`：每周讲义；
- `labs/`：实验指导；
- `assignments/`：作业与评分说明；
- `resources/`：教材、软件和延伸阅读；
- `_static/imgs/`：图片；
- `_static/files/`：学生可下载的附件。

每个 Markdown 页面保留以下结构：

````md
---
title: 页面标题
date: 2026-09-01
author: {{ cookiecutter.author_name }}
tags: [讲义]
---

# 页面标题

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: 2026-09-01
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```
````

新增页面后，把它加入相应目录 `index.md` 的 `{toctree}`。站内链接使用 docname，例如 `` {doc}`lectures/lesson-01-introduction` ``，不要写死 `.html`。

## 常用命令

```bash
# 严格构建；CI 也执行这一条
uv run make clean
uv run make dirhtml SPHINXOPTS="-W --keep-going"

# 只构建 CSS
npm run build:css

# 实时预览 Markdown 和 CSS
bash scripts/dev.sh
```

{% if cookiecutter.include_pdf == "yes" -%}
## 构建 PDF

系统需安装 XeLaTeX 及课程内容需要的中文字体：

```bash
uv run bash scripts/build_pdf.sh
```

生成的 PDF 会复制到 `source/_static/pdfs/`。

{% endif -%}
{% if cookiecutter.deploy_to_github_pages == "yes" -%}
## GitHub Pages 部署

推送 `main` 分支会执行 `.github/workflows/pages.yml`。首次使用时，在 GitHub 仓库的 **Settings → Pages → Build and deployment** 中把 Source 设为 **GitHub Actions**。

{% endif -%}
{% if cookiecutter.include_docker == "yes" -%}
## Docker 部署

```bash
docker compose up -d --build
```

站点默认暴露在 <http://localhost:8080>。生产环境可在反向代理中接入该端口。

{% endif -%}
## 提交前检查

```bash
uv run make clean
uv run make dirhtml SPHINXOPTS="-W --keep-going"
uv run python -m unittest discover -s tests -v
```
