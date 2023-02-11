---
title: Kruskal算法
index_img: /img/default.png
categories: 
  - algorithm
date: 2022-08-12 15:41:56
tags: 
  - Java
  - 树
  - Tree
  - 图
  - Graph
sticky: 
---

# Kruskal算法

## 基本介绍

（1）克鲁斯卡尔(Kruskal)算法，是用来求加权连通图的最小生成树的算法。

（2）基本思想：按照权值从小到大的顺序选择n-1条边，并保证这n-1条边不构成回路。

（3）具体做法：首先构造一个只含n个顶点的森林，然后依权值从小到大从连通网中选择边加入到森林中，并使森林中不产生回路，直至森林变成一棵树为止。

## 算法分析

根据前面介绍的克鲁斯卡尔算法的基本思想和做法，我们能够了解到，克鲁斯卡尔算法重点需要解决的以下两个问题：

**问题一**：对图的所有边按照权值大小进行排序。
**问题二**：将边添加到最小生成树中时，怎么样判断是否形成了回路。

问题一很好解决，采用排序算法进行排序即可。

问题二的处理方式是记录顶点在"最小生成树"中的终点，顶点的终点是"在最小生成树中与它连通的最大顶点"。然后每次需要将一条边添加到最小生存树时，判断该边的两个顶点的终点是否重合，重合的话则会构成回路。

关于终点的说明：
就是将所有顶点按照从小到大的顺序排列好之后，某个顶点的终点就是"与它连通的最大顶点"。

## 应用案例

克鲁斯卡尔最佳实践-公交站问题

（1）有北京有新增7个站点(A,B,C, D,E,F,G)，现在需要修路把7个站点连通。

（2）各个站点的距离用边线表示(权)，比如A-B距离12公里

（3）问：如何修路保证各个站点都能连通，并且总的修建公路总里程最短？

## 代码实现

```java
public class KruskalCase {
    private int edgeNum;
    final private char[] vertexes;
    final private int[][] matrix;
    private static final int INF = Integer.MAX_VALUE;// 表示两个顶点不能连通

    public static void main(String[] args) {
        char[] vertexes = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
        int[][] matrix = {
                {0, 12, INF, INF, INF, 16, 14},
                {12, 0, 10, INF, INF, 7, INF},
                {INF, 10, 0, 3, 5, 6, INF},
                {INF, INF, 3, 0, 4, INF, INF},
                {INF, INF, 5, 4, 0, 2, 8},
                {16, 7, 6, INF, 2, 0, 9},
                {14, INF, INF, INF, 8, 9, 0},
        };
        KruskalCase kruskalCase = new KruskalCase(vertexes, matrix);
        kruskalCase.print();
        kruskalCase.kruskal();
    }

    public KruskalCase(char[] vertexes, int[][] matrix) {
        this.vertexes = vertexes;
        this.matrix = matrix;
        for (int i = 0; i < vertexes.length; i++) {
            for (int j = i + 1; j < vertexes.length; j++) {
                if (this.matrix[i][j] != INF) {
                    edgeNum++;
                }
            }
        }
    }

    public void kruskal() {
        int index = 0; // 最后结果数组的索引
        int[] ends = new int[vertexes.length]; // 各个顶点的终点
        // 结构数组
        Edge[] res = new Edge[edgeNum];
        Edge[] edges = getEdges();
        sortEdges(edges);
        for (int i = 0; i < edgeNum; i++) {
            int p1 = getPos(edges[i].start);
            int p2 = getPos(edges[i].end);
            int m = getEnd(ends, p1);
            int n = getEnd(ends, p2);
            if (m != n) {
                ends[m] = n;
                res[index] = edges[i];
                index++;
            }

        }
        for (int i = 0; i < index; i++) {
            System.out.println(res[i]);
        }
    }


    public void print() {
        System.out.println("邻接矩阵为：");
        for (int i = 0; i < vertexes.length; i++) {
            for (int j = 0; j < vertexes.length; j++) {
                System.out.printf("%10d\t", matrix[i][j]);
            }
            System.out.println();
        }
    }

    // 对边进行冒泡排序
    private void sortEdges(Edge[] edges) {
        for (int i = 0; i < edges.length - 1; i++) {
            for (int j = 0; j < edges.length - 1 - i; j++) {
                if (edges[j].weight > edges[j + 1].weight) {
                    Edge temp = edges[j];
                    edges[j] = edges[j + 1];
                    edges[j + 1] = temp;
                }
            }
        }
    }

    private int getPos(char c) {
        for (int i = 0; i < vertexes.length; i++) {
            if (vertexes[i] == c) {
                return i;
            }
        }
        return -1;
    }

    private Edge[] getEdges() {
        int index = 0;
        Edge[] edges = new Edge[edgeNum];
        for (int i = 0; i < vertexes.length; i++) {
            for (int j = i + 1; j < vertexes.length; j++) {
                if (this.matrix[i][j] != INF) {
                    edges[index] = new Edge(vertexes[i], vertexes[j], matrix[i][j]);
                    index++;
                }
            }
        }
        return edges;
    }

    /**
     * 获取下标为i的顶点的终点，用于后面判断两个顶点的终点是否重合
     *
     * @param ends 记录各个顶点对应的终点，在遍历过程中逐步形成
     * @param i    顶点下标
     * @return 下标为i的顶点的终点的下标
     */
    private int getEnd(int[] ends, int i) {
        while (ends[i] != 0) {
            i = ends[i];
        }
        return i;
    }
}

class Edge {
    char start;
    char end;
    int weight;

    public Edge(char start, char end, int weight) {
        this.start = start;
        this.end = end;
        this.weight = weight;
    }

    @Override
    public String toString() {
        return "Edge{" +
                "start=" + start +
                ", end=" + end +
                ", weight=" + weight +
                '}';
    }
}
```
输出：
```java
邻接矩阵为：
         0	        12	2147483647	2147483647	2147483647	        16	        14	
        12	         0	        10	2147483647	2147483647	         7	2147483647	
2147483647	        10	         0	         3	         5	         6	2147483647	
2147483647	2147483647	         3	         0	         4	2147483647	2147483647	
2147483647	2147483647	         5	         4	         0	         2	         8	
        16	         7	         6	2147483647	         2	         0	         9	
        14	2147483647	2147483647	2147483647	         8	         9	         0	
Edge{start=E, end=F, weight=2}
Edge{start=C, end=D, weight=3}
Edge{start=D, end=E, weight=4}
Edge{start=B, end=F, weight=7}
Edge{start=E, end=G, weight=8}
Edge{start=A, end=B, weight=12}
```