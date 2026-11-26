class Solution {
    public long minimumCostWithDiscount(int n, int[][] edges, int source, int destination) {
        List<long[]>[] g=new ArrayList[n]; for(int i=0;i<n;i++)g[i]=new ArrayList<>();
        for(int[] e:edges){g[e[0]].add(new long[]{e[1],e[2]});g[e[1]].add(new long[]{e[0],e[2]});}
        long[][] d=new long[n][2]; for(long[] row:d)Arrays.fill(row,Long.MAX_VALUE); d[source][0]=0; PriorityQueue<long[]> pq=new PriorityQueue<>(Comparator.comparingLong(a->a[0])); pq.offer(new long[]{0,source,0});
        while(!pq.isEmpty()){long[] c=pq.poll();long cost=c[0];int u=(int)c[1],used=(int)c[2];if(cost!=d[u][used])continue;if(u==destination)return cost;for(long[] e:g[u]){int v=(int)e[0];long w=e[1];if(cost+w<d[v][used]){d[v][used]=cost+w;pq.offer(new long[]{cost+w,v,used});}if(used==0&&cost+w/2<d[v][1]){d[v][1]=cost+w/2;pq.offer(new long[]{cost+w/2,v,1});}}}
        return -1;
    }
}
