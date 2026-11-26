class Solution {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> res = new ArrayList<>();
        int ns = newInterval[0];
        int ne = newInterval[1];
        int i = 0, n = intervals.length;
        while (i < n && intervals[i][1] < ns) {
            res.add(intervals[i++]);
        }
        while (i < n && intervals[i][0] <= ne) {
            ns = Math.min(ns, intervals[i][0]);
            ne = Math.max(ne, intervals[i][1]);
            i++;
        }
        res.add(new int[]{ns, ne});
        while (i < n) {
            res.add(intervals[i++]);
        }
        return res.toArray(new int[res.size()][]);
    }
}
