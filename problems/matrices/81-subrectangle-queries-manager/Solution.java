class SubrectangleQueries {
    private final int[][] rect;
    private final List<int[]> updates;

    public SubrectangleQueries(int[][] rectangle) {
        this.rect = new int[rectangle.length][];
        for (int i = 0; i < rectangle.length; i++) {
            this.rect[i] = rectangle[i].clone();
        }
        this.updates = new ArrayList<>();
    }

    public void updateSubrectangle(int row1, int col1, int row2, int col2, int newValue) {
        updates.add(new int[]{row1, col1, row2, col2, newValue});
    }

    public int getValue(int row, int col) {
        for (int i = updates.size() - 1; i >= 0; i--) {
            int[] u = updates.get(i);
            if (u[0] <= row && row <= u[2] && u[1] <= col && col <= u[3]) {
                return u[4];
            }
        }
        return rect[row][col];
    }
}
