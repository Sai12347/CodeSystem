class Solution { public boolean isMonotonic(int[] a) { boolean up=true,down=true; for(int i=1;i<a.length;i++){if(a[i]<a[i-1])up=false;if(a[i]>a[i-1])down=false;} return up||down; } }
