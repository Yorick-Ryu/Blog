---
title: python复习题
tags:
  - 复习
index_img: /img/default.png
categories:
  - Python
date: 2023-02-17 15:27:11
sticky:
---

# Python复习题

1、用if分支结构完成程序设计(三选一):

- 输入成绩，查询等级(90分及以上优秀、60-89合格、低于60不合格)
  ```python
  score = int(input("Scroe:"))
  
  if score >= 90 and score <= 100:
      print("优秀")
  elif score >= 60 and score < 90:
      print("合格")
  elif score >= 0 and score < 60:
      print("不合格")
  else:
      print("Score must in 0-100")
  ```
  
- 输入年龄，查询公园门票价格(70岁以上老人免票，18岁以下儿童及60岁以上半票，18岁以上全价)

  ```python
  while(True):
      age = input("请输入年龄：")
      age = float(age)
      if age >= 70:
          print("免票")
      elif 60 < age < 70 or 0 < age < 18:
          print("半票")
      elif 18 <= age <= 60:
          print("全价")
      else:
          print("年龄不合法")
  ```

- 输入身高、体重，查询健康情况(BMI=体重(kg) /身高(m)的平方低于18.5偏瘦; 18.5-24 正常，超过24偏胖，超过28肥胖)

  ```python
  # 输入身高、体重
  height = input("请输入身高（cm）：")
  weight = input("请输入体重（kg）：")
  # 查询健康
  # BMI = 体重（kg）/ 身高（m）的平方
  BMI = float(weight) / (float(height)/100)**2
  # 低于18.5 偏瘦
  if BMI < 18.5:
      print("偏瘦")
  # 18.5-24 正常
  elif 18.5 <= BMI <= 24:
      print("正常")
  # 超过24偏胖
  elif 24 < BMI <= 28:
      print("偏胖")
  # 超过28肥胖
  elif BMI > 28:
      print("肥胖")
  
  ```

2、编程完成(三选一)：

- 求1-100范围内所有3的倍数的和。如3+6+9+...

  ```python
  sum = 0
  for i in range(1, 101):
      if i % 3 == 0:
          sum += i
  print("result:" , sum)
  ```

- 一个数如果恰好等于它的因子(不包含自身)之和，则称之为"完数"。 例如6=1+2+3。编程找出100以内的所有完数并输出。

  ```python
  for i in range(0, 101):
      sum = 0
      for n in range(1, i):
          if i % n == 0:
              sum += n
      if(i == sum):
          print(i)
  # 0 6 28
  ```

- 输出100以内的质数

  ```python
  for i in range(2,100):
      num = 0
      for j in range(2, i):
          if i % j == 0:
              num += 1
      if num == 0:
          print(i)
      num = 0
  # 25个
  ```

3、编程完成(三选一)：

- 己知字符串s= 'AbcDeFGhIJkmN'， 请计算该字符串中小写字母的数量。
  ```python
  num = 0
  for i in s:
      if i.islower():
          num += 1
  
  print(num) # 7
  ```

-  检查字符串"Life is short. I use python."中是否包含字符串"python"，若包含则替换为 "Python"后输出新字符串，否则输出原字符串。

  ```python
  s = "Life is short. I use python"
  
  if s.find("python"):
      print(s.replace("python", "Python"))
  else:
      print(s)
  ```

- 把“HAPPY BIRTHDAY”改成“Happy Birthday” 并输出。

  ```python
  s = "HAPPY BIRTHDAY"
  print(s.title())
  # Happy Birthday
  ```

4、编程实现(三选一)：
定义一个三角形类，输入三条边，判断能否构成三角形，如果能，计算并输出三角
形的面积，否则返回0。假设三角形三条边分别为a、 b、c，则周长的一半s=(a+ b
+c)/2，面积area=√s\*(s-a)\*(s-b)*(s-c)。

```python
class triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def canTri(self, a, b, c) -> bool:
        return a + b > c and b + c > a and a + c > b

    def getS(self, a, b, c) -> float:
        return (a + b + c) / 2

    def getArea(self, a, b, c) -> float:
        s = self.getS(a, b, c)
        return pow(s * (s - a) * (s - b) * (s - c), 0.5)

    def getRes(self) -> float:
        if self.canTri(self.a, self.b, self.c):
            return self.getArea(self.a, self.b, self.c)
        else:
            return 0

tri = triangle(3, 4, 5)
print(tri.getRes())
```

5、逄7拍手游戏

```python
for i in range(1, 100):
    if i % 7 == 0 or "7" in str(i):
        print(i)
# 30 次
```

6、菲波拉契数列前15项，例如: 0 1 1 2 3 5 8 13 21 ... (递归兔子序列)

```python
def sum(a):
    if a == 0:
        return 0
    if a == 1:
        return 1
    else:
        return sum(a - 1) + sum(a - 2)

for i in range(15):
    print(sum(i))
```

7、重写加减乘除运算符合

```python
class MyNumber:
    def __init__(self, v) -> None:
        self.data = v

    def __add__(self, other):
        v = self.data + other.data
        return MyNumber(v)

    def __sub__(self, other):
        v = self.data - other.data
        return MyNumber(v)

    def __mul__():
        pass

    def __div__():
        pass


n1 = MyNumber(100)
n2 = MyNumber(200)

print((n1-n2).data) # -100
```

9、重写两个点坐标的比较符

```python
"""
比较算术运算符的重载:
        方法名                  运算符和表达式      说明
        __lt__(self,rhs)       self < rhs        小于
        __le__(self,rhs)       self <= rhs       小于等于
        __gt__(self,rhs)       self > rhs        大于
        __ge__(self,rhs)       self >= rhs       大于等于
        __eq__(self,rhs)       self == rhs       等于
        __ne__(self,rhs)       self != rhs       不等于
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __lt__(self, p):
        return ((pow(self.x, 2) + pow(self.y, 2)) - (pow(p.x, 2) + pow(p.y, 2))) < 0

    def printIt(self):
        print(f"({self.x},{self.y})")


p1 = Point(3, 4)
p2 = Point(1, 2)

p3 = p1 + p2
p4 = p1 - p2
p3.printIt()   # (4,6)
p4.printIt()   # (2,2)
print(p1 < p2) # False
```

10、编程，为二次方程式ax2+bx+c=0设计一个名Equation 的类，判别方程有无实数解，并求解。

```python
class Equation(object):
    def __init__(self, a, b, c):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    def getDiscriminant(self):
        return pow(self.b, 2) - 4 * self.a * self.c

    def getRoot1(self):
        if self.getDiscriminant() < 0:
            print("判别式小于0")
            return 0
        return (-self.b + pow(self.getDiscriminant(), 0.5)) / 2 * self.a

    def getRoot2(self):
        if self.getDiscriminant() < 0:
            print("判别式小于0")
            return 0
        return (-self.b - pow(self.getDiscriminant(), 0.5)) / 2 * self.a


a = input("输入二次项系数")
b = input("输入一次项系数")
c = input("输入常数项系数")
equation = Equation(a, b, c)
print(f"判别式结果为：{equation.getDiscriminant()}")
print(f"第一个根为：{equation.getRoot1()}")
print(f"第二个根为：{equation.getRoot2()}")
```

