---
title: Hexo_Fluid_Tag插件的使用
tags:
  - Hexo
  - Fluid
index_img: /img/default.png
categories:
  - Environment
date: 2022-12-16 14:44:37
sticky:
---

# Hexo Fluid Tag插件的使用

[配置指南 | Hexo Fluid 用户手册 (fluid-dev.com)](https://hexo.fluid-dev.com/docs/guide/#tag-插件)

### Tag 插件

#### [#](https://hexo.fluid-dev.com/docs/guide/#便签)便签

在 markdown 中加入如下的代码来使用便签：

```markdown
{% note success %}
文字 或者 `markdown` 均可
{% endnote %}
```

或者使用 HTML 形式：

```html
<p class="note note-primary">标签</p>
```

可选便签：

<p class="note note-primary">primary</p>

<p class="note note-secondary">secondary</p>

<p class="note note-success">success</p>

<p class="note note-danger">danger</p>

<p class="note note-warning">warning</p>

<p class="note note-info">info</p>

<p class="note note-light">light</p>

```
WARNING
使用时 `{% note primary %}` 和 `{% endnote %}` 需单独一行，否则会出现问题
```

#### [#](https://hexo.fluid-dev.com/docs/guide/#行内标签)行内标签

在 markdown 中加入如下的代码来使用 Label：

```markdown
{% label primary @text %}
```

或者使用 HTML 形式：

```html
<span class="label label-primary">Label</span>
```

可选 Label：

<span class="label label-primary">primary</span>
<span class="label label-default">default</span>
<span class="label label-info">info</span>
<span class="label label-success">success</span>
<span class="label label-warning">warning</span>
<span class="label label-danger">danger</span>

```
WARNING
若使用 `{% label primary @text %}`，text 不能以 @ 开头
```

#### [#](https://hexo.fluid-dev.com/docs/guide/#勾选框)勾选框

在 markdown 中加入如下的代码来使用 Checkbox：

```markdown
{% cb text, checked?, incline? %}
```

- text：显示的文字
- checked：默认是否已勾选，默认 false
- incline: 是否内联（可以理解为后面的文字是否换行），默认 false

示例：

{% cb 普通示例 %}

{% cb 默认选中, true %}

{% cb 内联示例, false, true %} 后面文字不换行  

{% cb false %} 也可以只传入一个参数，文字写在后边（这样不支持外联）



#### [#](https://hexo.fluid-dev.com/docs/guide/#按钮)按钮

你可以在 markdown 中加入如下的代码来使用 Button：

```markdown
{% btn url, text, title %}
```

或者使用 HTML 形式：

```html
<a class="btn" href="url" title="title">text</a>
```

- url：跳转链接
- text：显示的文字
- title：鼠标悬停时显示的文字（可选）

<a class="btn" href="yorick.love" title="title">Button</a>
