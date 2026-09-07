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
sudo docker compose up -d --build
```

本机预览为 <http://localhost:8080>，仅绑定回环地址。

### Self-hosted Runner + Traefik

项目已生成 `.github/workflows/docker.yml`：在 GitHub 托管 Runner 上严格构建、测试并构建镜像，通过后仅 `main` 的 push 在 self-hosted Linux Runner 部署。Runner 需安装 Python 3、Docker Compose，并允许免密码执行 `sudo docker`。

在 GitHub **Settings → Environments → production** 中只需添加一个 Variable：

```dotenv
COURSE_DOMAIN=course.example.edu
```

可选 `COURSE_DATA_ROOT` 指定 Docker 宿主机上的绝对数据目录，不填则使用项目独立命名卷；可选 `COURSE_PORT` 修改本机诊断端口，默认 8080。宿主机绑定目录须提前创建，并对应用运行用户可写。

Traefik 应已连接 `traefik_default` 网络，提供 `web`、`websecure` 入口，并持有域名对应证书或已配置入口级证书解析器。模板启用 TLS，但不创建证书解析器。

```bash
sudo docker network inspect traefik_default
COURSE_DOMAIN=course.example.edu python3 scripts/deploy.py
```

`scripts/deploy.py` 校验输入后写入唯一的 0600 临时 env 文件，所有 Compose 命令使用 `sudo docker compose --env-file ...`，成功或失败都会清理文件。不会依赖 sudo 保留 Runner 环境变量，不会打印配置值。手动使用 `.env` 时执行：

```bash
cp .env.example .env
# 编辑 .env 中的域名后执行：
sudo docker compose --env-file .env -f docker-compose.yml -f docker-compose.traefik.yml up -d --build --wait
```

Docker 站点发布在域名根路径；生成时的 `site_url` 应与实际域名一致。网页和附件在镜像内，`/data` 不由 Nginx 对外提供。

### 以后接入 Django

当前模板仍为静态站，没有账号、上传接口或 Django 服务。`course_config.py` 为以后新增的 Django 后端提供公共配置；在后端 `settings.py` 中调用：

```python
from course_config import django_settings

globals().update(django_settings())
```

只设置 `COURSE_DOMAIN` 即可推导 HTTPS、`ALLOWED_HOSTS` 和 CSRF 来源。生产密钥首次启动生成并原子保存到 `/data/.django-secret-key`，重复启动及多进程并发使用同一个值，无需手动配置 Django Secret。数据库为 `/data/course.sqlite3`，上传目录为 `/data/uploads/`。需同时备份数据库、密钥及上传目录。

增加后端时还需自行添加 Django 依赖、应用、认证与上传路由，修改 Dockerfile 的运行入口和 Traefik 目标端口。容器内非 root 应用用户须能写入 `/data`；不要将私有上传目录挂到公开静态服务。切换已有数据卷前先迁移数据，不要重新生成已有密钥。

旧项目可显式覆盖 `COURSE_DJANGO_SECRET_KEY`、`COURSE_PUBLIC_ORIGIN`、`COURSE_ALLOWED_HOSTS`、`COURSE_CSRF_TRUSTED_ORIGINS`、`COURSE_DB_PATH` 和 `COURSE_MEDIA_ROOT`。这些扩展变量需在后端 Compose 中显式传入容器；默认静态站工作流只接收域名、数据目录与诊断端口。Django 的子域通配写法是 `.example.edu`，不是 `*.example.edu`。本地后端开发可设置 `COURSE_DEBUG=1`，数据默认存入被 Git 忽略的 `data/`。

{% endif -%}
## 提交前检查

```bash
uv run make clean
uv run make dirhtml SPHINXOPTS="-W --keep-going"
uv run python -m unittest discover -s tests -v
```
