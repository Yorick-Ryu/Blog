---
title: Java集合
index_img: ./img/javaAssemble.png
categories: 
  - Java
date: 2022-04-23 21:26:16
tags: 
  - 集合
  - Collection
  - Set
  - TreeSet
  - List
  - Map
  - HashMap
  - HashTable
sticky: 
---

# Java集合

目录：
- [Java集合](#java集合)
    - [Collection](#collection)
      - [添加元素](#添加元素)
      - [访问集合的方法](#访问集合的方法)
      - [移除集合中的元素](#移除集合中的元素)
      - [检测集合的方法](#检测集合的方法)
      - [集合的其他方法](#集合的其他方法)
    - [Set](#set)
      - [HashSet](#hashset)
      - [LinkedHashSet](#linkedhashset)
      - [TreeSet](#treeset)
        - [自然排序](#自然排序)
        - [定制排序](#定制排序)
    - [List](#list)
    - [Map](#map)
      - [HashMap](#hashmap)
      - [Hashtable](#hashtable)
      - [LinkedHashMap](#linkedhashmap)
      - [TreeMap](#treemap)
      - [Properties](#properties)
    - [Collections 工具类](#collections-工具类)
      - [排序方法](#排序方法)
      - [查找\&替换方法](#查找替换方法)
      - [同步控制方法](#同步控制方法)
    - [Enumeration](#enumeration)

Java集合就像一种容器，可以把多个对象的引用放入容器中。  

Java集合类可以用于存储数量不等的多个对象，还可用于保存具有映射关系的关联数组。

Java集合可分为 Set、List 和 Map 三种体系
- Set：无序、不可重复的集合
- List：有序、可重复的集合
- Map：具有映射关系的集合

在Java5之前，Java集合会丢失容器中所有对象的数据类型，把所有对象都当成Object类型处理；从Java5增加了**泛型**以后，Java集合可以记住容器中对象的数据类型。

![JavaAssemble](./img/javaAssemble.png)

### Collection

创建一个Collection接口的对象

```java
Collection collection = new ArrayList();
```

#### 添加元素

1. `add()`参数为要添加的元素对象
    ```java
    collection.add(new Person());
    ```
2. `addAll()`参数为要添加的集合对象
    ```java
    Collection collection2 = new ArrayList();
    collection2.add(new Person());
    collection2.add(new Person());
    collection.addAll(collection2);
    ```

#### 访问集合的方法

1. `size()`获取集合长度
    ```java
    System.out.println(collection.size());
    ```
2. `iterator()`对集合进行遍历，`iterator()`可以得到对应的`Iterator`对象。
   `Iterator`:迭代器
   使用方法：
    ```java
    //获取Iterator接口对象
    Iterator iterator = collection.iterator();
    //使用while循环和Iterator遍历集合的每一个元素。
    //具体使用Iterator接口的hasNext()和next()方法。
    while (iterator.hasNext()){
        Object obj = iterator.next();
        System.out.println(obj);
    }
    ```
1. 使用增强for循环的方式来对集合进行遍历
    ```java
    for(Object obj: collection){
        System.out.println(obj);
    }
    ```
#### 移除集合中的元素
1. `remove()`移除某一个指定的对象。通过`equals()`方法来判断要移除的那个元素在集合中是否存在，以及是否能够成功移除。参数为要移除的元素对象，返回是否成功的布尔值。  
    ```java
    boolean result = collection.remove(new Person());
    System.out.printIn(result);
    //返回：false
    ```
2. `removeAll()`参数为要移除的元素集合对象。
    ```java
    boolean result = collection.removeAll(collection2);
    System.out.printIn(result);
3. `clear()`使集合元素置空。
   ```java
   collection.clear()
   ```
#### 检测集合的方法
1. `contains()`检测集合是否包含某一元素
   ```java
   System.out.println(collection.contains(new Person()));
   //返回：false
   ```
2. `containsAll()`检测集合是否包含某一元素集合
   ```java
   System.out.println(collection.containsAll(collection2));
   ```
3. `isEmpty()`检测集合是否为空
   ```java
   System.out.println(collection.isEmpty());//false
   collection.clear();
   System.out.println(collection.isEmpty());//true
   ```
#### 集合的其他方法
1. `toArry()`
    ```java
    Object [] objects = collection.toArray();
    System.out.println(objects.length);
    ```
2. `toArry(T[])`涉及泛型
3. `equals()`比较两集合是否相等
   ```java
   //有序集合
   Collection collection3 = new ArrayList();
   collection3.add(p1);
   collection3.add(p2);
   Collection collection4 = new ArrayList();
   collection4.add(p2);
   collection4.add(p1);
   System.out.println(collection3.equals(collection4));
   //返回false
   
   //无序集合
   Collection collection3 = new HashSet();
   collection3.add(p1);
   collection3.add(p2);
   Collection collection4 = new HashSet();
   collection4.add(p2);
   collection4.add(p1);
   System.out.println(collection3.equals(collection4));
   //返回true
   ```
4. `hasCode()`
5. 使用增强for循环的方式来对集合进行遍历
   ```java
   for (Object obj : collection) {
       System.out.println(obj);
       }
   ```

### Set

1. Set是 Collection 的子接口
2. Set中不允许存放相同的元素。
3. 判定相同元素的标准是，两个对象**各**调用`equals()`方法，返回`true`。

#### HashSet

HashSet是Set接口的典型实现。

基本特征：
1. 不能保证元素的排列顺序（无序）
2. HashSet 不是线程安全的
3. 集合元素可以使`null`
   ```java
   Set set = new HashSet();
   set.add(null);
   System.out.println(set.size());
   //输出1
   ```
4. 对于 HashSet：如果两个对象通过`equals()`方法返回 true，这两个对象的 hashCode 值也应该相同。
   ```java
   
   set.add(new Person("xx",12));
   set.add(new Person("xx",12));
   System.out.println(set.size());
   //正常情况下输出4，两个对象不相同
   //在Person类中重写equals方法和hashcode方法
   @Override
   public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && name.equals(person.name);
   }
   
   @Override
   public int hashCode() {
        return Objects.hash(name, age);
   }
   //重写后返回3
   ```
5. 由根据元素自身属性计算的 hashCode 决定位置，所以可重写hashCode实现重复（不推荐）和有序类似 LinkedHashSet
   ```java
    //在Person类中重写hashCode方法
    private static int init = 0;
    @Override
    public int hashCode() {
        return init++;
    }
   ```

#### LinkedHashSet

1. LinkedHashSet 是 HashSet 的子类
2. 使用链表维护元素的次序，这使得元素看起来是以插入顺序保存的，也因此性能稍弱
3. LinkedHashset 不允许集合元素重复
4. 重写类的`hashCode()`方法也可以在 HashSet 实现序列化

#### TreeSet

TreeSet是SortedSet接口的实现类，TreeSet可以确保集合元素处于排序状态

##### 自然排序

TreeSet 会调用集合元素的`compareTo(Object obj)`方法来比较元素之间的大小关系，然后将集合元素按升序排列如果试图把一个对象添加到 TreeSet 时，则该对象的类必须实现 Comparable 接口。

实现 Comparable 的类必须实现`compareTo(Object obj)`方法，两个对象即通过`compareTo(Object obj)`方法的返回值来比较大小，返回值类型为int，正数表示当前元素大，负数表示参数元素大，返回0代表两元素相等。
```java
//实现Comparable接口
public class Students implements Comparable {
    private String name;
    public int score;

    public Students(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }
}
```

1. 因为只有相同类的两个实例才会比较大小，所以向 TreeSet 中添加的应该是**同一个类**的对象，否则可能发生类型转换异常。

2. 当需要把一个对象放入 TreeSet 中,重写该对象对应的`equals()`方法时，应保证该方法与`compareTo(Object obj)`方法有一致的结果：如果两个对象通过`equals()`方法比较返回`true`，则通过`compareTo(Object obj)`方法比较应返回`0`。
   ```java
   public int compareTo(Object o) {
        if (o instanceof Students) {
            Students stu = (Students) o;
            return this.score - stu.score;//分数升序排
            return - this.score + stu.score;//分数降序排
            //return -this.name.compareTo(stu.name);//按name字母顺序降序排
        } else {
            throw new ClassCastException("不是一个Student对象");
        }
    }
   ```

##### 定制排序

创建 TreeSet 对象时，传入 Comparator 的接口实现类。
```java
Comparator comparator = new Comparator() {
    @Override
    public int compare(Object o1, Object o2) {
        if (o1 instanceof Person && oinstanceof Person) {
            Person p1 = (Person) o1;
            Person p2 = (Person) o2;
            return -p1.getAge() + p2.getAge;//年龄降序
        } else {
            throw new ClassCastException("不能转为 Person");
        }
    }
};
Set set1 = new TreeSet<>(comparator);
set1.add(new Person("AA", 12));
set1.add(new Person("AA", 15));
set1.add(new Person("AA", 9));
set1.add(new Person("AA", 16));

for (Object p : set1) {
    System.out.println(p);
}
//输出：
//Person{name='AA', age=16}
//Person{name='AA', age=15}
//Person{name='AA', age=12}
///Person{name='AA', age=9}
```
这样Person就不需要实现`compareTo`接口
要求：Comparator 接口的`compare()`方法的返回值和两个元素的`equals()`要一致。

### List
1. List 代表一个元素有序、且可重复的集合，集合中的每个元素都有其对应的顺序索引。
2. List 允许使用重复元素，可以通过索引来访间指定位置的集合元素。
3. List 默认按元素的添加顺序设置元素的索引。

方法：
```java
- void add(int index, Objed ele)
//将元素插入到指定位置
- boolean addAll(int index, Collection eles)
//将集合插入到指定位置
- Object get(int index)
//获取指定位置的对象
- int indexOf(Objed obj)
//获取指定元素的索引，用equals方法判定，重复元素取第一个。
- int lastIndexOf(Objed obj)
//重复元素取最后一个
- Object remove(int index)
//移除指定位置的对象
- Object set(int index,Objed ele) 
//替换指定位置元素
- List subList(int fromlndex, int tolndex) 
//取区间内元素，前闭后开
List list2 = list.subList(2, 5);//2,3,4
for (Object obj : list2) {
    System.out.println(obj);
}
```

List额外提供了一个listIterator()方法，该方法返回一个ListLterator对象，Listerator接口继承了Iterator接口，提供了专门操作List的方法：
```java
- boolean hasPrevious()
- Object previous()
- void add()
```

ArrayList是List接口的典型实现
```java
List list = new ArrayList();
```

遍历：
```java
//使用Iterator
Iterator it = list.iterator();
while (it.hasNext()) {
    System.out.println(it.next());
}
//使用增强for循环
for (Object o : list) {
    System.out.println(o);
}
//使用for循环和List的get(int)方法
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}
//使用ListIterator
ListIterator lit = list.listIterator();
while (lit.hasNext()) {
    System.out.println(lit.next());
}
```
Vector也是List接口的远古典型实现，虽然线程安全但是不推荐使用。

Arrays.asList(...)方法返回的 List 集合既不是 ArrayList实例，也不是Vector实例。Arrays.asL.ist(...)返回值是一个固定长度的 List集合。
```java
System.out.println(Arrays.asList(new Person("MM",23),
new Person("NN",22)));
//[Person{name='MM', age=23}, Person{name='NN', age=22}]
```

### Map
- Map用于保存具有映射关系的数据，因此Map集合里保存着两组值，一组值用于保存Map里的 Key，另外一组用于保存Map里的Value。
- Map中的 key 和 value 都可以是任何引用类型的数据
- **Map中的 Key 不允许重复**，即同一个Map对象的任何两个Key通过equals方法比较中返回false
- Key和 Value之间存在单向一对一关系，即通过指定的Key总能找到唯一的，确定的Value。



#### HashMap
HashMap是Map接口的典型实现
```java
Map<String, Object> map = new HashMap<>();
```
常用方法：
```java
//1.添加元素
map.put("AA", new Person("AA", 12));//被覆盖
map.put("AA", new Person("AAA", 12));
map.put("CC", new Person("CCC", 12));
map.put("MM", new Person("MMM", 12));
map.put("DD", new Person("DDD", 12));
//2.取出元素（遍历）
//2.1得到键的集合，再利用键得到值
Set keySet = map.keySet();
for (Object key : keySet) {
    System.out.println(key + ": " + map.get(key));
}
//2.2直接得到value的集合
Collection values = map.values();
System.out.println(values.getClass());
for (Object val : values) {
    System.out.println(val);
}
//2.3得到键值对的集合
for (Map.Entry<String, Object> entry : map.entrySet()) {
    String key = entry.getKey();
    Object val = entry.getValue();
    System.out.println(key + ": " + val);
}
//3.移除元素
map.remove("AA");
//4.工具方法
System.out.println(map.size());//3
System.out.println(map);
//contains(); isEmpty()
System.out.println(map.containsKey("CC"));//true
System.out.println(map.isEmpty());//false
```
HashMap和HashSet：[HashSet](#hashset) 是由HashMap定义的
#### Hashtable
HashMap是Map接口的古老典型实现，不建议使用
Hashtable不允许使用null 作为key和 value，而 HashMap可以
#### LinkedHashMap
LinkedHashMap 是 HashMap 的子类
LinkedHashMap可以维护 Map 的迭代顺序:迭代顺序与Key-Value对的插入顺序一致
[LinkedHashSet](#linkedhashset) 是由 LinkedHashMap 定义的
#### TreeMap
TreeMap存储Key-Value 对时，需要根据Key对key-value 对进行排序。TreeMap可以保证所有
的Key-Value对处于有序状态。
方法参考 [TreeSet](#treeset)
```java
Comparator comparator = new Comparator() {
    @Override
    public int compare(Object o1, Object o2){
        Person p1 = (Person) o1;
        Person p2 = (Person) o2;
        return p1.getAge() - p2.getAge();//增序
    }
};
//注意要传入comparator参数，只能对key进行排序
TreeMap tm = new TreeMap(comparator);
tm.put(new Person("AA", 12), "AAA");
tm.put(new Person("BB", 32), "AAA");
tm.put(new Person("CC", 25), "AAA");
tm.put(new Person("DD", 22), "AAA");
//遍历
keySet = tm.keySet();
for (Object key : keySet) {
    Object val = tm.get(key);
    System.out.println(key + "：" + val);
}
/*输出
Person [name='AA', age=12]：AAA
Person [name='DD', age=22]：AAA
Person [name='CC', age=25]：AAA
Person [name='BB', age=32]：AAA
*/
```
#### Properties
Properties类是Hashtable的子类，该对象用于处理属性文件
由于属性文件里的key、value都是字符串类型，所以properties里的 Key和 Value都是字符串类型的

properties文件在Java中对一个的是一个 Properties类的对象
```properties
url=jdbc:mysql:///test
driver=com.mysql.jdbc.Driver
user=root
password=964538
```
方法：
```java
//1。创建一个Properties类的对象
Properties properties = new Properties();
//2，使用 IO 流加载对应的properties文件，注意抛异常
properties.load(new FileInputStream("jdbproperties"));
//3．得到对应的属性值
String url = properties.getProperty("url");
System.out.println(url);
//输出：jdbc:mysql:///test
```


### Collections 工具类

Collections是一个操作Set、List和 Map等集合的工具类

#### 排序方法
```java
reverse(List)
//反转List中元素的顺序
shuffle(List)
//对List集合元素进行随机排序
sort(List)
//根据元素的自然顺序对指定List集合元秦按升序排序
sort(List , Comparator):
//根据指定的Comparator产生的顺序对List集合元秦进行排序
swap(List , int , int)
//将指定list集合中的i处元素和j处元秦进行交换
```
实例：

根据指定的Comparator产生的顺序对List集合元秦进行排序
```java
Collections.sort(list, new Comparator() {
    @Override
    public int compare(Object o1, Object o2) {
        Person p1 = (Person) o1;
        Person p2 = (Person) o2;
        return p1.getAge() - p2.getAge();
    }
});
```
#### 查找&替换方法

```java
Object max(Collection)
//根据元素的自然顺序,返回给定集合中的最大元素
Object max(Collection , Comparator)
//根据Comparator指定的顺序,返回给定集合中的最大元素
Object min(Collection)
Object min(Collection , Comparator)
int frequency(Collection , Object)
//返回指疋集合甲指疋兀素的出现次数
boolean replaceAll(List list , Object oldVal , Object newVal)
//使用新值替换List对象的所有旧值
```
实例：

根据Comparator指定的顺序,返回给定集合中的最大元素
```java
System.out.println(Collections.max(list,new Comparator() {
    @Override
    public int compare(Object o1, Object o2) {
        Person p1 = (Person) o1;
        Person p2 = (Person) o2;
        return p1.getAge() - p2.getAge();
    }
}));
```
#### 同步控制方法

使用 synchronizedList(),将参数里的集合变成线程安全的
```java
//获取线程安全的List 对象，使用 synchronizedList()
List list2 = Collections.synchronizedList(new ArrayList<>());
```
### Enumeration
Enumeration 接口是lterator迭代器的“古老版本”

实例：
```java
//对Enumeration对象进行遍历 hasMoreElements() nextElement()
Enumeration names = Collections.enumerati(list);
while (names.hasMoreElements()){
    Object obj = names.nextElement();
    System.out.println(obj);
}
```
