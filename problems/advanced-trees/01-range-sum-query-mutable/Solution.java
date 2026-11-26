class NumArray {
    private final int[] values;
    private final int[] bit;
    public NumArray(int[] nums) {
        values = nums.clone(); bit = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) add(i + 1, nums[i]);
    }
    private void add(int i, int delta) { for (; i < bit.length; i += i & -i) bit[i] += delta; }
    private int prefix(int i) { int sum = 0; for (; i > 0; i -= i & -i) sum += bit[i]; return sum; }
    public void update(int index, int value) { int delta = value - values[index]; values[index] = value; add(index + 1, delta); }
    public int sumRange(int left, int right) { return prefix(right + 1) - prefix(left); }
}
