class Solution { public int[] singleNumber(int[] a) { int x=0;for(int n:a)x^=n;int bit=x&-x,u=0,v=0;for(int n:a)if((n&bit)!=0)u^=n;else v^=n;return new int[]{u,v}; } }
