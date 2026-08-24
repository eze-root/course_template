---
title: "{% if cookiecutter.language == "zh_CN" %}作业 1：入门练习{% else %}Assignment 1: Getting started{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}作业{% else %}assignment{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}作业 1：入门练习{% else %}Assignment 1: Getting started{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

## {% if cookiecutter.language == "zh_CN" %}要求{% else %}Requirements{% endif %}

{% if cookiecutter.language == "zh_CN" %}在此描述作业任务以及允许使用的资料与工具。{% else %}Describe the assignment and the resources and tools students may use.{% endif %}

## {% if cookiecutter.language == "zh_CN" %}提交{% else %}Submission{% endif %}

- {% if cookiecutter.language == "zh_CN" %}截止时间：待公布{% else %}Deadline: To be announced{% endif %}
- {% if cookiecutter.language == "zh_CN" %}提交方式：待公布{% else %}Method: To be announced{% endif %}

## {% if cookiecutter.language == "zh_CN" %}评分标准{% else %}Rubric{% endif %}

| {% if cookiecutter.language == "zh_CN" %}项目{% else %}Criterion{% endif %} | {% if cookiecutter.language == "zh_CN" %}分值{% else %}Points{% endif %} |
| --- | ---: |
| {% if cookiecutter.language == "zh_CN" %}正确性{% else %}Correctness{% endif %} | 60 |
| {% if cookiecutter.language == "zh_CN" %}可读性与说明{% else %}Clarity and documentation{% endif %} | 20 |
| {% if cookiecutter.language == "zh_CN" %}可复现性{% else %}Reproducibility{% endif %} | 20 |
