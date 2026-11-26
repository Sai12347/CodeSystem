class Solution {
    public int equalPairs(int[][] grid) {
        int n=grid.length;Map<String,Integer> rows=new HashMap<>();
        for(int[] row:grid){String key=Arrays.toString(row);rows.put(key,rows.getOrDefault(key,0)+1);}
        int answer=0;for(int c=0;c<n;c++){int[] col=new int[n];for(int r=0;r<n;r++)col[r]=grid[r][c];answer+=rows.getOrDefault(Arrays.toString(col),0);}
        return answer;
    }
}
