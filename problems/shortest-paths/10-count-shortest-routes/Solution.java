class Solution {
    public int countShortestRoutes(int n, int[][] roads) {
        int mod = 1000000007; List<int[]>[] graph = new ArrayList[n]; for (int i=0;i<n;i++) graph[i]=new ArrayList<>();
        for (int[] e:roads) { graph[e[0]].add(new int[]{e[1],e[2]}); graph[e[1]].add(new int[]{e[0],e[2]}); }
        long[] dist = new long[n]; Arrays.fill(dist,Long.MAX_VALUE); int[] ways = new int[n]; dist[0]=0; ways[0]=1;
        PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(a->a[0])); pq.offer(new long[]{0,0});
        while(!pq.isEmpty()) { long[] cur=pq.poll(); long d=cur[0]; int u=(int)cur[1]; if(d!=dist[u]) continue; for(int[] e:graph[u]) { int v=e[0]; long nd=d+e[1]; if(nd<dist[v]) { dist[v]=nd; ways[v]=ways[u]; pq.offer(new long[]{nd,v}); } else if(nd==dist[v]) ways[v]=(int)(((long)ways[v]+ways[u])%mod); } }
        return ways[n-1];
    }
}
