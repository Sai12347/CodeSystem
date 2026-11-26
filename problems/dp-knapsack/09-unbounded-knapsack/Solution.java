class Solution { public int unboundedKnapsack(int[]w,int[]v,int c){int[]d=new int[c+1];for(int i=0;i<w.length;i++)for(int x=w[i];x<=c;x++)d[x]=Math.max(d[x],d[x-w[i]]+v[i]);return d[c];} }
