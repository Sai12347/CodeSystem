class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) {
            int[] tmp = nums1;
            nums1 = nums2;
            nums2 = tmp;
        }
        Set<Integer> seen = new HashSet<>(nums1.length * 2);
        for (int x : nums1) {
            seen.add(x);
        }
        List<Integer> res = new ArrayList<>();
        for (int x : nums2) {
            if (seen.remove(x)) {
                res.add(x);
            }
        }
        int[] out = new int[res.size()];
        for (int i = 0; i < res.size(); i++) {
            out[i] = res.get(i);
        }
        return out;
    }
}
