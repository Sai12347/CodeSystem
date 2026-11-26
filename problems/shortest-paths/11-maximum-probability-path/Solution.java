class Solution {
    public double maxProbability(int n, int[][] edges, double[] succProb, int start, int end) {
        List<double[]>[] graph=new ArrayList[n]; for(int i=0;i<n;i++) graph[i]=new ArrayList<>();
        for(int i=0;i<edges.length;i++){int u=edges[i][0],v=edges[i][1]; graph[u].add(new double[]{v,succProb[i]}); graph[v].add(new double[]{u,succProb[i]});}
        double[] best=new double[n]; best[start]=1.0; PriorityQueue<double[]> pq=new PriorityQueue<>((a,b)->Double.compare(b[0],a[0])); pq.offer(new double[]{1.0,start});
        while(!pq.isEmpty()){double[] cur=pq.poll(); double p=cur[0]; int u=(int)cur[1]; if(p<best[u])continue; if(u==end)return p; for(double[] e:graph[u]){int v=(int)e[0]; double cand=p*e[1]; if(cand>best[v]){best[v]=cand;pq.offer(new double[]{cand,v});}}}
        return 0.0;
    }
}
