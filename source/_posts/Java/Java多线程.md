---
title: Java多线程
index_img: ./img/threadLife.png
categories: 
  - Java
date: 2022-05-15 16:14:47
tags: 
  - Java多线程
  - Thread
sticky: 
---

# Java多线程

- [Java多线程](#java多线程)
  - [程序、进程与多任务](#程序进程与多任务)
  - [线程](#线程)
    - [创建多线程](#创建多线程)
      - [方式一：继承Thread类](#方式一继承thread类)
      - [方式二：实现Runnable接口](#方式二实现runnable接口)
    - [线程的生命周期](#线程的生命周期)
    - [线程调度](#线程调度)
    - [线程同步](#线程同步)
      - [线程安全](#线程安全)
      - [Synchronized关键字](#synchronized关键字)
    - [线程通信](#线程通信)

## 程序、进程与多任务
程序（program）是对数据描述与操作的代码的集合，是应用程序执行的脚本。

进程（process）是程序的一次执行过程，是系统运行程序的基本单位。程序是静态的，进程是动态的。系统运行一个程序即是一个进程从创建运行到消亡的过程。

多任务（multi task）在一个系统中可以同时运行多个程序，即有多个独立运行的任务﹐每个任务对应一个进程。

## 线程
线程（thread）：比进程更小的运行单位，是程序中单个顺序的流控制。一个进程中可以包含多个线程。

简单来讲,线程是一个独立的执行流，是进程内部的一个独立执行单元，相当于一个子程序。

一个进程中的所有线程都在该进程的虚拟地址空间中，**使用该进程的全局变量和系统资源**。

操作系统给每个线程分配不同的CPU时间片,在某一时刻，CPU只执行一个时间片内的线程,多个时间片中的相应线程在CPU内轮流执行。

### 创建多线程

每个Java程序启动后，虚拟机将自动创建一个主线程
可以通过以下两种方式自定义线程类：
- 创建`java.lang.Thread`类的子类，重写该类的run方法
- 创建`java.lang.Runnable`接口的实现类，实现接口中的run方法

#### 方式一：继承Thread类

实例：
```java
class FirstThread extends Thread {
    /**
     * 线程体在 run()方法中
     */
    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        for (int i = 0; i < 100; i++) {
            System.out.println(threadName + " : " + i);
        }
    }
}
```
在主线程里调用 FirstThread
```java
public static void main(String[] args) {
    // 1. 创建线程对象
    Thread thread = new FirstThread();
    // 2. 调用线程的 start() 方法启动线程
    thread.start();
    //主线程main
    String threadName = Thread.currentThread().getName();
    for (int i = 0; i < 100; i++) {
        System.out.println(threadName + " : " + i);
    }
}
```
部分输出：
```java
main : 63
main : 64
main : 65
Thread-0 : 18
main : 66
Thread-0 : 19
main : 67
Thread-0 : 20
main : 68
Thread-0 : 21
Thread-0 : 22
Thread-0 : 23
```
发现两个线程交替运行

注意：调用线程的`start()`方法启动线程，而不是`run()`方法

练习：

不考虑线程安全的问题，使用 Thread 类,创建两个线程，共同打印1-100
```java
public class PrintNumber {
    public static void main(String[] args) {
        int i = 0;
        NumberThread.setI(i);
        Thread thread1 = new NumberThread("Thread_1");
        Thread thread2 = new NumberThread("Thread_2");
        thread1.start();
        thread2.start();
    }
}

class NumberThread extends Thread {
    public NumberThread(String threadName) {
        super(threadName);
    }
    //使用静态属性
    private static int i;

    public static void setI(int i) {
        NumberThread.i = i;
    }

    @Override
    public void run() {
        for (; i < 100; i++) {
            System.out.println(getName() + " : " + i);
        }
    }
}
```
另一种方式：
```java
public class PrintNumber {
    int i = 0;

    public static void main(String[] args) {

        PrintNumber printNumber = new PrintNumber();
        //两个线程对同一个对象进行操作
        Thread thread1 = new NumberThread("Thread_1", printNumber);
        Thread thread2 = new NumberThread("Thread_2", printNumber);
        thread1.start();
        thread2.start();
    }
}

class NumberThread extends Thread {
    PrintNumber printNumber;

    public NumberThread(String threadName, PrintNumber printNumber) {
        super(threadName);
        this.printNumber = printNumber;
    }
    
    @Override
    public void run() {
        for (; printNumber.i < 100; printNumber.i++) {
            System.out.println(getName() + " : " + printNumber.i);
        }
    }
}
```
部分输出：
```java
Thread_1 : 0
Thread_2 : 0
Thread_1 : 1
Thread_1 : 3
Thread_1 : 4
Thread_1 : 5
Thread_1 : 6
Thread_1 : 7
Thread_1 : 8
Thread_1 : 9
Thread_1 : 10
Thread_2 : 2
Thread_1 : 11
Thread_2 : 12
Thread_1 : 13
Thread_2 : 14
Thread_2 : 16
Thread_2 : 17
Thread_2 : 18
Thread_2 : 19
Thread_2 : 20
Thread_2 : 21
Thread_2 : 22
Thread_2 : 23
Thread_2 : 24
Thread_2 : 25
Thread_1 : 15
Thread_2 : 26
Thread_1 : 27
Thread_2 : 28
Thread_1 : 29
Thread_2 : 30
Thread_1 : 31
Thread_2 : 32
Thread_1 : 33
```
发现除了存在部分线程安全问题，两个线程同时对 i 实施自增操作的。

#### 方式二：实现Runnable接口

当需要定义的线程类已经显式继承了一个其他的类，即无法继承Thread类时，我们可以使用Runnable接口来实现多线程

Runnable接口中只有一个未实现的run方法，实现该接口的类必须重写该方法。

Runnable接口和Thread类之间的区别

- Runnable接口必须实现run方法，而Thread类中的run方法是一个空方法，可以不重写
- Runnable接口的实现类并不是真正的线程类，只是线程运行的目标类。要想以线程的方式执行run方法，必须依靠Thread类
- **Runnable接口适合于资源的共享**

实现Runnable接口的方式;
1. 创建实现 Runnable接口的实现类：必须实现`run()`方法
2. 创建 1 中对应的 Runnable接口的实现类对象
3. 使用 `new Thread (Runnable target)` 创建Thread对象
4. 调用 Thread 类`start()`方法启动线程。

实例：用Runnable接口实现上面的练习

```java
//1. 创建实现 Runnable接口的实现类：必须实现 run() 方法
public class MyRunnable implements Runnable {

    int i = 0;

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        for (; i < 100; i++) {
            System.out.println(threadName + " : " + i);
        }
    }

    public static void main(String[] args) {
        //2. 创建 1 中对应的 Runnable接口的实现类对象
        MyRunnable mr = new MyRunnable();
        //3. 使用 `new Thread (Runnable target)` 创建Thread对象，
        Thread thread1 = new Thread(mr);
        Thread thread2 = new Thread(mr);
        //4. 调用 Thread 类`start()`方法启动线程。
        thread1.start();
        thread2.start();
    }
}
```
### 线程的生命周期

线程的生命周期：

- 指线程从创建到启动，直至运行结束
- 可以通过调用Thread类的相关方法影响线程的运行状态

线程的运行状态：

- 新建 (New)
- 可执行 (Runnable)
- 运行 (Running)
- 阻塞（Blocking)
- 死亡 (Dead)

![ThreadLife](./img/threadLife.png)

新建状态(New)
- 当创建了一个Thread对象时，该对象就处于“新建状态”
- 没有启动，因此无法运行
  

可执行状态(Runnable)
- 其他线程调用了处于新建状态线程的start方法，该线程对象将转换到“可执行状态”
- 线程拥有获得CPU控制权的机会，处在等待调度阶段。

运行状态（Running )
- 处在“可执行状态”的线程对象一旦获得了CPU控制权就会转换到“执行状态”
在“执行状态”下,线程状态占用CPU时间片段 , 执行 run 方法中的代码
- 处在“执行状态”下的线程可以调用yield方法,该方法用于主动出让CPU 控制权。线程对象出让控制器后回到“可执行状态”，重新等待调度。
  ```java
  public class YieldThreadTest extends Thread {
  
    public static void main(String[] args) {
  
        Thread t1 = new YieldThreadTest("Thread_1");
        Thread t2 = new YieldThreadTest("Thread_2");
  
        t1.start();
        t2.start();
    }
  
    public YieldThreadTest(String name) {
        super(name);
    }
  
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(getName() + " : " + i);
            if (i%10==0){
                yield();
            }
        }
    }
  }
  ```
  阻塞状态(Blocking)
- 线程在“执行状态”下由于受某种条件的影响会被迫出让CPU控制权，进入“阻塞状态”。

进入阻塞状态的三种情况
- 调用`sleep`方法
  - Thread类的sleep方法用于让当前线程暂时休眠一段时间
  - 参数 millis 的单位是毫秒
  ```java
  public class SleepThreadTest extends Thread {
    public static void main(String[] args) {
        new SleepThreadTest().start();
    }
    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(getName() + " : " + i);
        }
    }
  }
  ```
  
- 调用`join`方法（合并某个线程）
  - 处在“执行状态”的线程如果调用了其他线程的`join`方法，将被挂起进入“阻塞状态”
  - 目标线程执行完毕后才会解除阻塞，回到“可执行状态”
  ```java
  public class JoinThreadTest extends Thread {
    public static void main(String[] args) {
        Thread thread = new JoinThreadTest();
        thread.start();
        for (int i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + " : " + i);
            if (i == 10) {
                try {
                    thread.join();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }
  
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(getName() + " : " + i);
        }
    }
  }
  ```

- 执行IO操作
  - 线程在执行过程中如果因为访问外部资源（等待用户键盘输入、访问网络）时发生了阻塞，也会导致当前线程进入“阻塞状态"。

解除阻塞
- 睡眠状态超时
- 调用`join`后等待其他线程执行完毕
- I/O操作执行完毕
- 调用阻塞线程的`interrupt`方法（线程睡眠时，调用该线程的`interrupt`方法会抛出`InterruptedException`）
  ```java
  public class InterruptThreadTest extends Thread {
    public static void main(String[] args) {
        InterruptThreadTest itt = new InterruptThreadTest();
        itt.start();
        itt.interrupt();
    }
  
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(getName() + " : " + i);
            if (i == 10) {
                try {
                    Thread.sleep(100000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }
  }
  ```
  死亡状态(Dead)

- 处于“执行状态”的线程一旦从`run`方法返回(无论是正常退出还是抛出异常)就会进入“死亡状态”。
- 已经“死亡”的线程不能重新运行，否则会抛出`IllegalThreadStateException`
- 可以使用 Thread类的`isAlive`方法判断线程是否活着
  ```java
  public class IsAliveThreadTest extends Thread {
    public static void main(String[] args) {
        Thread thread = new IsAliveThreadTest();
        System.out.println(thread.isAlive());//false
        thread.start();
        System.out.println(thread.isAlive());//true
        try {
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(thread.isAlive());//false
        //已经结束的线程无法再被执行
        //thread.start();
    }
  
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(getName() + " : " + i);
        }
    }
  }
  ```

### 线程调度

线程调度

- 按照特定机制为线程分配CPU时间片段的行为
- Java程序运行时，由Java虚拟机负责线程的调度
  

线程调度的实现方式
- 分时调度模型：让所有线程轮流获得CPU的控制权，并且为每个线程平均分配CPU时间片段
- 抢占式调度模型：选择优先级相对较高的线程执行，如果所有线程的优先级相同，则随机选择一个线程执行。Java虚拟机采用此种调度模型。

### 线程同步

Java允许多线程并发控制，当多个线程同时操作一个可共享的资源变量时（如数据的增删改查），将会导致数据不准确，相互之间产生冲突，因此加入同步锁以避免在该线程没有完成操作之前，被其他线程的调用，从而保证了该变量的唯一性和准确性。

#### 线程安全
多线程应用程序同时访问共享对象时，由于线程间相互抢占CPU的控制权，造成一个线程夹在另一个线程的执行过程中运行，所以可能导致错误的执行结果。
#### Synchronized关键字
为了防止共享对象在并发访问时出现错误Java中提供了`synchronized`关键字。

`synchronized`关键字
- 确保共享对象在同一时刻只能被一个线程访问，这种处理机制称为“线程同步”或“线程互斥”。Java中的“线程同步"基于“对象锁”的概念。  
  

使用`synchronized`关键字

- 修饰方法
- 修饰代码块
  

注意：

- 同步块的作用与同步方法一样，只是控制范围有所区别

- 使用synchronized 代码块解决线程安全的问题：需要在synchronized 代码块中参照共同的一个对象

实例：两个线程同步打印26个字母
```java
public class PrintLetters implements Runnable {
    private char c = 'a';

    public boolean print() {
        //修饰代码块
        synchronized (this) {
            if (c < +'z') {
                System.out.println(Thread.currentThread().getName() + " : " + c);
                c++;
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                return true;
            }
            return false;
        }
    }

    @Override
    public void run() {
        boolean flag = print();
        while (flag) {
            flag = print();
        }
    }

    public static void main(String[] args) {
        PrintLetters letters = new PrintLetters();
        Thread th1 = new Thread(letters);
        Thread th2 = new Thread(letters);

        th1.setName("线程1");
        th2.setName("线程2");
        th1.start();
        th2.start();
    }
}
```
修饰方法：
```java
public synchronized boolean print() {
    if (c < +'z') {
        System.out.println(Thread.currentThread().getName() + " : " + c);
        c++;
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return true;
    }
    return false;
}
```
### 线程通信

当一个线程正在使用同步方法时，其他线程就不能使用这个同步方法，而有时涉及一些特殊情况：

- 当一个人在一个售票窗口排队买电影票时，如果她给售票员的不是零钱，而售票员有没有售票员找她，那么她必须等待，并允许后面的人买票，以便售票员获取零钱找她，如果第2个人也没有零钱，那么她俩必须同时等待。

当一个线程使用的同步方法中用到某个变量，而此变量又需要其他线程修改后才能符合本线程的需要，那么可以在同步方法中使用`wait()`方法

`wait()`方法：
- 中断方法的执行，使本线程等待，暂时让出cpu的使用权，并允许其他线程使用这个同步方法。  

`notify()`方法：
- 唤醒由于使用这个同步方法而处于等待线程的某一个结束等待
  

`notifyall()`方法：  
- 唤醒所有由于使用这个同步方法而处于等待的线程结束等待
实例：刘关张买票，票价五元一张，售票员只有五元零钱，张飞有二十元整钱，刘关各有五元
```java
public class TicketHouse implements Runnable {

    private int fiveCount = 1, tenCount = 0, twentyCount = 0;

    public synchronized void buy() {

        String name = Thread.currentThread().getName();

        if ("zf".equals(name)) {
            if (fiveCount < 3) {
                try {
                    System.out.println("五元面值 " + fiveCount + " 张，张飞必须等待");
                    wait();
                    System.out.println("五元面值 " + fiveCount + " 张，卖一张票给张飞，找零 15");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } else if ("gy".equals(name)) {
            fiveCount++;
            System.out.println("卖一张票给关羽，钱正好，" + "五元面值 " + fiveCount + " 张");
        } else if ("lb".equals(name)) {
            fiveCount++;
            System.out.println("卖一张票给刘备，钱正好，" + "五元面值 " + fiveCount + " 张");
        }
        //唤醒
        if (fiveCount == 3)
            notifyAll();
    }

    @Override
    public void run() {
        buy();
    }

    public static void main(String[] args) {
        Runnable runnable = new TicketHouse();
        Thread th1 = new Thread(runnable);
        th1.setName("zf");
        Thread th2 = new Thread(runnable);
        th2.setName("gy");
        Thread th3 = new Thread(runnable);
        th3.setName("lb");
        th1.start();
        th2.start();
        th3.start();
    }
}
``