---
title: {{ cookiecutter.project_name | tojson }}
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}课程, 首页{% else %}course, home{% endif %}]
---

# {{ cookiecutter.project_name }}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

{% if cookiecutter.language == "zh_CN" -%}
欢迎来到 **{{ cookiecutter.course_code }} · {{ cookiecutter.semester }}** 课程主页。

{{ cookiecutter.project_description }}

## 课程导航
{% else -%}
Welcome to **{{ cookiecutter.course_code }} · {{ cookiecutter.semester }}**.

{{ cookiecutter.project_description }}

## Course navigation
{% endif %}

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} {% if cookiecutter.language == "zh_CN" %}课程讲义{% else %}Lectures{% endif %}
:link: lectures/index
:link-type: doc

{% if cookiecutter.language == "zh_CN" %}按课程进度阅读知识点、示例与课堂补充材料。{% else %}Read course topics, examples, and supplementary notes.{% endif %}
:::

:::{grid-item-card} {% if cookiecutter.language == "zh_CN" %}课程实验{% else %}Labs{% endif %}
:link: labs/index
:link-type: doc

{% if cookiecutter.language == "zh_CN" %}查看环境要求、实验步骤、提交方式和验收标准。{% else %}Find setup instructions, tasks, submission details, and acceptance criteria.{% endif %}
:::

:::{grid-item-card} {% if cookiecutter.language == "zh_CN" %}课程作业{% else %}Assignments{% endif %}
:link: assignments/index
:link-type: doc

{% if cookiecutter.language == "zh_CN" %}查看作业要求、截止时间和公开评分标准。{% else %}Review requirements, due dates, and published rubrics.{% endif %}
:::

:::{grid-item-card} {% if cookiecutter.language == "zh_CN" %}课程资源{% else %}Resources{% endif %}
:link: resources/index
:link-type: doc

{% if cookiecutter.language == "zh_CN" %}获取教材、开发工具、数据与延伸阅读。{% else %}Find textbooks, tools, datasets, and further reading.{% endif %}
:::
::::

```{toctree}
:hidden:
:maxdepth: 2

lectures/index
labs/index
assignments/index
resources/index
```
