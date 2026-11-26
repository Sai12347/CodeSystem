class Solution {
    public int numSpecial(int[][] mat) {
        int m=mat.length,n=mat[0].length;int[] rs=new int[m],cs=new int[n];
        for(int r=0;r<m;r++)for(int c=0;c<n;c++){rs[r]+=mat[r][c];cs[c]+=mat[r][c];}
        int count=0;for(int r=0;r<m;r++)for(int c=0;c<n;c++)if(mat[r][c]==1&&rs[r]==1&&cs[c]==1)count++;
        return count;
    }
}
