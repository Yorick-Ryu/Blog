---
title: Android自定义视图
index_img: ./img/image-20221124172128201.png
categories: 
  - Android
date: 2022-12-17 10:57:37
tags: 
  - layout
  - view
sticky: 
---

# 自定义视图

[自定义视图组件  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/guide/topics/ui/custom-components?hl=zh_cn)

[创建视图类  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/training/custom-views/create-view?hl=zh_cn)

## 系统如何绘制View

下图是布局树

![image-20221124172128201](./img/image-20221124172128201.png)

视图的每一次刷新都是完整地遍历布局树的过程，这个过程比较耗时

[Android系统显示原理简介 - 简书 (jianshu.com)](https://www.jianshu.com/p/a978a6250f9e)

![image-20221124185323496](./img/image-20221124185323496.png)

要在`16ms`内画完每一个界面

![image-20221124185524584](./img/image-20221124185524584.png)

```kotlin
class MyView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null, defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {
    // xml加载完毕时调用
    override fun onFinishInflate() {
        super.onFinishInflate()
        Log.d("yu","onFinishInflate：")
    }
	
    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        Log.d("yu", "onAttachedToWindow: ")
    }

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
        Log.d("yu", "onMeasure: ")
    }

    override fun onLayout(changed: Boolean, left: Int, top: Int, right: Int, bottom: Int) {
        super.onLayout(changed, left, top, right, bottom)
        Log.d("yu", "onLayout: ")
    }

    override fun onDraw(canvas: Canvas?) {
        super.onDraw(canvas)
        Log.d("yu", "onDraw: ")
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        Log.d("yu", "onSizeChanged: ")
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        Log.d("yu", "onDetachedFromWindow: ")
    }
}
```

启动输出

```
onFinishInflate：   
onAttachedToWindow:
onMeasure:         
onMeasure:         
onSizeChanged:     
onLayout:          
onDraw:            
```


- **DashPathEffect**：将Path的线段虚线化，intervals为虚线的ON和OFF的数组，数组中元素数目需要 >= 2； 而phase则为绘制时的偏移量。

[Android自定义view之利用PathEffect实现动态效果 - 掘金 (juejin.cn)](https://juejin.cn/post/6999603842845261860)