---
title: Prim算法
index_img: /img/default.png
categories: 
  - algorithm
date: 2022-08-11 15:15:18
tags: 
  - Java
  - Graph
  - 图
  - 最短路径
sticky: 
---

# Prim算法

- [Prim算法](#prim算法)
  - [应用场景](#应用场景)
  - [最小生成树](#最小生成树)
  - [算法介绍](#算法介绍)
  - [代码实现](#代码实现)

## 应用场景

最短路径问题，给定带权无向连通图，选中尽可能少的线路，使各顶点连通，并且使总路程最小。

也就是最小生成树问题。

## 最小生成树

最小生成树(Minimum CostSpanning Tree)，简称MST。

（1）给定一个带权的无向连通图，如何选取一棵生成树，使树上所有边上权的总和为最小，这叫最小生成树。

（2）N个顶点，一定有N-1条边
（3）包含全部顶点
（4）N-1条边都在图中
（5）求最小生成树的算法主要是普里姆算法和克鲁斯卡尔算法

## 算法介绍

普利姆(Prim)算法求最小生成树，也就是在包含n个顶点的连通图中，找出只有(n-1)条边包含所有n个顶点的连通子图，也就是所谓的极小连通子图。

## 代码实现

```java
public class PrimAlgorithm {
    public static void main(String[] args) {
        char[] data = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
        int verxs = data.length;
        int[][] weight = new int[][]{
                {10000, 5, 7, 10000, 10000, 10000, 2},
                {5, 10000, 10000, 9, 10000, 10000, 3},
                {7, 10000, 10000, 10000, 8, 10000, 10000},
                {10000, 9, 10000, 10000, 10000, 4, 10000},
                {10000, 10000, 8, 10000, 10000, 5, 4},
                {10000, 10000, 10000, 4, 5, 10000, 6},
                {2, 3, 10000, 10000, 4, 6, 10000},
        };
        MGraph graph = new MGraph(verxs);
        MinTree minTree = new MinTree();
        minTree.createGraph(graph, verxs, data, weight);
        minTree.showGraph(graph);
        int distance = minTree.prim(graph, 0);
        System.out.println("最短长度：" + distance);
    }
}

// 创建最小生成树
class MinTree {
    public void createGraph(MGraph graph, int verxs, char[] data, int[][] weight) {
        int i, j;
        for (i = 0; i < verxs; i++) {
            graph.data[i] = data[i];
            for (j = 0; j < verxs; j++) {
                graph.weight[i][j] = weight[i][j];
            }
        }
    }

    public void showGraph(MGraph graph) {
        for (int[] link : graph.weight) {
            System.out.println(Arrays.toString(link));
        }
    }

    public int prim(MGraph graph, int v) {
        int distance = 0;
        int[] visited = new int[graph.verxs];
        visited[v] = 1;
        int h1 = -1;
        int h2 = -1;
        int minWeight = 10000;
        for (int k = 1; k < graph.verxs; k++) {
            // 确定每一次遍历后，和哪个顶点的距离最近
            for (int i = 0; i < graph.verxs; i++) {
                for (int j = 0; j < graph.verxs; j++) {
                    if (visited[i] == 1 && visited[j] == 0 && graph.weight[i][j] < minWeight) {
                        minWeight = graph.weight[i][j];
                        h1 = i;
                        h2 = j;
                    }
                }
            }
            System.out.println("边<" + graph.data[h1] + "," + graph.data[h2] + "> 权值：" + minWeight);
            distance += minWeight;
            visited[h2] = 1;
            minWeight = 10000;
        }
        return distance;
    }
}

class MGraph {
    int verxs; // 表示图的顶点个数
    char[] data; //存放顶点数据
    int[][] weight; // 邻接矩阵存放边的权值

    public MGraph(int verxs) {
        this.verxs = verxs;
        data = new char[verxs];
        weight = new int[verxs][verxs];
    }
}
```