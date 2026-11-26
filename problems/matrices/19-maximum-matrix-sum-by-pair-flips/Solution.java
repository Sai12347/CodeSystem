class Solution {
    public long maxMatrixSum(int[][] matrix) {
        long total=0;int negatives=0;int smallest=Integer.MAX_VALUE;
        for(int[] row:matrix)for(int x:row){total+=Math.abs((long)x);smallest=Math.min(smallest,Math.abs(x));if(x<0)negatives++;}
        return total-(negatives%2==1?2L*smallest:0);
    }
}
