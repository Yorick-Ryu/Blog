---
title: Android活动（Activity）
index_img: /img/activity_life_cycle.png
categories:
  - Android
date: 2022-11-29 18:15:48
tags: 
  - activity
sticky:
---

# 活动(Activity)

<!-- toc -->

## 启停活动页面

### Activity的启动和结束
- 从当前页面跳到新页面，跳转代码如下：
`startActivity(new Intent(源页面.this,目标页面.class));`
- 从当前页面回到上一个页面，相当于关闭当前页面，返回代码如下：
  `finish();//结束当前的活动页面`

### Activity的生命周期

![activity_life_cycle](./img/activity_life_cycle.png)

onCreate：创建活动。把页面布局加载进内存，进入了初始状态。
onStart：开始活动。把活动页面显示在屏幕上，进入了就绪状态。
onResume：恢复活动。活动页面进入活跃状态，能够与用户正常交互，例如允许响应用户的点击动作、允许用户输入文字等等。
onPause：暂停活动。页面进入暂停状态，无法与用户正常交互。
onStop：停止活动。页面将不在屏幕上显示。
onDestroy：销毁活动。回收活动占用的系统资源，把页面从内存中清除。onRestart：重启活动。重新加载内存中的页面数据。
onNewlntent：重用已有的活动实例。

如果一个Activity已经启动过，并且存在当前应用的Activity任务栈中，启动模式为singieTask，singlelnstance或singleTop(此时已在任务栈顶端)，那么在此启动或回到这个Activity的时候，不会创建新的实例，也就是不会执行onCreate方法，而是执行onNewlntent方法。

**各状态的切换过程：**

![activity_state](./img/activity_state.png)

### Activity的启动模式

打开AndroidManifest.xml，给activity节点添加属性`android:launchMode`，属性值填入`standard`表示采取标准模式，当然不添加属性的话默认就是标准模式。具体的activity节点配置内容示例如下:


#### 默认启动模式 standard

该模式可以被设定，不在manifest 设定时候，Activity 的默认模式就是standard。在该模式下，启动的 Activity 会依照启动顺序被依次压入Task栈中：

![standard_mode](img/standard_mode.png)

#### 栈顶复用模式 singleTop

在该模式下，如果栈顶Activity为我们要新建的Activity(目标Activity)，那么就不会重复创建新的Activity。

![single_top_mode](img/single_top_mode.png)

**应用场景**

适合开启渠道多、多应用开启调用的Activity，通过这种设置可以避免已经创建过的Activity被重复创建，多数通过动态设置使用。


#### 栈内复用模式 singleTask

与singleTop模式相似，只不过singleTop模式是只是针对栈顶的元素，而singleTask模式下，如果task栈内存在目标Activity实例，则将task内的对应Activity 实例之上的所有Activity弹出栈，并将对应Activity置于栈顶，获得焦点。

![single_task_mode](img/single_task_mode.png)

**应用场景**

**程序主界面**：我们肯定不希望主界面被创建多次，而且在主界面退出的时候退出整个App是最好的效果。

**耗费系统资源的Activity**：对于那些及其耗费系统资源的Activity，我们可以考虑将其设为singleTask模式，减少资源耗费。


#### 全局唯一模式 singlelnstance

在该模式下，我们会为目标Activity创建一个新的Task栈，将目标Activity放入新的Task，并让目标Activity获得焦点。新的Task有且只有这一个Activity 实例。如果已经创建过目标Activity实例，则不会创建新的Task，而是将以前创建过的Activity唤醒。

![single_instance_mode](./img/single_instance_mode.png)

#### 动态设置启动模式

可以为intend设置不同启动标志

`intent.setF1ags(Intent.FLAG_ACTIVITY_CLEAR_TOP);`

##### FLAG_ACTIVITY_NEW_TASK

该标志用于开辟新任务的活动栈

##### FLAG_ACTIVITY_SINGLE_TOP

当栈顶为待跳转的活动实例之时，则重用栈顶的实例

##### FLAG_ACTIVITY_CLEAR_TASK

该标志会清空当前活动栈里的所有实例

##### FLAG_ACTIVITY_CLEAR_TOP

