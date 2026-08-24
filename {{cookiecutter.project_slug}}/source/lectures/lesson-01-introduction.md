---
title: "{% if cookiecutter.language == "zh_CN" %}第 1 讲：课程导论{% else %}Lecture 1: Introduction{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}讲义, 导论{% else %}lecture, introduction{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}第 1 讲：课程导论{% else %}Lecture 1: Introduction{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

## {% if cookiecutter.language == "zh_CN" %}学习目标{% else %}Learning objectives{% endif %}

{% if cookiecutter.language == "zh_CN" -%}
完成本讲后，学生应能够：

- 说明本课程要解决的核心问题；
- 了解课程进度、考核方式与协作规范；
- 完成本地学习环境的准备。

## 课前准备

在这里列出阅读材料、软件和预备知识。

## 本讲内容

用课程的第一讲替换这一节。公式、代码块、提示框和图表均可使用 MyST 语法编写。
{% else -%}
After this lecture, students should be able to:

- explain the central problems addressed by the course;
- understand the schedule, assessment, and collaboration rules;
- prepare their local learning environment.

## Preparation

List readings, software, and prerequisites here.

## Topics

Replace this section with the first lecture. MyST supports equations, code blocks, admonitions, and figures.
{% endif %}
