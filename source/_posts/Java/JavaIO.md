---
title: JavaIO
index_img: ./img/IOStream.png
categories: 
  - Java
date: 2022-04-30 15:42:04
tags: 
  - IO
  - 文件读写
sticky: 
---

# Java IO

- [Java IO](#java-io)
    - [IO概述](#io概述)
    - [File类](#file类)
    - [IO流分类](#io流分类)
    - [lnputStream \& Reader](#lnputstream--reader)
    - [OutputStream \& Writer](#outputstream--writer)
    - [缓冲流](#缓冲流)
    - [转换流](#转换流)
    - [RandomAccessFile类](#randomaccessfile类)
    - [对象的序列化](#对象的序列化)

### IO概述
Java的IO流主要包括输入、输出两种IO流，每种输入输出流有可分为字节流和字符流两大类:

### File类
File类代表与平台无关的文件和目录。
File能新建、删除、重命名文件和目录，但File 不能访问文件内容本身。如果需要访问文件内容本身，则需要使用输入/输出流。
相关方法：
```java
import org.junit.Test;
import java.io.File;
import java.io.IOException;

public class IOTest {

    @Test
    public void testFile() throws IOException {
        //创建File对象
        File file = new File("file.txt");

        //测试File对象的方法
        //文件名相关的方法
        String fileName = file.getName();
        System.out.println(fileName);

        //访问文件的绝对路径
        String path = file.getAbsolutePath();
        System.out.println(path);

        //为文件重命名
        file.renameTo(new File("d:\\hello.txt"));

        //文件检测相关方法
        System.out.println(file.exists());//false

        File dir = new File("hello");
        System.out.println(dir.isDirectory());//true

        //获取文件的常规信息
        System.out.println(file.length());

        //文件操作相关
        //新建文件
        File file1 = new File("aa.txt");
        file1.createNewFile();
    }
}
```
### IO流分类
按流向分：

- 输入流
- 输出流  

按处理的单位：

- 字节流(8位的字节)，所有二进制文件通用
- 字符流(16位的字节)，只能处理纯字符文本文件

按流的角色：

- 节点流:可以从一个特定的IO设备读/写数据的流
- 处理流:对一个已存在的流进行连接和封装，通过封装后的流来实现数据读/写操作

IO流体系 
![IO流体系](./img/IOStream.png)


### lnputStream & Reader
InputStream和 Reader是所有输入流的基类。
InputStream(典型实现:FileInputStream ) :
```java
- int read()
- int read(byte[] b)
- int read(byte[] b, int off, int len)
```
Reader (典型实现:FileReader ) :
```java
- int read()
- int read(char[] c)
- int read(char[] c, int off, int len)
```
程序中打开的文件IO资源不属于内存里的资源，垃圾回收机制无法回收该资源，所以应该显式关闭文件IO资源。
实例：
字节输入流
```java
//字节输入流，本段代码仅示例，实际运行要注释掉一部分
@Test
public void testInputStream() throws IOException {
    //创建一个字节输入流
    InputStream in = new FileInputStream("file.txt");
    //读取文件的内容
    //读取一个字节,效率很低，不建议，
    int result = in.read();

    //-1表示读取到文件的末尾
    while (result != -1) {
           System.out.print((char) result);
           result = in.read();
    }
        一次读一组,一组10个字节
    byte[] buffer = new byte[10];
    int len = 0;

    //返回读取的字节数，若为-1表示读取到文件的结尾
    while ((len = in.read(buffer)) != -1) {
        //末尾容易出错
        for (byte b : buffer) {
            System.out.print((char) b);
        }
        for (int i = 0; i < len; i++) {
            System.out.print((char) buffer[i]);
        }
    }

    //把内容读取到字节数组的部分连续的元素中
    byte[] result = new byte[1024 * 10];
    in.read(result, 10, in.available());

    //关闭流资源
    in.close();
}
```
字符输入流
```java
//字符输入流
@Test
public void testReader() throws IOException {
    //利用字符输入流读取hello.txt文档的内容，输出到控制台.
    Reader reader = new FileReader("file.txt");

    char[] buffer = new char[10];
    int len = 0;
    while ((len = reader.read(buffer)) != -1) {
        for (int i = 0; i < len; i++) {
            System.out.print(buffer[i]);
        }
    }
}
```
### OutputStream & Writer

OutputStream和Writer也非常相似:
```java
- void write(byte write/int c)
- void []/char[] buff)
- void write(byte[]/char[] buff, int off, int len);
```
因为字符流直接以字符作为操作单位，所以 Writer可以用字符串来替换字符数组，即以 String对象作为参数
```java
- void write(String str);
- void write(String str, int off, int len)
```
实例：
```java
    //测试字节输出流
    @Test
    public void testOutputStream() throws IOException {
        OutputStream out = new FileOutputStream("abcd.txt");

        String content = "www.yorick.com\n\rHello Yorick";
//        byte[] buffer = new byte[10];
//        int len = 10;
//
//        int time = content.length() / 10;
//
//
//        byte[] contentBytes = content.getBytes();
//
//        for (int i = 0; i < content.length() / 10; i++) {
//            //把String拆分为多个buffer
//            out.write(contentBytes, i * 10, len);
//        }
//
//        if (content.length() % 10 != 0) {
//           out.write(contentBytes,10*(content.length()/10),
//                   content.length()-10*(content.length()/10));
//        }

        out.write(content.getBytes(StandardCharsets.UTF_8));

        out.close();
    }
```
文件复制实例：

利用字节输入输出流。完成hello.txt文件的复制把该文件复制为hello2.txt
```java
@Test
public void testCopyFile() throws IOException{
    //1。创建定位到hello.txt的文件的输入流
    InputStream in = new FileInputStream("hello.txt");
    //2．创建定位到 hello2.txt的文件输出流
    OutputStream out = new FileOutputStream("hello2.txt");
    //3．创建一个 byte数组，用于读写文件
    byte [] buffer = new byte[ 1024*10];
    int len = 0;
    //4．读写文件:
    //in.read( buffer); out.write(buffer, 0, len);
    while ((len =in.read(buffer)) !=-1){
        out.write(buffer,0,len);
    }
    //5. 关闭流资源
    in.close();
    out.close();
}
```
利用字符输入输出流。完成hello.txt文件的复制把该文件复制为hello2.txt
```java
@Test
public void testCopyByReaderAndWriter() throws IOException {
    //1，创建字符输入，输出流
    Reader reader = new FileReader("hello.txt");
    Writer writer = new FileWriter("hello2.txt");
    //3. 创建一个字符数组。
    char[] buffer = new char[10];
    //4. 利用循环读取源文件，并向目标文件写入
    //5. 注意:使用的写入的方法:write(char[] buf，int off, int len)
    //而不能直接使用write(char[] buf)|
    int len = 0;
    while ((len = reader.read(buffer)) != -1) {
        writer.write(buffer, 0, len);
        System.out.println(len);
    }
    //2. 关闭流资源
    reader.close();
    writer.close();
}
```
### 缓冲流
文件复制（字符流）
```java
//复制hello.txt 为 hello3.txt
@Test
public void testBufferedReaderAndBufferedWrite() throws IOException {
    //1。创建 BufferedReader和 BufferedWriter
    BufferedReader bufferedReader = new BufferedReader(new FileReader("hello.txt"));
    BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter("hello3.txt"));

    //2. 进行读写操作
    String str = null;

    int i = 0;

    while ((str = bufferedReader.readLine()) !=null) {
        if (i != 0)
            bufferedWriter.write("\n");
        bufferedWriter.write(str);
        i++;
    }

    //3.关闭IO流,直接关闭包装流 ，内部会关闭节点流
    bufferedReader.close();
    bufferedWriter.close();
}
```
缓冲字节流，最常用的文件复制方法
```java
@Test
public void testBufferedInputStreamAndBufferedOutputStream()throws IOException{
    BufferedInputStream bIS = new BufferedInputStream(new FileInputStream("hello.txt"));
    BufferedOutputStream bOT = new BufferedOutputStream(new FileOutputStream("hello4.txt"));

    byte [] buffer = new byte[1024];
    int len = 0;

    while ((len = bIS.read(buffer))!= -1){
        bOT.write(buffer,0,len);
    }

    bIS.close();
    bOT.close();
}
```
### 转换流
字节流和字符流相互转换
实例一：
```java
@Test
public void testInputStreamReader() throwsIOException {
    //指向文档的字节流
    InputStream in = new FileInputStream("hello.txt");
    //把上面的流转为字符流
    Reader reader = new InputStreamReader(in);
    //把字符流转为带缓冲的字符流
    BufferedReader bufferedReader = new BufferedReader(reader);
    //打印文本内容
    String str = null;
    while ((str = bufferedReader.readLine()) != null) {
        System.out.println(str);
    }
    //关闭
    in.close();
    reader.close();
    bufferedReader.close();
}
```
实例二：
```java
@Test
public void testOutStreamReader() throws IOException {
    //先创建两个字节输入输出流:分别指向hello.txt, hello5.txt
    InputStream in = new FileInputStream("hello.txt");
    OutputStream out = new FileOutputStream("hello5.txt");
    //然后再转为字符输入输出流
    Reader reader = new InputStreamReader(in);
    Writer writer = new OutputStreamWriter(out);
    //再转为带缓冲的字符输入输出流
    BufferedReader bufferedReader = new BufferedReader(reader);
    BufferedWriter bufferedWriter = new BufferedWriter(writer);
    //完成文件的复制
    int i = 0;
    String str = null;
    while ((str = bufferedReader.readLine()) != null) {
        if (i != 0)
            writer.write("\n");
        writer.write(str);
        i++;
    }
    //关闭
    in.close();
    reader.close();
    bufferedReader.close();
    bufferedWriter.close();
    writer.close();
    out.close();
}
```
### RandomAccessFile类
RandomAccessFile类既可以读取文件内容，也可以向文件输出数据。
RandomAccessFile类支持“随机访问”的方式，程序可以直接跳到文件的任意地方来读写文件。

- 支持只访问文件的部分内容
- 可以向已存在的文件后追加内容  
  

RandomAccessFile对象包含一个记录指针，用以标示当前读写处的位置。RandomAccessFile类对象可以自由移动记录指针：

- long getFilePointer()：获取文件记录指针的当前位置
- void seek(long pos)：将文件记录指针定位到pos 位置
  

创建RandomAccessFile类可以指定一个mode参数，该参数指定RandomAccessFile的访问模式：
- r：以只读方式打开
- rw：以读、写方式打开  
  

实例一：
```java
@Test
public void testRandomAccessFile() throws IOException {
    //1.创建 RandomAccessFile类
    RandomAccessFile accessFile = new RandomAccessFile("hello.txt", "rw");
    //3. 对文件进行读取
    String str = null;
    while ((str = accessFile.readLine()) != null) {
        System.out.println(str);
    }
    //4.向文件结尾写入
    accessFile.writeBytes("www.yorick.com");
    //2.关闭
}
```
实例二：
向hello.txt文件中插入一行:I Love KongFu，
插入到第二行，原内容下移。
```java
@Test
public void testRandomAccessFile2() throws IOException {
    //创建 RandomAccessFile类
    RandomAccessFile accessFile = new RandomAccessFile("hello.txt", "rw");
    //先读一行
    String line = accessFile.readLine();
    //把第一行后面的内容先读取到一个byte数组中
    byte[] buffer = new byte[(int) (accessFile.length() - line.length())];
    accessFile.read(buffer);
    //移动指针到第一行的后面
    accessFile.seek(line.length());
    //写入字符
    accessFile.writeBytes("\nI Love KongFu\n");
    //写入第二行往后的内容
    accessFile.write(buffer);
    //关闭
    accessFile.close();
}
```

### 对象的序列化
对象序列化的目标是将对象保存到磁盘上，或允许在网络中直接传输对象。
序列化是 RMI ( Remote Method Invoke-远程方法调用）过程的参数和返回值都必须实现的机制，而RMI是JavaEE的基础。因此序列化机制是JavaEE平台的基础。
如果需要让某个对象支持序列化机制，则必须让的类是可序列化的，为了让某个类是可序列化的，该类必须实现如下两个接口之一︰
- Serializable
- Externalizable

若某个类实现了Serializable接口，该类的对象就是可序列化的：
- 创建一个ObjectOutputStream
- 调用ObjectOutputStream对象的writeObiect()方法输出可序列化对象  
  

反序列化：
- 创建一个ObjectInputStream
- 调用readObject(方法读取六种的对象  

如果某个类的字段不是基本数据类型或 String类型，而是另一个引用类型，那么这个引用类型必须是可序列化的，否则拥有该类型的Field的类也不能序列化
实例：
Person类
```java
import java.io.Serializable;

public class Person implements Serializable {
    
    // 类的版本号:用于对象的序列化。具体用于读取对象时比对硬盘上对象的版本和
    // 程序中对象的版本是否一致,若不一致读取失败，并抛出异常。
    private static final long serialVersionUID = 8461301440305913644L;

    private String name;
    private int age;
    private Address address;

    public Person() {
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
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

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", address=" + address +
                '}';
    }
}
```
包含字段Address，Address类也要序列化
```java
import java.io.Serializable;

public class Address implements Serializable {
    private static final long serialVersionUID = -1872787737087373355L;
    private String city;

    public Address(String city) {
        this.city = city;
    }

    public Address() {
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    @Override
    public String toString() {
        return "Address{" +
                "city='" + city + '\'' +
                '}';
    }
}
```
序列化，将person对象写入磁盘
```java
@Test
public void testSerializable() throws IOException {
    Person person = new Person("AA", 12);
    person.setAddress(new Address("BeiJing"));
    //使用ObjectOutputStream 把对象写到硬盘上
    OutputStream out = new FileOutputStream("d:\\obj.txt");
    ObjectOutputStream objectOutputStream = new ObjectOutputStream(out);
    objectOutputStream.writeObject(person);
    out.close();
    objectOutputStream.close();
}
```
反序列化，从磁盘读取person对象
```java
@Test
public void testObjectInputStream() throws IOException, ClassNotFoundException {
    InputStream inputStream = new FileInputStream("d:\\obj.txt");
    ObjectInputStream objectInputStream = new ObjectInputStream(inputStream);
    Object obj = objectInputStream.readObject();
    System.out.println(obj);
    objectInputStream.close();
    inputStream.close();
}
```

