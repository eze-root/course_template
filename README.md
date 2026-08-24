# Course Cookiecutter

这是一个从 `examples/swu-docs` 提炼出的课程站点脚手架。它保留了原项目中比较成熟的技术组合：Sphinx、MyST Markdown、Shibuya、Tailwind CSS、uv、本地热更新和自动部署；实验室品牌、NAS 挂载、域名与自托管服务器配置没有写死在模板中。

## 生成一门新课

仓库根目录执行：

```bash
uv run cookiecutter .
```

按提示填写课程名、课程代码、学期、作者等信息。生成后进入新目录：

```bash
cd <project_slug>
uv sync
npm install
uv run make dirhtml
```

本地实时预览：

```bash
uv run sphinx-autobuild -a source build/dirhtml --host 0.0.0.0 --port 8000
```

首次安装会生成 `uv.lock` 和 `package-lock.json`，建议和课程仓库一起提交。

也可以无交互生成：

```bash
uv run cookiecutter . --no-input \
  project_name="数据结构" \
  project_slug="data-structures" \
  course_code="CS201" \
  semester="2026 秋"
```

## 主要选项

| 选项 | 用途 |
| --- | --- |
| `project_name` / `project_slug` | 站点标题与目录名；中文课程名会默认转为拼音 slug，也可改成小写英文、数字和连字符 |
| `course_code` / `semester` | 首页及课程信息中的课程代码、开课学期 |
| `language` | Sphinx 站点语言，支持 `zh_CN` 或 `en` |
| `accent_color` | 站点强调色，使用六位十六进制颜色 |
| `deploy_to_github_pages` | 是否生成 GitHub Pages 工作流 |
| `include_docker` | 是否生成 Nginx 静态站点镜像配置 |
| `include_pdf` | 是否保留 XeLaTeX PDF 构建脚本与配置 |
| `initialize_git` | 是否在生成目录中执行 `git init -b main` |

## 生成后的内容

- `source/lectures/`：讲义与课堂内容
- `source/labs/`：实验指导
- `source/assignments/`：作业说明
- `source/resources/`：课程资源
- `source/_static/`：品牌图、样式、图片和可下载文件
- `docs/plans/`：课程建设与较大改版的设计记录
- `AGENTS.md`：面向后续 AI 协作的项目规则；这是必生成文件，不受任何可选项影响

模板默认生成一套最小示例页，确认构建正常后直接替换其中内容即可。

## 模板维护与测试

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

测试会分别渲染“最小功能”和“全部功能”两种项目，检查可选文件裁剪、模板变量残留以及 Python 配置语法。
