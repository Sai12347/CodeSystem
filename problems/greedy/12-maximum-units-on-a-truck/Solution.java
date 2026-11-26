class Solution { public int maximumUnits(int[][] a,int t) { Arrays.sort(a,(x,y)->Integer.compare(y[1],x[1])); int s=0; for(int[] b:a){int k=Math.min(t,b[0]);s+=k*b[1];t-=k;if(t==0)break;}return s;} }
