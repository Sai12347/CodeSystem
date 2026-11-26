class Solution { public int combinationSum4(int[] a,int t) { int[] d=new int[t+1];d[0]=1;for(int s=1;s<=t;s++)for(int x:a)if(x<=s)d[s]+=d[s-x];return d[t];} }
