class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        List<int[]> merged = new ArrayList<>();
        int curStart = intervals[0][0];
        int curEnd = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= curEnd) {
                curEnd = Math.max(curEnd, intervals[i][1]);
            } else {
                merged.add(new int[]{curStart, curEnd});
                curStart = intervals[i][0];
                curEnd = intervals[i][1];
            }
        }
        merged.add(new int[]{curStart, curEnd});
        return merged.toArray(new int[merged.size()][]);
    }
}
