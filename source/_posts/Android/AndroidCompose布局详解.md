---
title: Compose布局详解
index_img: ./img/image-20221209183304625.png
categories: 
  - Android
date: 2022-12-09 18:29:00
tags: 
  - Jetpack
  - Compose
  - layout
sticky: 
---

# 深入了解 Jetpack Compose 布局

[TOC]

Jetpack Compose 提供一个全新的布局模型，用于构建精美、高效的界面。我们深入介绍了这个布局模型，说明了它的底层工作逻辑，它所具备的功能，捆绑的布局和修饰符是如何构建的，以及可以如何轻松创建自定义布局和修饰符。本次研讨会将有助于了解 Compose 的布局模型，您可以使用这个模型来构建应用所需的布局，并且编写更优质的代码。

内容来自[深入了解 Jetpack Compose 布局 - YouTube](https://youtu.be/zMKMwh9gZuI)

## Compose布局系统的目标

- 简化布局的创建，尤其是自定义布局
- 提供强大的布局系统
- 实现卓越的性能

![image-20221209183304625](./img/image-20221209183304625.png)

**如何实现以上目标？**

## Jetpack Compose 如何将状态转为界面

这个流程包含三个阶段

- 组合
- 布局
- 绘制

![image-20221209183505668](./img/image-20221209183505668.png)

### 组合阶段（Composition）

组合阶段会执行可组合函数，这些函数会创建界面并组建界面树。

例如，执行这个SearchResult可组合函数，就会生成这样一个界面树。

![image-20221209184149125](./img/image-20221209184149125.png)

可组合项包含逻辑和控制流，在不同的状态下产生不同的界面树。

### 布局阶段（Layout）

布局阶段会遍历整个界面树，测量每个界面元素并将它们放置在屏幕上的二维空间。也就是说，每个节点会确定其宽度和高度以及x和y坐标。

### 绘制阶段（Drawing）

绘制阶段会重新遍历界面树并呈现全部元素。

## 布局阶段的深入介绍

布局阶段包含两个环节：

- 测量（Measure）
- 放置（Place）

![image-20221209185018210](./img/image-20221209185018210.png)

大致相当于View中的`onMeasure`和`onLayout`

不过在Compose中，这两个环节是相互交织的，因此我们暂且将它们视作一个布局环节。

界面树中每个节点的布局流程包含三个步骤：

- 先测量全部子项
- 决定自身尺寸
- 放置子项

![image-20221209185722752](./img/image-20221209185722752.png)

具体过程如下：

![image-20221209185904184](./img/image-20221209185904184.png)

这样以来，跟布局在确定了所有子项的尺寸和位置后，就可以确定自己的尺寸和位置（放置指令），然后就可以进入放置环节，系统重新遍历界面树，并执行所有放置指令。

上述过程如何实现？

实际上，每个高级别可组合项都是通过低级别可组合项构造而成的。

![image-20221209190725298](./img/image-20221209190725298.png)

每一个在屏幕上放置元素的可组合项都包含了一个或多个Layout可组合项，这个Layout可组合项是Compose界面的基础构建块。

Layout可组合项发出LayoutNode，在Compose中，界面树或组合是LayoutNode的树。

![image-20221209190949564](./img/image-20221209190949564.png)

下面是`Layout`的源码

参数：

- content - 可组合放置的子项。
- modifier - 应用于布局的修饰符。
- measurePolicy - 定义布局的测量和定位的策略。

```kotlin
@Suppress("ComposableLambdaParameterPosition")
@UiComposable
@Composable inline fun Layout(
    content: @Composable @UiComposable () -> Unit, // The children composable to be laid out
    modifier: Modifier = Modifier, 				   // Modifiers to be applied to the layout
    measurePolicy: MeasurePolicy				   // The policy defining the measurement and positioning of the layout
) {
    val density = LocalDensity.current
    val layoutDirection = LocalLayoutDirection.current
    val viewConfiguration = LocalViewConfiguration.current
    ReusableComposeNode<ComposeUiNode, Applier<Any>>(
        factory = ComposeUiNode.Constructor,
        update = {
            set(measurePolicy, ComposeUiNode.SetMeasurePolicy)
            set(density, ComposeUiNode.SetDensity)
            set(layoutDirection, ComposeUiNode.SetLayoutDirection)
            set(viewConfiguration, ComposeUiNode.SetViewConfiguration)
        },
        skippableUpdate = materializerOf(modifier),
        content = content
    )
}
```

自定义Layout

```kotlin
@Composable
fun MyCustomLayout(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Layout(
        modifier = modifier,
        content = content
    ) {measurables:List<Measurable>,
        constraints:Constraints ->
        // TODO measure and place items
    }
}
```

在本例的MyCustomLayout可组合项中，我们调用Layout函数，并以尾随lambda的形式提供measurePolicy用于实现所需的测量函数，这个函数接受`Constraints`对象，定义布局的大小。

`Constraints`是一个简单的类，用于对布局可以采用的宽度和高度上下限进行建模。

```kotlin
class Constraints {
    val minWidth: Int
    val maxWidth: Int
    val minHeight: Int
    val maxHeight: Int
}
```

例如，`Constrains`可以表达布局可以采用任意尺寸

```kotlin
val bigAsYouLike = class Constraints(
    minWidth = 0,
    maxWidth = Constraints.Infinity,
    minHeight = 0,
    maxHeight = Constraints.Infinity,
)
```

也可以表达布局必须采用确切的尺寸

```kotlin
val bigAsYouLike = class Constraints(
    minWidth = 50,
    maxWidth = 50,
    minHeight = 50,
    maxHeight = 50,
)
```

测量函数还会接收可测量项的列表，此列表表示传入的子项元素，Measurable类型公开用于测量项目的函数。

每个元素的布局流程具体实现：

```kotlin
@Composable
fun MyCustomLayout(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Layout(
        modifier = modifier,
        content = content
    ) {measurables:List<Measurable>,
        constraints:Constraints ->
        // 测量各个子项，产生可放置列表
        val palceables = measurables.map { measurable ->
            // 执行measurable的measure方法，此方法接受尺寸约束条件
            measurable.measure(constraints)
        }
        // 可放置项是经过测量的子项，都有一个尺寸
        // 使用可放置项来计算布局大小
        val width = // 从palceables计算得到
        val height = // 从palceables计算得到
        // 报告尺寸
        layout(width, height){
            // layout方法需要一个放置位置块来放置每个项目
            placeables.forEach{ palceable ->
                placeable.place( // 还有palceRelative方法，针对从右向左的语言区域镜像水平坐标
                    x = ...
                    y = ...
                )
            }
        }
    }
}
```

place方法仅能用于measure方法返回的放置项，这样的API设计可以防止放置没有测量过的元素。在View中，onMeasure和onLayout的调用顺序没有强制性要求，容易产生bug。

示例：实现自定义Colum

```kotlin
@Composable
fun MyColum(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Layout(
        modifier = modifier,
        content = content
    ) { measurables: List<Measurable>,
        constraints: Constraints ->
        // 测量
        val palceables = measurables.map { measurable ->
            measurable.measure(constraints)
        }
        // 计算
        val height = palceables.sumOf { it.height }
        val width = palceables.maxOf { it.width }
        // 放置
        layout(width, height) {
            var y = 0
            palceables.forEach { placeable ->
                placeable.placeRelative(x = 0, y = y)
                y += placeable.height
            }
        }
    }
}
```

示例：

```kotlin
@Composable
fun VerticalGrid(
    modifier: Modifier = Modifier,
    columns:Int = 2,
    content: @Composable () -> Unit
){
    Layout(
        modifier = modifier,
        content = content
    ) { measurables,constraints->
        // 列宽等于布局的最大宽度除以列数
        val itemWidth = constraints.maxWidth / columns
        // 构造新的constraints对象
        val itemConstraints = constraints.copy(
            minWidth = itemWidth,
            maxWidth = itemWidth
        )
        // 使用约束条件测量每个项目
        val palceables = measurables.map { measurable ->
            measurable.measure(itemConstraints)
        }
        // 将项目放入网格
        ...
    }
}
```

这种为子项内容创建新约束条件的理念，就是实现自定义测量逻辑的方式，能够创建不同约束条件来测量子项，这是这个模型的关键。

![image-20221213213747607](./img/image-20221213213747607.png)

最后父项7传递一系列可选的尺寸供子项选择，一旦子项选择了自己的尺寸，父项就必须接受并进行处理。

优点是可以通过单次测量遍历整个界面树，并且禁止多个测量循环（测试多次会报错），这样可以提高性能，例如用动画效果呈现布局。

```kotlin
// try out different constraints
val constraints1 = ...
val constraints2 = ...
val placeable1 = measurable.measure(constraints1)
val placeable2 = measurable.measure(constraints2)
```

什么时候用自定义布局

- 无法用标准布局实现
- 需要精确元素的控制测量和放置
- 实现布局动画
- 需要更高的性能

## Modifier修饰符

Layout函数接受修饰符链作为参数，修饰符修饰自己所关联到的元素，并且在布局自行进行测量和放置之前参与测量和放置。 

如何实现？

有很多影响不同行为的各类修饰符，例如drawing修饰符，pointerInput修饰符和focus修饰符，和我们密切相关的是LayoutModifier。 它提供了measure方法，此方法几乎与Layout组合项完全一样，但是它只作用于单个可测量项，而不是可测量项列表，因为修饰符就是应用于单个项目的 。 

这个示例中，修饰符可像布局一样修改约束条件或实现自定义放置逻辑。这意味着，你并不总是需要编写自定义布局，如果只需要作用于单个项目，就可以改为使用修饰符。

```kotlin
interface LayoutModifier : Modifier.Element {
    
fun MeasureScope.measure(
	measurable: Measurable,
	constraints: Constraints
): MeasureResult
    ...
}
```

例如，我们看看PaddingModifier如何工作。

```kotlin
fun Modifier.padding(all: Dp) = 
	this.then(PaddingModifier(
        start = all,
        top = a1l,
        end = all,
        bottom = all
        )
    )

private class PaddingModifier(
    val start: Dp = 0.dp, 
    val top: Dp = 0.dp,
    val end: Dp = 0.dp,
    val bottom: Dp = 0.dp
) : LayoutModifier {
...
}
```

## 高级布局功能

### 固有测量属性（Intrinsic Measurement）

Compose不总是使用单传递布局系统。例如，下拉列表需要使用固有最大宽度来确定具体尺寸。

```kotlin
Column(Modifier.width(IntrinsicSize.Max)) {
    Text(Modifier.fillMaxWidth())
    Text(Modifier.fillMaxWidth()) 
    Text(Modifier.fillMaxWidth()) 
    Text(Modifier.fillMaxWidth()) 
    Text(Modifier.fillMaxWidth())
}
```

下拉列表的宽度 = 每个文本不换行的情况下的最大宽度

文本的最小固有宽度是每行一个单词的宽度，多了会换行。

### ParentData修饰符

某个布局行为需要从子项获取信息，就需要使用ParentData。

Box中的align就是ParentData修饰符，它向父项传递信息，供父项确定子项布局，如果不在Box中，就无法使用。

基线对齐

![image-20221214113056005](./img/image-20221214113056005.png)

对齐会穿透至子项

![image-20221214113124913](./img/image-20221214113124913.png)

### BoxWithConstraints

这是一个类似Box的可组合项，但是它会将对其内容的组合操作一直延迟到布局环节，那时就有布局信息可用了。

 BoxWithConstraints中的内容在公开约束条件的接收器作用域中运行，这些约束条件是在布局环节以像素或DPI值确定的，因此，里面的内容可以使用这些约束条件来选择要组合的内容。

例如，根据最大宽度选择不同的呈现内容。

```kotlin
@Composable
fun MyApp(...) { 
	BoxWithConstraints() { // this: BoxWithConstraintsScope 
		when {
			maxWidth < 400.dp -> CompactLayout()
			maxWidth < 800.dp -> MediumLayout()
			else -> LargeLayout()
		}
	}
}
```

但是BoxWithConstraints会在布局阶段启动子组合，这会影响性能。除非信息的类型会随着大小一起改变，请尽量避免使用BoxWithConstraints。![image-20221214114817861](./img/image-20221214114817861.png)

## 性能

- 只有在改变显示内容时才需要重组，而改变显示位置或显示方法时则不需要。
- 除非信息的类型会随着大小一起改变，请尽量避免使用BoxWithConstraints。
- 有时无需测量自己的所有子项来确定布局大小