当设置此Flag时，目标 Activity 会检查Task 中是否存在此实例，如果没有则添加压入栈。如果有，就将位于Task中的对应Activity其上的所有Activity弹出栈，此时有以下两种情况：
- 如果同时设置Flag_ACTIVITY_SINGLE_TOP，则直接使用栈内的对应Activity。
`intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);`
- 没有设置，则将栈内的对应Activity 销毁重新创建。

##### FLAG_ACTIVITY_NO_HISTORY

栈中不保存新启动的活动实例


**应用场景示例：**

对于不允许重复返回的情况，可以设置启动标志`FLAG_ACTIVITY_CLEAR_TOP`，即使活动栈里面存在待跳转的活动实例，也会重新创建该活动的实例，并清除原实例上方的所有实例，保证栈中最多只有该活动的唯一实例，从而避免了无谓的重复返回。


对于回不去的登录页面情况，可以设置启动标志`FLAG_ACTMTY_CLEAR_TASK`，该标志会清空当前活动栈里的所有实例。不过全部清空之后，意味着当前栈没法用了，必须另外找个活动栈才行，也就是同时设置启动标志`FLAG_ACTIVTY_ NEW_TASK`，该标志用于开辟新任务的活动栈。

`intent.setF1ags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);`

## 在活动之间传递消息

Intent是各个组件之间信息沟通的桥梁，它用于Android各组件之间的通信，主要完成下列工作：

- 标明本次通信请求从哪里来、到哪里去、要怎么走。
- 发起方携带本次通信需要的数据内容，接收方从收到的意图中解析数据。
- 发起方若想判断接收方的处理结果，意图就要负责让接收方传回应答的数据内容。

### Intent的组成部分

| 元素名称  | 设置方法     | 说明与用途                        |
| --------- | ------------ | --------------------------------- |
| Component | setComponent | 组件，它指定意图的来源与目标      |
| Action    | setAction    | 动作，它指定意图的动作行为        |
| Data      | setData      | 即Uri，它指定动作要操纵的数据路径 |
| Category  | addCategory  | 类别，它指定意图的操作类别        |
| Type      | setType      | 数据类型，它指定消息的数据类型    |
| Extras    | putExtras    | 扩展信息，它指定装载的包裹信息    |
| Flags     | setFlags     | 标志位，它指定活动的启动标志      |


### 显式lntent和隐式Intent

**显式lntent，直接指定来源活动与目标活动，属于精确匹配**

在构建一个意图对象时，需要指定两个参数，第一个参数表示跳转的来源页面，即"来源`Activity.this`"；第二个参数表示待跳转的页面，即"目标`Activity.class`"。具体的意图构建方式有如下3种：

(1) 在Intent的构造函数中指定，示例代码如下：

```java
// 创建一个目标确定的意图
Intent intent = new Intent(this,ActNextActivity.class);
```

(2) 调用意图对象的`setClass`方法指定，示例代码如下：

```java
// 创建一个新意图
Intent intent = new Intent();
// 设置意图要跳转的目标活动
intent.setclass(this,ActNextActivity.class);
```

(3) 调用意图对象的`setComponent`方法指定，示例代码如下：
```java
// 创建一个新意图
Intent intent = new Intent();
// 创建包含目标活动在内的组件名称对象
ComponentName component = new componentName(this,ActNextActivity.c1ass);
// 设置意图携带的组件信息
intent.setcomponent(component); 
```

这种方式可用于启动其他应用（包括系统应用）的Activity

只需知道包名和类名即可

```java
ComponentName component = new ComponentName(pkg:"",cls:"");
```

**隐式Intent，没有明确指定要跳转的目标活动，只给出一个动作字符串让系统自动匹配，属于模糊匹配**

通常App不希望向外部暴露活动名称，只给出一个事先定义好的标记串，这样大家约定俗成、按图索骥就好，隐式lntent便起到了标记过滤作用。这个动作名称标记串，可以是自己定义的动作，也可以是已有的系统动作。常见系统动作的取值说明见表。

