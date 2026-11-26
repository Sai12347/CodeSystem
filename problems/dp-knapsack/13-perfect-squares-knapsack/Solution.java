class Solution { public int numSquares(int n){int[]d=new int[n+1];Arrays.fill(d,n+1);d[0]=0;for(int x=1;x*x<=n;x++)for(int s=x*x;s<=n;s++)d[s]=Math.min(d[s],d[s-x*x]+1);return d[n];} }
