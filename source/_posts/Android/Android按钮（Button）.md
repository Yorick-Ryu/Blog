---
title: Android按钮（Button）
index_img: /img/default.png
categories:
  - Android
date: 2022-11-29 18:08:23
tags: 
  - view
  - button
  - 控件
sticky:
---

# 按钮(Button)

- [按钮(Button)](#按钮button)
  - [控件属性](#控件属性)
  - [点击和长按事件](#点击和长按事件)
  - [禁用和恢复按钮](#禁用和恢复按钮)

## 控件属性

按钮控件`Button`由`TextView`派生而来，它们之间的区别有：

- `Button`拥有默认的按钮背景，而`TextView`默认无背景;
- `Button`的内部文本默认居中对齐，而`TextView`的内部文本默认靠左对齐；
- `Button`会默认将英文字母转为大写，而`TextView`保持原始的英文大小写。

与`TextView`相比，`Button`增加了两个新属性：

- `textAllCaps`属性，它指定了是否将英文字母转为大写，为`true`是表示自动转为大写，为`false`表示不做大写转换；
- `onClick`属性，它用来接管用户的点击动作，指定了点击按钮时要触发哪个方法。

## 点击和长按事件

监听器，意思是专门监听控件的动作行为。只有控件发生了指定的动作，监听器才会触发开关去执行对应的代码逻辑。

按钮控件有两种常用的监听器：

- 点击监听器，通过`setOnClickListener`方法设置。按钮被按住少于500毫秒时，会触发点击事件。
- 长按监听器，通过`setOnLongClickListener`方法设置。按钮被按住超过500毫秒时，会触发长按事件。

点击事件有多种实现方式：

- 使用匿名内部类的方式适用于按钮少的情况，使用静态内部类可以防止内存泄漏。

  ```java
  btnLongClick.setOnLongClickListener(new View.OnLongClickListener() {
    @Override
    public boolean onLongClick(View v) {
        // 这里放点击实现的代码
        return false; 
        // 返回true表示事件已经被消耗掉，不往上层冒泡；否则向上层冒泡
    }
    });
  ```

  改用`lambda`表达式：

  ```java
  btnLongClick.setOnLongClickListener(v -> {
    //这里放点击实现的代码
    return false; 
    });
  ```

  没有事件甚至可以省略大括号：

  ```java
  btnLongClick.setOnLongClickListener(v -> false);
  ```

- 单独点击事件也适用于按钮少的情况，使用静态内部类可以防止内存泄漏。

- 公共点击事件适用于按钮多的时候，直接使当前`Activity`实现`View.OnClickListener`接口的`onClick`方法。

代码示例：

```java
public class ButtonClickActivity extends AppCompatActivity implements View.OnClickListener {

    private TextView tvResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_button_click);
        tvResult = findViewById(R.id.tv_result);
        Button btnClickSingle = findViewById(R.id.btn_click_single);
        btnClickSingle.setOnClickListener(new MyOnClickListener(tvResult));

        Button btnClickPublic = findViewById(R.id.btn_click_public);
        Button btnClickPublic2 = findViewById(R.id.btn_click_public_2);
        btnClickPublic.setOnClickListener(this);
        btnClickPublic2.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        String desc = String.format("%s 您点击了按钮 %s", DateUtil.getCurrentTime(), ((Button) v).getText());
        switch (v.getId()) {
            case R.id.btn_click_public:
                tvResult.setText(desc);
                break;
            case R.id.btn_click_public_2:
                tvResult.setText(desc);
                break;
        }
    }

    // 写成静态内部类，减少内存泄露
    static class MyOnClickListener implements View.OnClickListener {
        private final TextView tvResult;

        public MyOnClickListener(TextView tvResult) {
            this.tvResult = tvResult;
        }

        @Override
        public void onClick(View v) {
            String desc = String.format("%s 您点击了按钮 %s", DateUtil.getCurrentTime(), ((Button) v).getText());
            tvResult.setText(desc);
        }
    }
}
```

当然，除此之外`button`还有很多事件监听器。如`setOnTouchListener`可以实现双击事件。

[参考](https://blog.csdn.net/zuo_er_lyf/article/details/80068006)

## 禁用和恢复按钮

在实际业务中，按钮通常拥有两种状态，即不可用状态与可用状态，它们在外观和功能上的区别如下：

- 不可用按钮：按钮不允许点击，即使点击也没反应，同时按钮文字为灰色；
- 可用按钮：按钮允许点击，点击按钮会触发点击事件，同时按钮文字为正常的黑色；

是否允许点击由`enabled`属性控制，属性值为`true`时表示允许点击，为`false`时表示不允许点击。

在Java代码中用`setEnabled()`方法控制，属性值为`true`时表示允许点击，为`false`时表示不允许点击。

