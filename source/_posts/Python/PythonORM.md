---
title: Python编写ORM框架
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-15 16:17:04
tags: 
  - ORM
  - sql
sticky: 
---

# Python编写ORM框架

ORM全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表，这样，写代码更简单，不用直接操作SQL语句。

要编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来。

首先来定义Field类，它负责保存数据库表的字段名和字段类型：
```py
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    # __str__方法，重写print()函数返回值
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
```
在Field的基础上，进一步定义各种类型的Field，比如StringField，IntegerField等等：
```py
class StringField(Field):

    def __init__(self, name):
        # 用super()调用父类方法
        super().__init__(name, 'varchar(100)')

class IntegerField(Field):

    def __init__(self, name):
        super().__init__(name, 'bigint')
```
下一步，就是编写最复杂的ModelMetaclass了：
```py
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # attrs是一个字典，包含Model类及其子类的所有属性
        # 排除掉对Model类的修改，只修改其子类
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        # 筛选出Field属性或其子类
        for k,v in attrs.items():
            if isinstance(v,Field):
                print("Found mapping: %s ==> %s" % (k,v))
                mappings[k] = v
        # 从子类属性中删除该Field属性，子类属性会覆盖自动生成的属性
        for k in mappings.keys():
            attrs.pop(k)
        # 为Model的子类添加新属性
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)
```
然后，编写User类的基类Model
```py
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    # 把一个类的所有属性和方法调用全部动态化处理
    def __getattr__(self, key):
        try:
            # self已经是一个dict
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 生成实例化对象时调用
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name) # 等同于fields.append(k)
            params.append('?')
            # None这一位参数表示如果拿不到参数k，自动返回None
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))
```
最后定义User类
```py
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
```
测试：
```py
# 创建一个实例：
u = User(id=12345, name='Yorick', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()
```
输出：
```py
Found model: User
Found mapping: id ==> <IntegerField:id>
Found mapping: name ==> <StringField:username>
Found mapping: email ==> <StringField:email>
Found mapping: password ==> <StringField:password>
SQL: insert into User (id,username,email,password) values (?,?,?,?)
ARGS: [12345, 'Yorick', 'test@orm.org', 'my-pwd']
```

完整代码：
```python
class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, "varchar(100)")


class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, "bigint")


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 排除掉对Model类的修改，只修改其子类
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        # 查找Field属性
        for k,v in attrs.items():
            if isinstance(v,Field):
                print("Found mapping: %s ==> %s" % (k,v))
                mappings[k] = v
        # 从类属性中删除该Field属性
        for k in mappings.keys():
            attrs.pop(k)
        # 为Model的子类添加新属性
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)
        
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    # 把一个类的所有属性和方法调用全部动态化处理
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 生成实例化对象时调用
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name) # 等同于fields.append(k)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建一个实例：
u = User(id=12345, name='Yorick', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()
```