| lntent类的系统动作常量名 | 系统动作的常量值             | 说明            |
| ------------------------ | ---------------------------- | --------------- |
| ACTION_MAIN              | android.intent.action.MAIN   | App启动时的入口 |
| ACTION_VIEW              | android.intent.action.VIEW   | 向用户显示数据  |
| ACTION_SEND              | android.intent.action.SEND   | 分享内容        |
| ACTION_CALL              | android.intent.action.CALL   | 直接拨号        |
| ACITON_DIAL              | android.intent.action.DIAL   | 准备拨号        |
| ACTION_SENDTO            | android.intent.action.SENDTO | 发送短信        |
| ACTION_ANSWER            | android.intent.action.ANSWER | 接听电话        |

**示例：拨打指定电话**

```java
Intent intent = new Intent();
intent.setAction(Intent.ACTION_DIAL);
Uri uri =  Uri.parse("tel:"+phoneNo);
intent.setData(uri);
startActivity(intent);
```

**示例：发送短信到指定号码**

```java
Intent intent = new Intent();
intent.setAction(Intent.ACTION_SENDTO);
Uri uri =  Uri.parse("smsto:"+phoneNo);
intent.setData(uri);
startActivity(intent);
```

**示例：自定义隐式  intent**

在目标Activity的清单文件中加入`<intent-filter>`
```xml
<activity
    android:name=".MainActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />

        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>

    <intent-filter>
        <action android:name="android.intent.action.YUR" />

        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
</activity>
```
进行跳转
```java
Intent intent = new Intent();
intent.setAction("android.intent.action.YUR");
intent.addCategory(Intent.CATEGORY_DEFAULT);
startActivity(intent);
```

### 向下一个Activity发送数据

Intent使用Bundle对象存放待传递的数据信息。
Bundle对象操作各类型数据的读写方法说明见下表。

| 数据类型     | 读方法             | 写方法             |
| ------------ | ------------------ | ------------------ |
| 整型数       | getlnt             | putlnt             |
| 浮点数       | getFloat           | putFloat           |
| 双精度数     | getDouble          | putDouble          |
| 布尔值       | getBoolean         | putBoolean         |
| 字符串       | getString          | putString          |
| 字符串数组   | getStringArray     | putStringArray     |
| 字符串列表   | getStringArrayList | putStringArrayList |
| 可序列化结构 | getSerializable    | putSerializable    |


### 向上一个Activity返回数据

请求类

```java
public class ActRequestActivity extends AppCompatActivity implements View.OnClickListener {

    private String mRequest = "你睡了吗？";
    private ActivityResultLauncher<Intent> register;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_act_request);
        TextView tvRequest = findViewById(R.id.tv_request);
        tvRequest.setText("待发送的消息：" + mRequest);
        findViewById(R.id.btn_request).setOnClickListener(this);
        TextView tvResponse = findViewById(R.id.tv_response);

        register = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
            if (result != null) {
                Intent intent = result.getData();
                if (intent != null && result.getResultCode() == Activity.RESULT_OK) {
                    Bundle bundle = intent.getExtras();
                    String response_time = bundle.getString("response_time");
                    String response_content = bundle.getString("response_content");
                    String desc = String.format("收到返回消息：\n返回时间为%s\n返回内容为%s", response_time, response_content);
                    tvResponse.setText(desc);
                }
            }
        });
    }

    @Override
    public void onClick(View v) {
        Intent intent = new Intent(this, ActResponseActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("request_time", DateUtil.getCurrentTime());
        bundle.putString("request_content", mRequest);
        intent.putExtras(bundle);
        register.launch(intent);
    }
}
```

回应类

```java
public class ActResponseActivity extends AppCompatActivity implements View.OnClickListener {

    private static final String mResponse = "我没睡";

    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_act_response);
        TextView tvRequest = findViewById(R.id.tv_request);
        // 获取上个Activity传的的数据
        Bundle bundle = getIntent().getExtras();
        String request_time = bundle.getString("request_time");
        String request_content = bundle.getString("request_content");
        String desc = String.format("收到请求消息：\n请求时间为%s\n请求内容为%s", request_time, request_content);
        tvRequest.setText(desc);

        findViewById(R.id.btn_response).setOnClickListener(this);

        TextView tvResponse = findViewById(R.id.tv_response);
        tvResponse.setText("待返回的消息：" + mResponse);
    }

    @Override
    public void onClick(View v) {
        Intent intent = new Intent();
        Bundle bundle = new Bundle();
        bundle.putString("response_time", DateUtil.getCurrentTime());
        bundle.putString("response_content", mResponse);
        intent.putExtras(bundle);
        // 携带意图返回上一个页面。RESULT OK表示处理成功
        setResult(Activity.RESULT_OK, intent);
        finish();
    }
}
```

