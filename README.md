# 课程网站 Cookiecutter 模板

这个仓库不是某一门课程的网站，而是一个“课程项目生成器”。每次开新课时运行一次，它会创建一个可以直接编写、预览和部署的独立课程仓库。

生成的课程项目默认包含：

- Sphinx + MyST Markdown 文档站；
- 讲义、实验、作业和课程资源目录；
- Shibuya 主题与 Tailwind CSS；
- uv 管理的 Python 环境；
- 本地实时预览脚本；
- 必生成的 `AGENTS.md` 协作规则；
- 可选的 GitHub Pages、Docker 和 PDF 配置。

## 1. 准备环境

先确认本机有以下命令：

```bash
uv --version
node --version
npm --version
```

推荐使用 Python 3.13 和 Node.js 20 以上版本。Python 无需提前手动创建虚拟环境，uv 会负责安装和管理。

## 2. 生成一门新课

进入本模板仓库：

```bash
cd /path/to/course_template
```

运行 Cookiecutter，并把新课程生成到模板仓库的上一级目录：

```bash
uv run cookiecutter . --output-dir ..
```

命令会逐项询问课程信息。比如要创建“数据结构”：

| 提示项 | 示例填写 | 说明 |
| --- | --- | --- |
| `project_name` | `数据结构` | 课程网站标题 |
| `project_slug` | `data-structures` | 生成的目录名，只使用小写英文、数字和连字符；直接回车会根据中文名生成拼音 |
| `project_description` | `数据结构课程讲义与实验` | 首页和项目简介 |
| `course_code` | `CS201` | 课程代码 |
| `semester` | `2026 秋` | 开课学期 |
| `course_start_date` | `2026-09-01` | 页面初始日期，格式必须为 `YYYY-MM-DD` |
| `author_name` | `张老师` | 课程负责人 |
| `author_email` | `teacher@example.com` | 项目元数据中的联系邮箱 |
| `language` | `1` | `1` 是中文，`2` 是英文 |
| `site_url` | `https://courses.example.com/data-structures` | 计划部署的站点地址 |
| `accent_color` | `#d95c41` | 网站强调色 |
| `deploy_to_github_pages` | `1` | `1` 生成，`2` 不生成 GitHub Pages 工作流 |
| `include_docker` | `1` | `1` 不生成，`2` 生成 Docker 配置 |
| `include_pdf` | `1` | `1` 不生成，`2` 生成 PDF 构建脚本 |
| `initialize_git` | `1` | `1` 自动初始化 Git，`2` 不初始化 |

如果填写的 `project_slug` 是 `data-structures`，最终目录就是：

```text
/path/to/data-structures/
```

也可以在任何目录使用模板的绝对路径：

```bash
uvx cookiecutter /path/to/course_template --output-dir /path/to/courses
```

## 3. 启动刚生成的课程网站

进入生成目录并安装依赖：

```bash
cd /path/to/data-structures
uv sync
npm install
```

启动实时预览：

```bash
bash scripts/dev.sh
```

浏览器打开 <http://localhost:8000>。修改 Markdown 或 CSS 后，页面会自动重新构建和刷新。

只想构建一次、不启动预览服务器时：

```bash
uv run make dirhtml
```

构建结果位于 `build/dirhtml/`。

首次执行 `uv sync` 和 `npm install` 会生成 `uv.lock`、`package-lock.json`，应该把它们提交到新课程仓库。

## 4. 开始编写课程内容

生成项目中的主要目录如下：

```text
data-structures/
├── AGENTS.md
├── README.md
├── source/
│   ├── index.md
│   ├── lectures/
│   ├── labs/
│   ├── assignments/
│   ├── resources/
│   └── _static/
├── scripts/
├── tests/
└── docs/plans/
```

各目录用途：

- `source/index.md`：课程首页；
- `source/lectures/`：每周讲义；
- `source/labs/`：实验指导；
- `source/assignments/`：作业要求与评分标准；
- `source/resources/`：教材、软件和延伸阅读；
- `source/_static/imgs/`：课程图片；
- `source/_static/files/`：学生可下载的附件；
- `docs/plans/`：较大的课程建设或改版计划。

例如，添加第 2 讲：

```bash
cp source/lectures/lesson-01-introduction.md \
  source/lectures/lesson-02-linear-lists.md
```

修改新文件的 frontmatter、一级标题和正文，然后在 `source/lectures/index.md` 的 toctree 中加入：

````md
```{toctree}
:maxdepth: 1

lesson-01-introduction
lesson-02-linear-lists
```
````

站内链接使用 docname，不写 `.html`：

```md
请先阅读 {doc}`/lectures/lesson-01-introduction`。
```

图片放入 `source/_static/imgs/`，引用方式为：

```md
![示意图](/_static/imgs/example.png)
```

## 5. 使用 AGENTS.md

每个课程项目都会在根目录生成 `AGENTS.md`，不能通过选项关闭。它用于告诉 Codex 等代码代理：

- 课程资料应该放在哪里；
- 页面 frontmatter 和导航如何维护；
- 应该使用哪些构建、测试和预览命令；
- 哪些构建产物、凭据和学生数据不能提交；
- Git、部署和完成验收遵循什么规则。

开课后可以继续补充本课程特有的规则，例如作业发布流程、讲义命名方式和允许公开的资料范围。

## 6. 构建与检查

提交课程内容前运行：

```bash
uv run make clean
uv run make dirhtml SPHINXOPTS="-W --keep-going"
uv run python -m unittest discover -s tests -v
```

如果严格构建成功，静态网站就在 `build/dirhtml/`。

常用命令：

| 命令 | 用途 |
| --- | --- |
| `bash scripts/dev.sh` | 实时预览 Markdown 与 CSS |
| `npm run build:css` | 只编译 Tailwind CSS |
| `uv run make dirhtml` | 构建静态 HTML |
| `uv run make clean` | 清理构建目录 |
| `uv run python -m unittest discover -s tests -v` | 检查项目结构和配置 |

## 7. 可选部署方式

### GitHub Pages

生成时选择 `deploy_to_github_pages=yes`，项目会包含 `.github/workflows/pages.yml`。

1. 把新课程仓库推送到 GitHub；
2. 打开仓库的 **Settings → Pages**；
3. 把 Source 设为 **GitHub Actions**；
4. 推送 `main` 分支，工作流会构建并发布网站。

### Docker

生成时选择 `include_docker=yes`：

```bash
docker compose up -d --build
```

默认访问 <http://localhost:8080>。

### PDF

生成时选择 `include_pdf=yes`，并在系统中安装 XeLaTeX：

```bash
uv run bash scripts/build_pdf.sh
```

PDF 会复制到 `source/_static/pdfs/`。

## 8. 无交互生成

需要批量创建课程时，可以直接传入参数：

```bash
uv run cookiecutter . \
  --no-input \
  --output-dir .. \
  project_name="数据结构" \
  project_slug="data-structures" \
  project_description="数据结构课程讲义与实验" \
  course_code="CS201" \
  semester="2026 秋" \
  course_start_date="2026-09-01" \
  author_name="张老师" \
  author_email="teacher@example.com" \
  site_url="https://courses.example.com/data-structures" \
  deploy_to_github_pages="yes" \
  include_docker="no" \
  include_pdf="no" \
  initialize_git="yes"
```

## 9. 维护模板本身

修改 Cookiecutter 模板后，在模板仓库运行：

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

测试会渲染最小配置、完整配置和英文配置，并确认 `AGENTS.md`、可选文件、页面 frontmatter 与 Sphinx 配置正常。
