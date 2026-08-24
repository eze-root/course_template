---
title: "{% if cookiecutter.language == "zh_CN" %}课程作业{% else %}Assignments{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}作业, 导航{% else %}assignments, navigation{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}课程作业{% else %}Assignments{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

{% if cookiecutter.language == "zh_CN" %}作业页应同时写清目标、提交格式、截止时间、协作边界和评分标准。{% else %}Assignment pages should state objectives, submission format, deadline, collaboration policy, and rubric.{% endif %}

```{toctree}
:maxdepth: 1

assignment-01
```
