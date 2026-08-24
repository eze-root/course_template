---
title: "{% if cookiecutter.language == "zh_CN" %}课程资源{% else %}Resources{% endif %}"
date: {{ cookiecutter.course_start_date }}
author: {{ cookiecutter.author_name | tojson }}
tags: [{% if cookiecutter.language == "zh_CN" %}资源{% else %}resources{% endif %}]
---

# {% if cookiecutter.language == "zh_CN" %}课程资源{% else %}Resources{% endif %}

```{article-info}
:avatar-outline: muted
:author: {{ cookiecutter.author_name }} updated on
:date: {{ cookiecutter.course_start_date }}
:class-container: sd-p-2 sd-outline-muted sd-rounded-1
```

## {% if cookiecutter.language == "zh_CN" %}教材与阅读{% else %}Textbooks and reading{% endif %}

- {% if cookiecutter.language == "zh_CN" %}在此添加教材、论文或公开课程链接。{% else %}Add textbooks, papers, or open course links here.{% endif %}

## {% if cookiecutter.language == "zh_CN" %}软件与环境{% else %}Software and environment{% endif %}

- {% if cookiecutter.language == "zh_CN" %}在此记录学生需要使用的稳定工具与安装入口。{% else %}Document stable tools and installation entry points here.{% endif %}

## {% if cookiecutter.language == "zh_CN" %}课程文件{% else %}Course files{% endif %}

{% if cookiecutter.language == "zh_CN" %}附件放入 `source/_static/files/` 后，可通过 `/_static/files/<文件名>` 链接。{% else %}Place downloads in `source/_static/files/` and link them as `/_static/files/<filename>`.{% endif %}
