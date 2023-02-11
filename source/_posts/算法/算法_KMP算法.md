---
title: KMP算法
index_img: /img/default.png
categories: 
  - algorithm
date: 2022-08-09 16:18:52
tags: 
  - Java
  - KMP
sticky: 
---

# KMP算法

## 暴力匹配算法

如果用暴力匹配的思路，并假设现在str1匹配到i位置，子串str2匹配到j位置，则有：

（1）如果当前字符匹配成功，即`str1[i] == str2[i]`，则`i++,j++`，继续匹配下一个字符

（2）如果失败，即`str1[i] != str2[j]`，令`i=i-(j-1),j=0`。相当于每次匹配失败时，i回溯，j被置为0。

（3）用暴力方法解决的话就会有大量的回溯，每次只移动一位，若是不匹配，移动到下一位接着判断，浪费了大量的时间。(不可行!)

## 暴力匹配算法实现

```java
public class ViolenceMatch {
    public static void main(String[] args) {
        String str1 = "你好啥时候回啊";
        String str2 = "啥时候回";
        int index = violenceMatch(str1, str2);
        System.out.println(index);
    }

    // 暴力匹配
    public static int violenceMatch(String str1, String str2) {
        char[] s1 = str1.toCharArray();
        char[] s2 = str2.toCharArray();

        int i = 0;
        int j = 0;
        while (i < s1.length && j < s2.length) {
            // 保证匹配时，不越界
            if (s1[i] == s2[j]) {
                i++;
                j++;
            } else {
                i = i - (j - 1);
                j = 0;
            }
        }
        if (j == str2.length()) {
            return i - j;
        }
        return -1;
    }
}
```

## KMP算法介绍

（1）KMP是一个解决模式串在文本串是否出现过，如果出现过，最早出现的位置的经典算法。

（2）Knuth-Morris-Pratt字符串查找算法，简称为“KMP算法”，常用于在一个文本串s内查找一个模式串P的出现位置，这个算法由Donald Knuth、Vaughan Pratt、James H. Morris三人于1977年联合发表，故取这3人的姓氏命名此算法。

（3）KMP方法算法就利用之前判断过信息，通过一个next数组，保存模式串中前后最长公共子序列的长度，每次回溯时，通过next数组找到，前面匹配过的位置，省去了大量的计算时间。

## KMP算法思路


“部分匹配值”就是”前缀”和”后缀”的最长的共有元素的长度。以“ABCDABD”为例：

- “A”的前缀和后缀都为空集,共有元素的长度为0;
- “AB”的前缀为[A]，后缀为[B]，共有元素的长度为0;
- “ABC”的前缀为[A,AB]，后缀为[BC,C]，共有元素的长度0;
- “ABCD”的前缀为[A,AB,ABC]，后缀为[BCD,CD,D]，共有元素的长度为0;
- “ABCDA”的前缀为[A,AB,ABC,ABCD]，后缀为[BCDA,CDA,DA,A]，共有元素为”A”，长度为1;
- “ABCDAB”的前缀为[A,AB,ABC,ABCD,ABCDA]，后缀为[BCDAB,CDAB,DAB,AB,B]，共有元素为”AB”，长度为2;
- “ABCDABD”的前缀为[A,AB,ABC,ABCD,ABCDA,ABCDAB]，后缀为[BCDABD,CDABD,DABD,ABD,BD,D],共有元素的长度为0。

（1）先得到子串的部分匹配表

（2）使用部分匹配表完成KMP匹配

移动位数 = 已匹配的字符数 – 对应的部分匹配值

### KMP算法实现

```java
public class KMP {
    public static void main(String[] args) {
        String str1 = "BBC ABCDAB ABCDABCDABDE";
        String str2 = "ABCDABD";

        int[] next = kmpNext(str2);
        System.out.println(Arrays.toString(next));
        int index = kmpSearch2(str1, str2, next);
        System.out.println(index);
    }

    /** 第一种
     * @param str1 源字符串
     * @param str2 子串
     * @param next 部分匹配表
     * @return -1表示未匹配到，否则返回第一次出现的下标
     */
    public static int kmpSearch(String str1, String str2, int[] next) {
        for (int i = 1, j = 0; i < str1.length(); i++) {
            // 核心！
            while (j > 0 && str1.charAt(i) != str2.charAt(j)) {
                j = next[j - 1];
            }
            if (str1.charAt(i) == str2.charAt(j)) {
                j++;
            }
            if (j == str2.length()) {
                return i - j + 1;
            }
        }
        return -1;
    }

    /** 第二种
     * @param str1 源字符串
     * @param str2 子串
     * @param next 部分匹配表
     * @return -1表示未匹配到，否则返回第一次出现的下标
     */
    public static int kmpSearch2(String str1, String str2, int[] next) {
        char[] s1 = str1.toCharArray();
        char[] s2 = str2.toCharArray();

        int i = 0;
        int j = 0;
        while (i < s1.length && j < s2.length) {
            // 保证匹配时，不越界
            if (s1[i] == s2[j]) {
                i++;
                j++;
            } else {
                if (j - 1 < 0) {
                    i = i - (j - 1);
                } else {
                    i = i - next[j - 1];
                    j = 0;
                }
            }
        }
        if (j == str2.length()) {
            return i - j;
        }
        return -1;
    }

    // 获取部分匹配表
    public static int[] kmpNext(String dest) {
        int[] next = new int[dest.length()];
        // 字符串长度为1，部分匹配值为0
        next[0] = 0;
        for (int i = 1, j = 0; i < dest.length(); i++) {
            // 核心！
            while (j > 0 && dest.charAt(i) != dest.charAt(j)) {
                j = next[j - 1];
            }
            if (dest.charAt(i) == dest.charAt(j)) {
                j++;
            }
            next[i] = j;
        }
        return next;
    }
}
```