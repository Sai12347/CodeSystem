class Solution { public int[] stableParityPartition(int[] a) { int[] r=new int[a.length];int k=0;for(int x:a)if(x%2==0)r[k++]=x;for(int x:a)if(x%2!=0)r[k++]=x;return r;} }