## 为活动补充附加信息


### 利用资源文件配置字符串

示例：

```java
String value = getString(R.string.weather_str);
tv_resource.setText(value);
```

优点： 无需编译，使用灵活。

### 利用元数据传递配置信息

#### 什么是元数据

放在清单文件里的数据

```xml
<activity
    android:name=".MetaDataActivity"
    android:exported="false">
    <meta-data
        android:name="MetaDate"
        android:value="Hello Meta" />
</activity>
```

#### 元数据应用场景

调用第三方SDK是，使用token进行身份验证

#### 获取元数据信息

在Java代码中，获取元数据信息的步骤分为下列三步：
- 调用`getPackageManager`方法获得当前应用的包管理器；
- 调用包管理器的`getActivitylnfo`方法获得当前活动的信息对象；
- 活动信息对象的`metaData`是`Bundle`包裹类型，调用包裹对象的`getString`即可获得指定名称的参数值；

```java
TextView tvMeta = findViewById(R.id.tv_meta);
// 获取应用包管理器
PackageManager pm = getPackageManager();
try {
    // 从应用包管理器中获取当前的活动信息
    ActivityInfo info = pm.getActivityInfo(getComponentName(), PackageManager.GET_META_DATA);
    // 获取活动附加的元数据信息
    Bundle metaData = info.metaData;
    String metaDate = metaData.getString("MetaDate");
    tvMeta.setText(metaDate);
} catch (PackageManager.NameNotFoundException e) {
    e.printStackTrace();
}
```

### 给应用页面注册快捷方式

元数据不仅能传递简单的字符串参数，还能传送更复杂的资源数据，比如实现应用的快捷方式菜单。

**示例：**
清单文件：
```xml
<activity
    android:name=".ButtonClickActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
    <meta-data
        android:name="android.app.shortcuts"
        android:resource="@xml/shortcuts" />
</activity>
```
在res目录下新建xml文件夹，里面新建`shortcuts.xml`，注意所有字符串要在`value/string.xml`文件里注册，

`shortcuts.xml`代码示例：
```xml
<?xml version="1.0" encoding="utf-8"?>
<shortcuts xmlns:android="http://schemas.android.com/apk/res/android">

    <shortcut
        android:enabled="true"
        android:icon="@mipmap/ic_launcher"
        android:shortcutId="first"
        android:shortcutLongLabel="@string/long_1"
        android:shortcutShortLabel="@string/short_1">

        <intent
            android:action="android.intent.action.VIEW"
            android:targetClass="com.yorick.chapter03.ViewGravityActivity"
            android:targetPackage="com.yorick.chapter03" />
        <categories android:name="android.shortcut.conversation" />
    </shortcut>
    <shortcut
        android:enabled="true"
        android:icon="@mipmap/ic_launcher"
        android:shortcutId="second"
        android:shortcutLongLabel="@string/long_2"
        android:shortcutShortLabel="@string/short_2">

        <intent
            android:action="android.intent.action.VIEW"
            android:targetClass="com.yorick.chapter03.GridLayoutActivity"
            android:targetPackage="com.yorick.chapter03" />
        <categories android:name="android.shortcut.conversation" />
    </shortcut>
    <shortcut
        android:enabled="true"
        android:icon="@mipmap/ic_launcher"
        android:shortcutId="third"
        android:shortcutLongLabel="@string/long_3"
        android:shortcutShortLabel="@string/short_3">

        <intent
            android:action="android.intent.action.VIEW"
            android:targetClass="com.yorick.chapter03.RelativeLayoutActivity"
            android:targetPackage="com.yorick.chapter03" />
        <categories android:name="android.shortcut.conversation" />
    </shortcut>
</shortcuts>
```
`string.xml`代码示例：
```xml
<resources>
    <string name="app_name">chapter03</string>
    <string name="hello">Hello,World!</string>
    <string name="short_1">first</string>
    <string name="long_1">重力视图</string>
    <string name="short_2">short</string>
    <string name="long_2">网格视图</string>
    <string name="short_3">third</string>
    <string name="long_3">相对视图</string>
</resources>
```