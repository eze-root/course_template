FROM node:22-bookworm-slim AS styles

WORKDIR /site
COPY package.json ./
RUN npm install
COPY scripts/build_css.sh scripts/build_css.sh
COPY source source
RUN bash scripts/build_css.sh

FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim AS docs

WORKDIR /site
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml README.md ./
RUN uv sync --no-dev
COPY --from=styles /site/source source
# Production images should build usable docs even when a non-fatal Sphinx
# warning exists. Keep -W for the explicit strict check in CI/pre-commit.
RUN uv run --no-sync python -m sphinx -M dirhtml source build --keep-going

FROM nginx:1.29-alpine
COPY --from=docs /site/build/dirhtml /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=6 \
  CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
