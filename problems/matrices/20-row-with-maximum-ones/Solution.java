class Solution {
    public int rowWithMaximumOnes(int[][] mat) {
        int best=-1,bestCount=0;
        for(int r=0;r<mat.length;r++){int count=0;for(int x:mat[r])count+=x;if(count>bestCount){bestCount=count;best=r;}}
        return best;
    }
}
