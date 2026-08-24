# 课程项目协作约定

## 项目定位

本仓库是 **{{ cookiecutter.project_name }}（{{ cookiecutter.course_code }}）** 的课程网站与教学资料。站点使用 Sphinx + MyST Markdown，不在文档目录中混入应用服务代码。

内容应面向学生、可直接操作，并优先记录长期稳定的课程知识。具体学期才有效的通知应明确写出学期与日期。

## 内容组织

- `source/lectures/`：课堂讲义，建议按 `lesson-01-topic.md` 命名；
- `source/labs/`：实验指导，建议按 `lab-01-topic.md` 命名；
- `source/assignments/`：作业说明与公开评分标准；
- `source/resources/`：教材、环境配置和延伸阅读；
- `source/_static/imgs/`：页面图片；
- `source/_static/files/`：可下载附件；
- `docs/plans/`：课程建设或大型改版计划。

每篇 `source/**/*.md` 页面按以下顺序组织：frontmatter、同名一级标题、`article-info`、正文。frontmatter 至少包含 `title`、`date`、`author` 和 `tags`；展示的作者与日期必须一致。

新增或移动页面时：

- 同步更新所属目录 `index.md` 的 toctree；
- 用 docname 建立站内链接，不写 `.html`；
- 图片统一引用 `/_static/imgs/<文件名>`；
- 全局搜索并更新旧链接；
- 不再使用但仍有教学价值的材料先移至归档目录，不直接删除。

## 工具链

- Python 环境与依赖统一由 uv 管理；用 `uv add` / `uv remove` 修改依赖，不手改 `uv.lock`；
- 用 `npm install` 安装前端依赖，修改后提交 `package-lock.json`；
- HTML 构建：`uv run make clean && uv run make dirhtml`；
- 本地预览：`bash scripts/dev.sh`；
{% if cookiecutter.include_pdf == "yes" -%}
- PDF 构建：`uv run bash scripts/build_pdf.sh`；
{% endif -%}
- 不提交 `build/`、`.venv/`、`node_modules/` 和生成的 CSS/PDF。

## 样式与资源

- Tailwind 源文件位于 `source/_static/css/src/site.css`，编译产物 `source/_static/css/site.css` 不提交；
- 改动样式后执行 `uv run make clean && uv run make dirhtml`，确认明暗主题、导航和代码块没有退化；
- 品牌图使用 `source/_static/logo.svg` 与 `favicon.svg`，替换时同步检查 `source/conf.py`；
- 不直接修改 Sphinx 或 Shibuya 安装目录中的文件，定制统一放在仓库内。

## 文档工作流

把课程资料改动当作代码改动，保持术语、命令、日期、导航和评分说明内部一致。

完成任务前：

- 涉及渲染、导航或交叉引用时执行 `uv run make clean && uv run make dirhtml SPHINXOPTS="-W --keep-going"`；
{% if cookiecutter.include_pdf == "yes" -%}
- 涉及 PDF 内容或 LaTeX 配置时执行 `uv run bash scripts/build_pdf.sh`；
{% endif -%}
- 执行 `uv run python -m unittest discover -s tests -v`；
- 修复新引入的 warning，不用 suppress 规则掩盖真实问题；
- 纯文本小修改且不影响渲染、导航、链接时可以跳过完整构建。

## Git 与变更范围

- 一个任务对应一个逻辑变更，避免混入无关格式化或课程内容；
- 不覆盖学生提交、教师草稿或工作区中已有的未提交修改；
- 重命名、移动页面前全局搜索引用，改动后再次确认没有旧路径；
- 不提交密钥、token、账号、内部地址、受版权限制的教材全文或学生隐私数据。

{% if cookiecutter.deploy_to_github_pages == "yes" or cookiecutter.include_docker == "yes" -%}
## 部署

{% if cookiecutter.deploy_to_github_pages == "yes" -%}
- `main` 分支推送会触发 GitHub Pages 构建；较大的改动应先在分支验证，严格构建通过后再合入；
{% endif -%}
{% if cookiecutter.include_docker == "yes" -%}
- Docker 只负责构建并托管静态站点；端口、域名和反向代理配置留在部署环境，不写入课程内容；
{% endif -%}
- 部署失败先读取构建日志并定位根因，不通过反复推送试错。

{% endif -%}
## 完成标准

- 内容、导航、交叉引用和附件路径一致；
- 影响渲染或导航的修改通过严格构建，无新增 warning；
- 示例命令经过检查，不包含个人凭据、内网地址或机器专属绝对路径；
- 学期、截止时间、评分规则等高影响信息有明确来源，并保持相关页面同步。
- `AGENTS.md` 与实际目录、命令和部署方式一致。
