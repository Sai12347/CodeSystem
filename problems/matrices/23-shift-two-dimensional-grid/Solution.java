class Solution {
    public int[][] shiftGrid(int[][] grid, int k) {
        int m=grid.length,n=grid[0].length,size=m*n,shift=k%size;int[][] out=new int[m][n];
        for(int i=0;i<size;i++){int from=(i-shift+size)%size;out[i/n][i%n]=grid[from/n][from%n];}
        return out;
    }
}
