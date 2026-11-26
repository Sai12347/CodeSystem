class Solution { public int minCostClimbingStairs(int[] c) { int a=0,b=0;for(int x:c){int z=Math.min(a+x,b+x);a=b;b=z;}return Math.min(a,b);} }
