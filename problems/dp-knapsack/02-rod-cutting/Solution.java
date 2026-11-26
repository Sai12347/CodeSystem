class Solution { public int cutRod(int[] p,int n) { int[] d=new int[n+1];for(int len=1;len<=n;len++)for(int k=1;k<=len;k++)d[len]=Math.max(d[len],p[k-1]+d[len-k]);return d[n];} }
