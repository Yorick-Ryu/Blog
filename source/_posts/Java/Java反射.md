---
title: Java反射
index_img: ./img/classLoader.png
categories: 
  - Java
date: 2022-05-08 11:02:22
tags: 
  - Java反射
  - reflect
sticky: 
---

# Java反射

- [Java反射](#java反射)
  - [Class](#class)
    - [Class定义](#class定义)
    - [获取Class对象](#获取class对象)
    - [Class类的常用方法](#class类的常用方法)
    - [类加载器](#类加载器)
  - [Method](#method)
    - [获取类的方法](#获取类的方法)
    - [调用类的方法](#调用类的方法)
    - [获取类的父类](#获取类的父类)
    - [获取父类的方法](#获取父类的方法)
  - [Field](#field)
    - [获取Field](#获取field)
    - [获取Field的值](#获取field的值)
    - [设置Field的值](#设置field的值)
  - [Constructor](#constructor)
    - [获取Constructor构造器](#获取constructor构造器)
    - [调用构造器的方法创建对象](#调用构造器的方法创建对象)
  - [Annotation](#annotation)
    - [获取Annotation](#获取annotation)
  - [泛型和反射](#泛型和反射)

## Class

### Class定义

- 关于Class:
  1. class是一个类，是一个描述类的类；
  2. 对象照镜子后可以得到的信息：某个类的数据成员名、方法和构造器、某个类到底实现了哪些接口；
  3. 对于每个类而言，JRE 都为其保留一个不变的Class类型的对象。一个Class对象包含了特定某个类的有关信息。 

- Class对象只能由系统建立对象
- 一个类在JVM中只会有一个Class实例
- 每个类的实例都会记得自己是由哪个Class 实例所生成
### 获取Class对象
获取Class对象的三种方式
```java
@Test
public void testClass() throws ClassNotFoundException {
    Class clazz = null;
    //1.获取Class对象的方式
    //1.1直接通过 类名.class 的方式得到
    clazz = Person.class;
    //1.2通过对象调用 getClass() 方法获取
    Object obj = new Person();
    clazz = obj.getClass();
    //1.3通过全类名的方式获取（最常用）
    String className = "com.yur.java.Person";
    clazz = Class.forName(className);
    //Field[] fields= clazz.getDeclaredFields();//字段集合
    System.out.println();
}
```
### Class类的常用方法

`getConstructor()`返回指定参数类型public的构造器。
`getDeclaredConstructor()`返回指定参数类型的private和public构造器。但在使用private的构造器时，必须设置`setAccessible()`为true,才可以获取并操作该Constructor对象。

实例：
```java
package com.yur.java;

public class Person {
    private String name;
    private int age;

    //供反射使用
    public Person() {
        System.out.println("无参数的构造器");
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
        System.out.println("有参数的构造器");
    }

    public Person(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }

    public void sayHello(){
        System.out.println("Hello"+name);
    }
}
```
测试：
```java
@Test
public void testNewInstance() throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
    String className =   "com.yur.java.Person";
    Class clazz = Class.forName(className);
    //利用Class对象的getConstructor()方法来调用类的无参构造器
    Constructor constructor = clazz.getConstructor();
    //使用该无参构造构造实例
    Object obj = constructor.newInstance();
}
@Test
public void testNewInstance1() throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
    String className =   "com.yur.java.Person";
    Class clazz = Class.forName(className);
    //利用Class对象的getDeclaredConstructor()方法来调用类的无参私有构造器
    Constructor constructor = clazz.getDeclaredConstructor();
    constructor.setAccessible(true);
    Object obj = constructor.newInstance();
}
@Test
public void testNewInstance2() throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
    String className =   "com.yur.java.Person";
    Class clazz = Class.forName(className);
    //利用Class对象的getDeclaredConstructor()方法来调用类的有参构造器
    Constructor constructor = clazz.getDeclaredConstructor(String.class);
    //使用该够惨凄创建实例对象
    Object obj = constructor.newInstance("Yorick");
}
```
### 类加载器

ClassLoader
类装载器是用来把类(class)装载进JVM的。
JVM规范定义了两种类型的类装载器：启动类装载器(bootstrap)和用户自定义装载器(user-defined class loader)。JVM在运行时会产生3个类加载器组成的初始化加载器层次结构，如下图所示：

![classLoader](./img/classLoader.png)

实例：

```java
@Test
public void testClassLoader() throws ClassNotFoundException, FileNotFoundException {
    //1.获取一个系统的类加载器
    ClassLoader classLoader = ClassLoader.getSystemClassLoader();
    System.out.println(classLoader);
    //2.获取系统类加载器的父类加载器
    classLoader = classLoader.getParent();
    System.out.println(classLoader);
    //3.获取扩展类加载器的父类加载器.
    classLoader = classLoader.getParent();
    System.out.println(classLoader);
    //4.测试当前类由哪个类加载器加载
    classLoader = Class.forName("com.yur.java.Person").getClassLoader();
    System.out.println(classLoader);
    //5.测试JDK 提供的Object 类由哪个类加载器负责加载
    classLoader = Class.forName("java.lang.Object").getClassLoader();
    System.out.println(classLoader);
    //6.关于类加载器的主要方法（重要）
    //调用getResourceAsStream获取类路径下的文件对应的输入流·
    //InputStream in = new FileInputStream("test.properties");
    InputStream in = null;
    in = this.getClass().getClassLoader().getResourceAsStream("test.properties");
    System.out.println(in);
}
```
## Method

Method: 对应类中的方法。

### 获取类的方法

- 获取类的方法的数组:
 `clazz.getDeclaredMethods();`
- 获取类的指定的方法:
 `getDeclaredMethod(String name, class<?>... parameterTypes)`
   name：方法名
   parameterTypes：方法的参数类型(使用Class来描述)的列表
    ```java
    Method method = clazz.getDeclaredMethod("setName", String.class);
    method = clazz.getDeclaredMethod("setName", String.class, int.class);
    ```

### 调用类的方法

通过method对象执行方法：
`public Object invoke(object obj, Object... args)`
obj：执行哪个对象的方法；
args：执行方法时需要传入的参数。

如果方法是 private 修饰的，需要先调用 Method 的 setAccessible(true)，使其变为可访间


实例：获取类的方法并执行
```java
@Test
public void testMethod() throws Exception {
    Class clazz = Class.forName("com.yur.java.Person");
    //1.得到clazz对应的类中有哪些方法（无法获取私有方法）
    Method[] methods = clazz.getMethods();
    for (Method method : methods) {
        System.out.println("-" + method.getName());
    }
    //2.获取所有的方法，包括private方法，且只获取当前类声明的方法
    Method[] methods1 = clazz.getDeclaredMethods();
    for (Method method : methods1) {
        System.out.println("~" + method.getName());
    }
    //3.获取指定的方法
    Method method = clazz.getDeclaredMethod("setName", String.class);
    System.out.println(method);
    method = clazz.getDeclaredMethod("sayHello");
    System.out.println(method);
    method = clazz.getDeclaredMethod("setName", String.class, int.class);
    System.out.println(method);
    //4.执行方法
    Object obj = clazz.getConstructor().newInstance();
    method.invoke(obj, "Yorick", 22);
}
```

### 获取类的父类

获取当前类的父类，直接调用Class对象的`getSuperclass()`方法。
```java
@Test
public void testGetSuperClass() throws  Exception {
    String className = "com.yur.java.Student";
    Class clazz = Class.forName(className);
    Class superClazz = clazz.getSuperclass();
    System.out.println(superClazz);
    //class com.yur.java.Person
}
```
### 获取父类的方法
实例：可以获取自身或父类的方法（包括私有方法）
```java
/**
 * @param className:  某个类的全类名
 * @param methodName: 类的一个方法的方法名。（包括私有方法或者父类方法）
 * @param args:       调用该方法
 * @throws Exception
 * @return: 调用方法后的返回值
 * 该方法实际调用了下面的方法
 */
public Object invoke2(String className, String methodName, Object... args) throws Exception {
    Class[] parameterTypes = new Class[args.length];
    for (int i = 0; i < args.length; i++) {
        parameterTypes[i] = args[i].getClass();
        System.out.println(parameterTypes[i]);
    }
    Class clazz = Class.forName(className);
    Method method = null;
    Object obj = null;
    for (; clazz != Object.class; clazz = clazz.getSuperclass()) {
        try {
            method = clazz.getDeclaredMethod(methodName, parameterTypes);
            method.setAccessible(true);
            obj = clazz.getConstructor().newInstance();
        } catch (Exception e) {}
    }
    return method.invoke(obj, args);
}
```
测试：
```java
@Test
public void testInvoke2() throws Exception {
    //Student类的method1方法被调用,打印"private void method1 " + age
    invoke1("com.yur.java.Student", "method1", 10);
    //Student 类的父类的method2()方法被调用，返回值为"private String method2"
    Object result = invoke2("com.yur.java.Student", "method2");
    System.out.println(result);
}
```

练习：将通过反射读取并调用类的方法封装为一个工具类

Code1：接收全类名，使用`getMethod()`可读取父级方法,但是无法获取私有方法
```java
/**
 * @param className:  某个类的全类名
 * @param methodName: 类的一个方法的方法名。（包括父级方法）
 * @param args:       调用该方法
 * @throws Exception
 * @return: 调用方法后的返回值
 */
public Object invoke(String className, String methodName, Object... args) throws Exception {
    Class[] parameterTypes = new Class[args.length];
    for (int i = 0; i < args.length; i++) {
        parameterTypes[i] = args[i].getClass();
        System.out.println(parameterTypes[i]);
    }
    Class clazz = Class.forName(className);
    Method method = clazz.getMethod(methodName, parameterTypes);
    Object obj = clazz.getConstructor().newInstance();
    return method.invoke(obj, args);
}
```
Code2：接收全类名，由类名新建一个类的对象，再调用Code3的方法
```java
/**
 * @param className:  某个类的全类名
 * @param methodName: 类的一个方法的方法名。（包括私有方法）
 * @param args:       调用该方法
 * @throws Exception
 * @return: 调用方法后的返回值
 * 该方法实际调用了下面的方法
 */
public Object invoke1(String className, String methodName, Object... args) throws Exception {
   Object obj = null;
   obj = Class.forName(className).getConstructor().newInstance();
   invoke(obj,methodName,args);
   return null;
}
```
Code3：接收对象，使用`getDeclaredMethod()`获取方法，可获取私有方法，但是不能获取父类方法
```java
/**
 * @param obj:        方法执行的那个对象.
 * @param methodName: 类的一个方法的方法名。该方法也可能是私有方法·
 * @param args:       调用该方法
 * @throws Exception
 * @return: 调用方法后的返回值
 */
public Object invoke(Object obj, String methodName, Object... args) throws Exception {
    Class[] parameterTypes = new Class[args.length];
    for (int i = 0; i < args.length; i++) {
        parameterTypes[i] = args[i].getClass();
        System.out.println(parameterTypes[i]);
    }
    Class clazz = obj.getClass();
    Method method = clazz.getDeclaredMethod(methodName, parameterTypes);
    Object obj1 = clazz.getConstructor().newInstance();
    return method.invoke(obj1, args);
}
```
测试Code3：
```java
@Test
public void testInvoke() throws Exception {
    Object obj = new Person();
    invoke(obj, "setName", "Yorick", 1);
}
```
测试Code1和Code2：
```java
@Test
public void testInvoke1() throws Exception {
    invoke("com.yur.java.Person","setName", "Yorick", 10);
    invoke1("com.yur.java.Person","setName", "Yorick", 20);
    Object obj = invoke("java.text.SimpleDateFormat","format",new Date());
    System.out.println(obj);
}
```
## Field
字段
### 获取Field
- 获取 Field 的数组
`clazz.getDeclaredFields()`
- 获取指定名字的 Field
`clazz.getDeclaredField(String fieldName);`
### 获取Field的值
- 若该字段是私有的，需要调用
  `setAccessible(true`)
- 获取对象所对应的字段值
  `field.get(Object obj)`
### 设置Field的值
- 设置指定对象的Field的值
`field.set(Object obj, Object value);`
```java
/**
 * Filed:封装了字段的信息
 */
@Test
public void testField() throws Exception {
    String className = "com.yur.java.Person";
    Class clazz = Class.forName(className);
    //1.获取字段
    //1.1获取 Field 的数组
    Field fields[] = clazz.getDeclaredFields();
    for (Field field : fields) {
        System.out.println(field.getName());
    }
    //1.2获取指定名字的Field
    Field field = clazz.getDeclaredField("name");
    System.out.println(field.getName());
    Person person = new Person("ABC",12);
    //2.获取指定对象的指定Field的值
    //若该字段是私有的，需要调用setAccessible(true)方法
    field.setAccessible(true);
    Object val = field.get(person);
    System.out.println(val);
    //3.设置指定对象的Field的值
    field.set(person,"Yorick");
    System.out.println(person.getName());
}
```
工具方法：
```java
@Test
public void testClassField() throws Exception {
    String className = "com.yur.java.Student";
    String fieldName = "age";//可能为私有，可能再其父类中
    Object val = 20;
    Object obj = null;
    Field field = null;
    Class clazz = Class.forName(className);
    field = getField(fieldName, field, clazz);
    clazz = Class.forName(className);
    obj = clazz.getConstructor().newInstance();
    field.setAccessible(true);
    field.set(obj, val);
    Student stu = (Student) obj;
    System.out.println(stu.getAge());//20
}
private Field getField(String fieldName, Field field, Class clazz) {
    for (; clazz != Object.class; clazz = clazz.getSuperclass()) {
        try {
            field = clazz.getDeclaredField(fieldName);
        } catch (Exception e) {
        }
    }
    return field;
}
```
## Constructor
构造器
### 获取Constructor构造器
- 获取全部Constructor对象
`getConstructors()`
- 获取某一个指定的Constructor对象
`getConstructor(class<?>... parameterTypes)`
### 调用构造器的方法创建对象
`Object obj = constructor.newInstance("Yorick", 21);`

实例：
```java
/**
 * Constructor：构造器
 * @throws ClassNotFoundException
 * @throws NoSuchMethodException
 * @throws InvocationTargetException
 * @throws InstantiationException
 * @throws IllegalAccessException
 */
@Test
public void testConstructor() throws ClassNotFoundException, NoSuchMethodException, 
InvocationTargetException, InstantiationException, IllegalAccessException {
    String className = "com.yur.java.Person";
    Class<Person> clazz = (Class<Person>) Class.forName(className);
    //1.获取全部Constructor对象
    Constructor<Person>[] constructors = 
    (Constructor<Person>[]) Class.forName(className).getConstructors();
    for (Constructor<Person> constructor : constructors) {
        System.out.println(constructor);
    }
    //2.获取某一个指定的Constructor对象
    Constructor<Person> constructor = 
    clazz.getConstructor(String.class, int.class);
    System.out.println(constructor);
    //3.调用构造器的newInstance()方法创建对象
    Object obj = constructor.newInstance("Yorick", 21);
}
```
## Annotation
### 获取Annotation

- `getAnnotation()`
- `getDeclaredAnnotations()`

实例：
新建注解类：AgeValidator
```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(value = ElementType.METHOD)
public @interface AgeValidator {
    public int min();

    public int max();
}
```
对Person类的setAge()方法进行注解
```java
@AgeValidator(min = 18,max = 35)
public void setAge(int age) {
    this.age = age;
}
```
通过反射获取注解里的范围，对属性值进行限制
```java
@Test
public void testAnnotation() throws ClassNotFoundException, NoSuchMethodException, 
InvocationTargetException, InstantiationException, IllegalAccessException {
    String className = "com.yur.java.Person";
    Class clazz = Class.forName(className);
    Object obj = clazz.getConstructor().newInstance();
    Method method = clazz.getDeclaredMethod("setAge", int.class);
    int val = 20;
    Annotation annotation = method.getAnnotation(AgeValidator.class);
    if (annotation != null) {
        if (annotation instanceof AgeValidator) {
            AgeValidator ageValidator = (AgeValidator) annotation;
            if (val < ageValidator.min() || val > ageValidator.max()) {
                throw new RuntimeException("年龄非法");
            }
        }
    }
    method.invoke(obj, val);
    System.out.println(obj);
}
```
## 泛型和反射

实例：
通过反射，获得定义Class 时声明的父类的泛型参数的类型
- 获取带泛型参数的父类
`getGenericSuperclass()`
- `Type` 的子接口：`ParameterizedType`
- 可以调用`ParameterizedType`的`Type[] getActualTypeArguments()`获取泛型参数的数组。

BaseDao类
```java
public class BaseDao<T,PK> {
}
```
类EmployeeDao继承自BaseDao类
```java
public class EmployeeDao extends BaseDao<Employee,String>{
}
```
目标：通过反射，获得定义Class 时声明的父类的泛型参数的类型
```java
/**
 * 通过反射，获得定义Class 时声明的父类的泛型参数的类型
 *
 * @param clazz:子类对应的Class对象
 * @param index:子类继承父类时传入的泛型的索引，从0开始
 * @return
 */
public static Class getSuperClassGenericType(Class clazz, int index) {
    //获取父类
    Type genType = clazz.getGenericSuperclass();
    //获取具体的泛型参数
    if (!(genType instanceof ParameterizedType)) {
        return Object.class;
    }
    ParameterizedType parameterizedType =
            (ParameterizedType) genType;
    Type[] params = parameterizedType.getActualTypeArguments();
    if (index > params.length - 1 || index < 0) {
        return Object.class;
    }
    if (!(params[index] instanceof Class)) {
        return Object.class;
    }
    return (Class) params[index];
}
```
测试：
```java
@Test
public void testgetSuperClassGenericType() {
    Class clazz = EmployeeDao.class;
    //Employee.class
    Class argClazz = getSuperClassGenericType(clazz, 0);
    System.out.println(argClazz);
    //String.class
    argClazz = getSuperClassGenericType(clazz, 1);
    System.out.println(argClazz);
}
```