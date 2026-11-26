class Solution {
    public long[] bellmanFord(int n, int[][] edges, int source) {
        long inf=Long.MAX_VALUE/4; long[] d=new long[n]; Arrays.fill(d,inf); d[source]=0;
        for(int pass=0;pass<n-1;pass++){boolean changed=false;for(int[] e:edges)if(d[e[0]]!=inf&&d[e[0]]+e[2]<d[e[1]]){d[e[1]]=d[e[0]]+e[2];changed=true;}if(!changed)break;}
        for(int i=0;i<n;i++)if(d[i]==inf)d[i]=-1; return d;
    }
}
