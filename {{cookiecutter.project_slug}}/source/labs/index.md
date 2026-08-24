---
title: "{% if cookiecutter.language == "zh_CN" %}课程实验{% else %}Labs{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}实验, 导航{% else %}labs, navigation{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}课程实验{% else %}Labs{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

{% if cookiecutter.language == "zh_CN" %}每份实验指导应明确环境、任务、提交物与验收方式。{% else %}Each lab should define its environment, tasks, deliverables, and acceptance criteria.{% endif %}

```{toctree}
:maxdepth: 1

lab-01-setup
```
