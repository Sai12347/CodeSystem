class Solution {
    public boolean checkXMatrix(int[][] matrix) {
        int n=matrix.length;
        for(int r=0;r<n;r++)for(int c=0;c<n;c++){boolean diagonal=r==c||r+c==n-1;if(diagonal==(matrix[r][c]==0))return false;}
        return true;
    }
}
