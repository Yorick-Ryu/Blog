---
title: Java泛型
index_img: /img/default.png
categories: 
  - Java
date: 2022-04-23 16:44:23
tags: 
  - 泛型
  - Generic
sticky: 
---

# Java泛型

- [Java泛型](#java泛型)
    - [在集合中使用泛型](#在集合中使用泛型)
    - [定义简单的泛型](#定义简单的泛型)
    - [泛型和子类继承](#泛型和子类继承)
      - [通配符](#通配符)
    - [泛型方法](#泛型方法)

### 在集合中使用泛型

对于集合没有泛型的情况:

1. 放入集合中的对象可以是任意类型.
2. 获取元素后，需进行类型的强制转换。  

如下所示：
```java
List persons = new ArrayList();
//放入集合中的对象可以是任意类型
persons.add(new Person("AA",12));
persons.add(new Person("BB",13));
persons.add(new Person("CC",14));
persons.add(new Person("DD",15));
persons.add("person");

Object obj = persons.get(0)
//获取元素后，需进行类型的强制转换
Person person = (Person) persons.get(1);
//这里遍历会出现类型转换异常
for (int i = 0;i<persons.size();i++){
    Person person = (Person) persons.get(i);
    System.out.println(person);
}
```
使用泛型之后，`List<Person>`是一个带一个类型参数的泛型接口
```java
List<Person> persons = new ArrayList<>();
//只能放类型为Person的类
persons.add(new Person("AA", 12));
persons.add(new Person("BB", 13));
persons.add(new Person("CC", 14));
persons.add(new Person("DD", 15));
//遍历时不用类型转换
for (Person person : persons) {
    System.out.println(person);
}
//告诉返回类型为person
Person[] personArray = persons.toArray(Person[0]);
System.out.println(personArray.length);//4
```
Map使用泛型
```java
Map<String, Person> personMap = new HashMap<();

personMap.put("AA", persons.get(0));
personMap.put("BB", persons.get(1));
personMap.put("CC", persons.get(2));
personMap.put("DD", persons.get(3));

for (Map.Entry<String, Person> entry : personMap.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```
### 定义简单的泛型

```java
//在声明类的同时声明泛型类型，T为形参，一般为单个大写字母
public class DAO<T> {
    //方法的返回值可以使用前面声明的泛型类型
    public T get(Integer id){
        T result = null;
        return result;
    }
    //方法的参数也可以使用声明类时声明的泛型类型.
    public void save(T entity){
    }
}
```
类型参数在整个类的声明中可用，几乎是所有可以使用其他普通类型的地方

使用：
```java
//传入实参Person
DAO<Person> dao = new DAO<>();
Person person = dao.get(10);
dao.save(new Person());
```
### 泛型和子类继承
String 为 Object 类型的子类，则String[] 也是Object[] 的子类。
```java
Object [] objects = new String[]{"AA","BB"};
```
String 为 Object 类型的子类，而`List<String>`不是`List<Object>`的子类！

#### 通配符
实例：
```java
Collection<?> c = new ArrayList<String>();
//可以正常取，但不能放入任何对象，除了null 
c.add(new Object());//编译错误
c.add(null);//只能放null
```
```java
//工具方法，打印Person信息
//List<? extends Person代表可以放入所有Person的子类
public static void printPersonInfo(List<?> extends Person> persons) {
    //不能放，只能取
    for (Person person : persons) {
        System.out.println(person);
    }
}

public static void main(String[] args) {

    List<Student> stus = new ArrayList<>();
    stus.add(new Student("BB",22,"NIIT"));
    printPersonInfo(stus);

    List<Person> personList = new ArrayList<>();
    personList.add(new Person("AA",12));
    printPersonInfo(personList);
}
//输出：
//Person [name='BB', age=22, school=NIIT]
//Person [name='AA', age=12]
```
### 泛型方法
泛型方法:在方法声明时，同时声明泛型。在方法的返回值，参数列表以及方法体中都可以使用泛型类型.

实例：
把指定类型的数组中的元素放入到指定类型的集合中
```java
public static <T> void fromArrayToCollection(T[] objs, Collection<T> coll){
        
}

public static void main(String[] args) {
        
    String [] objs = new String[]{"AA","BB","CC"};
    Collection<String> coll = new ArrayList<>();
    fromArrayToCollection(objs,coll);
}
```

