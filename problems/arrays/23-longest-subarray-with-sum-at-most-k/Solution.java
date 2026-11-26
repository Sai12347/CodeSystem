class Solution { public int longestSubarrayAtMostK(int[] a,long k) { int l=0,best=0;long sum=0;for(int r=0;r<a.length;r++){sum+=a[r];while(sum>k)sum-=a[l++];best=Math.max(best,r-l+1);}return best;} }
