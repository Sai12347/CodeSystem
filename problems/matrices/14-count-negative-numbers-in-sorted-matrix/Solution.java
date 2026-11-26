class Solution { public int countNegatives(int[][] g) { int n=0; for(int[] row:g)for(int x:row)if(x<0)n++; return n; } }
