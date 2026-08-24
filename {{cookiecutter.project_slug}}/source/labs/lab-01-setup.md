---
title: "{% if cookiecutter.language == "zh_CN" %}实验 1：环境准备{% else %}Lab 1: Environment setup{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}实验, 环境{% else %}lab, setup{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}实验 1：环境准备{% else %}Lab 1: Environment setup{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

## {% if cookiecutter.language == "zh_CN" %}目标{% else %}Objective{% endif %}

{% if cookiecutter.language == "zh_CN" %}安装课程工具链并完成一次最小验证。{% else %}Install the course toolchain and complete a minimal verification.{% endif %}

## {% if cookiecutter.language == "zh_CN" %}任务{% else %}Tasks{% endif %}

1. {% if cookiecutter.language == "zh_CN" %}安装所需软件。{% else %}Install the required software.{% endif %}
2. {% if cookiecutter.language == "zh_CN" %}运行教师提供的验证命令。{% else %}Run the validation command provided by the instructor.{% endif %}
3. {% if cookiecutter.language == "zh_CN" %}按要求提交结果。{% else %}Submit the result as instructed.{% endif %}

## {% if cookiecutter.language == "zh_CN" %}验收标准{% else %}Acceptance criteria{% endif %}

- [ ] {% if cookiecutter.language == "zh_CN" %}命令执行成功。{% else %}The command completes successfully.{% endif %}
- [ ] {% if cookiecutter.language == "zh_CN" %}提交物可复现。{% else %}The deliverable is reproducible.{% endif %}
