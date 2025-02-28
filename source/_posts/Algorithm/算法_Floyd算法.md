---
title: Floyd算法
index_img: /img/default.png
categories: 
  - algorithm
date: 2022-08-14 17:07:41
tags: 
  - Java
  - Floyd
  - Graph
  - 图
  - 最短路径
sticky: 
---

# Floyd算法

## 弗洛伊德(Floyd)算法介绍

（1）和Dijkstra算法一样，弗洛伊德(Floyd)算法也是一种用于寻找给定的加权图中顶点间最短路径的算法。该算法名称以创始人之一、1978年图灵奖获得者、斯坦福大学计算机科学系教授罗伯特·弗洛伊德命名。

（2）弗洛伊德算法(Floyd)计算图中各个顶点之间的最短路径。

（3）迪杰斯特拉算法用于计算图中某一个顶点到其他顶点的最短路径。

（4）弗洛伊德算法VS迪杰斯特拉算法：迪杰斯特拉算法通过选定的被访问顶点，求出从出发访问顶点到其他顶点的最短路径；弗洛伊德算法中每一个顶点都是出发访问点，所以需要将每一个顶点看做被访问顶点，求出从每一个顶点到其他顶点的最短路径。

## 弗洛伊德(Floyd)算法分析

（1）设置顶点vi到顶点vk的最短路径已知为Lik，顶点vk到vj的最短路径已知为Lkj，顶点vi到vj的路径为Lij，则vi到vj的最短路径为: min((Lik+Lkj),Lij)，vk的取值为图中所有顶点，则可获得vi到vj的最短路径

（2）至于vi到vk的最短路径Lik或者k到vj的最短路径Lkj，是以同样的方式获得

```java
import java.util.Arrays;

public class Floyd {
    public static void main(String[] args) {
        char[] vertex = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
        int[][] matrix = new int[vertex.length][vertex.length];
        final int N = 65535; // 表示不可连接
        matrix[0] = new int[]{0, 5, 7, N, N, N, 2};
        matrix[1] = new int[]{5, 0, N, 9, N, N, 3};
        matrix[2] = new int[]{7, N, 0, N, 8, N, N};
        matrix[3] = new int[]{N, 9, N, 0, N, 4, N};
        matrix[4] = new int[]{N, N, 8, N, 0, 5, 4};
        matrix[5] = new int[]{N, N, N, 4, 5, 0, 6};
        matrix[6] = new int[]{2, 3, N, N, 4, 6, 0};
        Graph graph = new Graph(vertex, matrix);
        graph.floyd();
        graph.show();
    }
}

class Graph {
    final private char[] vertex; // 存放顶点的数组
    private int[][] dis; // 保存从各个顶点出发到其他顶点的距离
    private int[][] pre; // 保存前驱结点

    public Graph(char[] vertex, int[][] matrix) {
        this.vertex = vertex;
        this.dis = matrix;
        this.pre = new int[vertex.length][vertex.length];
        for (int i = 0; i < vertex.length; i++) {
            Arrays.fill(pre[i], i);
        }
    }

    public void show() {
        char[] vertex = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
        for (int k = 0; k < dis.length; k++) {
            for (int i = 0; i < pre.length; i++) {
                System.out.print(vertex[pre[k][i]] + "       ");
            }
            System.out.println();
            for (int i = 0; i < dis.length; i++) {
                System.out.print(vertex[k] + "->" + vertex[i] + ":" + dis[k][i] + " ");
            }
            System.out.println();
            System.out.println();
        }
    }

    public void floyd() {
        int len = 0;
        // k为中间结点
        for (int k = 0; k < vertex.length; k++) {
            for (int i = 0; i < vertex.length; i++) {
                for (int j = 0; j < vertex.length; j++) {
                    len = dis[i][k] + dis[k][j];
                    if (len < dis[i][j]) {
                        dis[i][j] = len;
                        pre[i][j] = pre[k][j];
                    }
                }
            }
        }
    }
}
```