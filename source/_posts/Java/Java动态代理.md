---
title: Java动态代理
index_img: /img/default.png
categories: 
  - Java
date: 2022-05-14 13:56:19
tags: 
  - 动态代理
sticky: 
---

# 动态代理
## 使用动态代理实现AOP
AOP(Aspect Orient Program，面向切面编程)

代理设计模式的原理：

使用一个代理将对象包装起来，然后用该代理对象取代原始对象，任何对原始对象的调用都要通过代理，代理对象决定是否以及何时将方法调用转到原始对象上。

实例：

定义接口 ArithmeticCalculator
```java
public interface ArithmeticCalculator {
    int add(int i, int j);

    int sub(int i, int j);

    void mul(int i, int j);

    void div(int i, int j);
}
```
实现接口
```java
public class ArithmeticCalculatorImpl implements ArithmeticCalculator {
    @Override
    public int add(int i, int j) {
        return i + j;
    }

    @Override
    public int sub(int i, int j) {
        return i - j;
    }

    @Override
    public void mul(int i, int j) {
        System.out.println(i * j);
    }

    @Override
    public void div(int i, int j) {
        System.out.println(i / j);
    }
}
```
用代理包装对象
```java
@Test
public void testProxy() {
    ArithmeticCalculator arithmeticCalculator = new ArithmeticCalculatorImpl();
    /**
     * ClassLoader loader:
     * 由动态代理产生的对象由哪个类加载器来加载.
     * 通常情况下和被代理对象使用一样的类加载器
     * @NotNull Class<?>[] interfaces:
     * 由动态代理产生的对象必须实现的接口的 Class 数组
     * @NotNull reflect.InvocationHandler h
     * 当具体调用代理对象的方法时,将产生什么行为
     */
    final ArithmeticCalculator proxyInstance =
            (ArithmeticCalculator) Proxy.newProxyInstance(
                    arithmeticCalculator.getClass().getClassLoader(),
                    new Class[]{ArithmeticCalculator.class},
                    new InvocationHandler() {
                        /**
                         *
                         * @param proxy
                         * @param method: 正在被调用的方法
                         * @param args: 调用方法时传入的参数
                         * @return
                         * @throws Throwable
                         */
                        @Override
                        public Object invoke(Object proxy, 
                                             Method method, 
                                             Object[] args) throws Throwable {
                            System.out.print("计算；" + args[0] + 
                                    method.getName() + args[1] + " = ");
                            Object res = method.invoke(arithmeticCalculator, args);
                            return res;
                        }
                    });
    //测试
    proxyInstance.mul(1, 2);
    int res = proxyInstance.add(1, 1);
    System.out.println(res);
}
```
 关于动态代理的细节
 1. 需要一个被代理的对象。
 2. 类加载器通常是和被代理对象使用相同的类加载器
 3. 一般地，`Proxy.newProxyInstance()`的返回值是一个被代理对象实现的接口的类型.当然也可以是其他的接口的类型。
 提示:若代理对象不需要额外实现被代理对象实现的接口以外的接口,
 可以使用`target.getClass(().getInterfaces()`
 4. `InvocationHandler` 通常使用匿名内部类的方式，被代理对象需要是 final 类型的。
 5. `InvocationHandler` 的 `invoke()` 方法中的第一个参数 Object 类型的 proxy
 指的是正在被返回的那个代理对象，一般不使用