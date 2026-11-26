class Solution { public int maxAdjacentDiff(int[] a) { int best=0; for(int i=1;i<a.length;i++)best=Math.max(best,(int)Math.abs((long)a[i]-a[i-1])); return best; } }
