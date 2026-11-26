class Solution {
    public int[] minimumReversalsFromSource(int n, int[][] directedEdges, int source) {
        List<int[]>[] g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();
        for(int[] e:directedEdges){g[e[0]].add(new int[]{e[1],0});g[e[1]].add(new int[]{e[0],1});}
        int inf=1000000000;int[] d=new int[n];Arrays.fill(d,inf);d[source]=0;PriorityQueue<int[]> pq=new PriorityQueue<>(Comparator.comparingInt(a->a[0]));pq.offer(new int[]{0,source});
        while(!pq.isEmpty()){int[] c=pq.poll();int cost=c[0],u=c[1];if(cost!=d[u])continue;for(int[] e:g[u])if(cost+e[1]<d[e[0]]){d[e[0]]=cost+e[1];pq.offer(new int[]{d[e[0]],e[0]});}}
        for(int i=0;i<n;i++)if(d[i]==inf)d[i]=-1;return d;
    }
}
