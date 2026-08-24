---
title: "{% if cookiecutter.language == "zh_CN" %}课程讲义{% else %}Lectures{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}讲义, 导航{% else %}lectures, navigation{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}课程讲义{% else %}Lectures{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

{% if cookiecutter.language == "zh_CN" %}讲义按授课顺序排列。复制示例页并在下方 toctree 中加入新 docname。{% else %}Lectures follow the teaching schedule. Copy the sample page and add its docname to the toctree below.{% endif %}

```{toctree}
:maxdepth: 1

lesson-01-introduction
```
