class Solution { public int heightChecker(int[] h) { int[] s=h.clone(); Arrays.sort(s); int c=0; for(int i=0;i<h.length;i++)if(h[i]!=s[i])c++; return c; } }
