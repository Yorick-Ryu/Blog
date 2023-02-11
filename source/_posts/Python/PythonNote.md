---
title: Python笔记
index_img: img/img1.png
categories: 
  - Python
date: 2022-04-18 16:13:49
tags: 
  - note
sticky: 
---

### Python_Mini_Note

1. import random 随机数库
2. import decimal 十进制库，提供精准的浮点数
3. `//`地板除,两数相除后向下取整的结果
4. 一个公式：`x == (x // y) * y+(x % y)`
5. `divmod(a,b)` 得到 `(a // b,a % b)`
6. `ads(x)`返回x的绝对值，若x是复数，则返回x的模
7. `pow(x,y)`和`x ** y`都表示x的y次方 
8. `pow(x,y,z)`表示x的y次方除以z的余数
9. 流程图

    ![流程图](img/img1.png)
10. for in 
11. 深拷贝和浅拷贝 `import copy`
12. 列表推导式
13. 元组不可以修改，只支持查
14. 打包和解包
    ```py
    t = (123,222,"hh")
    x,y,z = t
    a,b,c,d,e,f = 'Yorick'
    a,b,c,*d = 'Yorick'
    ```
15. 多重赋值`x,y = 1,2`

16. 元组里放列表就可变

17. `zip(x,y,z)`以最短的为准,可以`import itertools` 使用`itertools.zip_longest(x,y,z)`可以按照最长的来，空用`None`填充

18. map()
     ```py
    mapped = map(pow,[1,2,3],[2,3,4])
    #等价：
    mapped = [pow(1,2),pow(2,3),pow(3,4)]
     ```

19. filter()
    ```py
    list(filter(str.islower,"Yorick"))
    #返回orick
    ```
20. set 集合元素具有唯一性
    ```py
    set([1,1,2,3,5,3])
    #输出去重集合
    {1, 2, 3, 5}
    ```
21. 参数列表里`/`左边只能传递位置参数，不能传递关键字参数。
    ```py
    def abc(a,/,b,c):
	    print(a,b,c)
    abc(1,2,3)
    #正常输出 1 2 3
    abc(a = 1,2,3)
    #报错SyntaxError: positional argument follows keyword argument
    ```
22. `*`限制参数列表,`*`号右侧只能为关键字参数,左侧不限
    ```py
    def abc(a,*,b,c):
	    print(a,b,c)
    ```
23. 收集参数，利用元组（tuple）的打包解包功能实现动态参数
    ```py
    def myfunc(*args):
        print("有{}个参数".format(len(args)))
        print("第二个参数是：{}".format(args[1]))
    myfunc(1,2,3)
    # 输出：
    # 有3个参数
    # 第二个参数是：2
    ```
    当某函数的参数列表中存在收集参数时，收集参数右侧只能为关键字参数,左侧不限。（同22）
24. `**`字典形式的收集参数
    ```py
    def myfunc(a,*b,**c):
        print(a,b,c)
    myfunc(1,2,3,4,x=5,y=6)
    # 输出：
    # 1 (2, 3, 4) {'x': 5, 'y': 6}
    ```
    常见于`format`函数：
    ```py
    help(str.format)
    Help on method_descriptor:
    
    format(...)
        S.format(*args, **kwargs) -> str
    
        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
    ```
25. 解包参数
    调用时解包元组`*`，解包字典`**`。
    ```py
    #定义一个元组
    arg = (1,2,3,4)
    #定义一函数，需要4个参数
    def myfunc(a,b,c,d):
        print(a,b,c,d)
    #第一个报错
    myfunc(arg)
    #第二个正常输出1 2 3 4，解包了
    myfunc(*arg)
    ```
26. 全局变量无法在函数中改变，只能访问。
    如果非要改，用`global`关键字，但不提倡
    ```py
    x = 880
    def myfunc():
        global x
        x = 520
        print(x)
    
    myfunc()
    #输出520
    print(x)
    #输出520，全局变量x被改变
    ````
27. `nonlocal`实现在内部函数改变外部函数的变量

28. 变量作用域遵循LEGB规则，优先级由高到低
    `Local`局部作用域
    `Enclosed`嵌套函数的外层作用域
    `Global`全局作用域
    `Built-In`内置作用域

29. 闭包，工厂函数
    1. 利用嵌套函数的外层作用域具有记忆能力这个特性。
    2. 将内层函数作为返回值给返回



30. 返回值是一个函数时不用加`()`

31. 装饰器,不改变原函数的前提下加功能

    注意：
    - **多个装饰器**调用顺序：**自下往上**
    - 可以通过再套一层函数的方式来传递参数

    实现原理：
    ```py
    import time

    def time_master(func):
        def call_func():
	        print("Starting...")
	        start = time.time()
	        func()
	        stop = time.time()
	        print("ending...")
	        print(f"time:{(stop-start):.2f}秒")
        return call_func

    #原函数
    def myfunc():
        time.sleep(2)
        print("Hello Yorick")

    #闭包覆盖原函数
    myfunc = time_master(myfunc)

    #调用
    myfunc()

    #输出：
    #Starting...
    #Hello Yorick
    #ending...
    #time:2.00秒
    ```
    语法糖：
    ```py
    import time

    def time_master(func):
        def call_func():
	        print("Starting...")
	        start = time.time()
	        func()
	        stop = time.time()
	        print("ending...")
	        print(f"time:{(stop-start):.2f}秒")
        return call_func

    #语法糖，以后再调用myfunc，则将此函数作参数代入至time_master函数中运行time_master
    @time_master

    #原函数
    def myfunc():
        time.sleep(2)
        print("Hello Yorick")

    #调用
    myfunc()

    #输出：
    #Starting...
    #Hello Yorick
    #ending...
    #time:2.00秒
    ```

32. lambda函数，匿名函数，一行流
    ```py
    y = [lambda x : x * x,2,3]
    y[0](y[1])
    #结果：4
    ```

33. 生成器：每次调用提供一份数据，并保留函数内部状态，下次调用重复以上过程
    ```py
    def counter():
        i = 0
        while i <= 5:
            yield i
            #yield i与函数中的return i类似，返回上层程序并给出返回值。
            #但是函数在return后不保存当前状态，生成器则是一个迭代器，每次引用时从上一次的结束状态开始运行。
            i += 1
    
    for i in counter():
        print(i)
    
    """
    输出：
    0
    1
    2
    3
    4
    5
    """
    
    #也可以用next()语句，不支持下表索引
    ```
    斐波那契数列:
    ```py
    #斐波那契数列生成器函数
    def fib():
	    back1,back2 = 0,1
	    while True:
		    yield back1
		    back1, back2 = back2, back1+back2
    
    f = fib()
    
    #下一个斐波那契数
    next(f)
    
    #打印斐波那契数列
    for i in f:
        print(i)
    ```
34. 生成器表达式和列表表达式：生成器表达式每次调用只输出一个数据，而列表表达式一次调用全部输出为列表形式。
    ```py
    #生成器表式
    g = (i ** 2 for i in range(10))
    next(g)
    #输出0
    for i in g:
        print()
    #依次输出16 25 36 49 64 91 
    
    #列表表达式
    [i ** 2 for i in range(10)]
    #输出：[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    ```


​    

