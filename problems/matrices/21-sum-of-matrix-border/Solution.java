class Solution {
    public long sumMatrixBorder(int[][] matrix) {
        int m=matrix.length,n=matrix[0].length;long sum=0;
        for(int r=0;r<m;r++)for(int c=0;c<n;c++)if(r==0||r==m-1||c==0||c==n-1)sum+=matrix[r][c];
        return sum;
    }
}
