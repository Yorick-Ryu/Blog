---
title: Dijkstra算法
index_img: /img/default.png
categories: 
  - algorithm
date: 2022-08-13 15:14:27
tags: 
  - Java
  - Dijkstra
  - Graph
  - 图
  - 最短路径
sticky: 
---

# 迪杰斯特拉(Dijkstra)算法


## 基本介绍

迪杰斯特拉(Dijkstra)算法是典型最短路径算法，用于计算一个结点到其他结点的最短路径。它的主要特点是以起始点为中心向外层层扩展(广度优先搜索思想)，直到扩展到终点为止。

## 实现思路

设置出发顶点为v，顶点集合V{v1,v2,vi...}，v到V中各顶点的距离构成距离集合Dis，Dis{d1,d2,di...}]，Dis集合记录着v到图中各顶点的距离(到自身可以看作0，v到vi距离对应为di)

（1）从Dis中选择值最小的di并移出Dis集合，同时移出V集合中对应的顶点vi，此时的v到vi即为最短路径

（2）更新Dis集合，更新规则为：比较v到V集合中顶点的距离值，与v通过vi到v集合中顶点的距离值，保留值较小的一个(同时也应该更新顶点的前驱节点为vi，表明是通过vi到达的)

（3）重复执行两步骤，直到最短路径顶点为目标顶点即可结束


## 代码实现

```java
import java.util.Arrays;

public class Dijkstra {
    public static void main(String[] args) {
        char[] vertex = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
        int[][] matrix = new int[vertex.length][vertex.length];
        final int N = 65535; // 表示不可连接
        matrix[0] = new int[]{N, 5, 7, N, N, N, 2};
        matrix[1] = new int[]{5, N, N, 9, N, N, 3};
        matrix[2] = new int[]{7, N, N, N, 8, N, N};
        matrix[3] = new int[]{N, 9, N, N, N, 4, N};
        matrix[4] = new int[]{N, N, 8, N, N, 5, 4};
        matrix[5] = new int[]{N, N, N, 4, 5, N, 6};
        matrix[6] = new int[]{2, 3, N, N, 4, 6, N};
        Graph graph = new Graph(vertex, matrix);
        graph.showGraph();
        graph.dijkstra(6);
    }
}

class Graph {
    final private char[] vertex;
    public int[][] matrix;
    private VisitedVertex vv;

    public Graph(char[] vertex, int[][] matrix) {
        this.vertex = vertex;
        this.matrix = matrix;
    }

    // 显示图
    public void showGraph() {
        for (int[] link : matrix) {
            System.out.println(Arrays.toString(link));
        }
    }

    public void dijkstra(int index) {
        vv = new VisitedVertex(vertex.length, index);
        for (int j = 0; j < vertex.length; j++) {
            index = vv.updateArr();
            update(index);
        }
        System.out.println(vv);
    }


    // 更新index下标顶点到周围顶点的距离和周结点的前驱结点
    public void update(int index) {
        int len;
        vv.visited[index] = 1;
        for (int j = 0; j < matrix[index].length; j++) {
            //len含义是;出发顶点到index顶点的距离＋从index顶点到j顶点的距离的和
            len = vv.getDis(index) + matrix[index][j];
            // 如果j顶点没有被访问过，并且 len小于出发顶点到j顶点的距离，就需要更新
            if (!vv.in(j) && len < vv.getDis(j)) {
                vv.updatePre(j, index);
                vv.updateDis(j, len);
            }
        }
    }
}

class VisitedVertex {
    public int[] visited;
    public int[] pre;
    public int[] dis;

    public VisitedVertex(int length, int index) {
        this.visited = new int[length];
        this.pre = new int[length];
        this.dis = new int[length];
        Arrays.fill(dis, 65535);
        this.dis[index] = 0;
    }

    // 判断结点是否被访问过
    public boolean in(int index) {
        return visited[index] == 1;
    }

    // 更新到index距离
    public void updateDis(int index, int len) {
        dis[index] = len;
    }

    // 更新pre的前驱结点为index
    public void updatePre(int pre, int index) {
        this.pre[pre] = index;
    }

    // 返回出发结点到index的距离
    public int getDis(int index) {
        return dis[index];
    }

    public int updateArr() {
        int min = 65535, index = 0;
        for (int i = 0; i < visited.length; i++) {
            if (visited[i] == 0 && dis[i] < min) {
                min = dis[i];
                index = i;
            }
        }
        return index;
    }

    @Override
    public String toString() {
        return "VisitedVertex{" +
                "visited=" + Arrays.toString(visited) +
                ", pre=" + Arrays.toString(pre) +
                ", dis=" + Arrays.toString(dis) +
                '}';
    }
}
```

