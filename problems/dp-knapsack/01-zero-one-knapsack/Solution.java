class Solution { public int knapSack(int[] w,int[] v,int c) { int[] d=new int[c+1];for(int i=0;i<w.length;i++)for(int x=c;x>=w[i];x--)d[x]=Math.max(d[x],d[x-w[i]]+v[i]);return d[c];} }
