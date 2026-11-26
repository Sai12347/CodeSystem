class SnakeGame {
    private final int w;
    private final int h;
    private final int[][] food;
    private int fi = 0;
    private final Deque<Long> body = new ArrayDeque<>();
    private final Set<Long> occupied = new HashSet<>();
    private boolean over = false;

    public SnakeGame(int width, int height, int[][] food) {
        this.w = width;
        this.h = height;
        this.food = food;
        body.addFirst(0L);
        occupied.add(0L);
    }

    private long encode(int r, int c) {
        return (long) r * w + c;
    }

    public int move(String direction) {
        if (over) {
            return -1;
        }
        long headKey = body.peekFirst();
        int r = (int) (headKey / w);
        int c = (int) (headKey % w);
        char ch = direction.charAt(0);
        if (ch == 'U') r--;
        else if (ch == 'D') r++;
        else if (ch == 'L') c--;
        else c++;
        if (r < 0 || r >= h || c < 0 || c >= w) {
            over = true;
            return -1;
        }
        boolean eating = fi < food.length && food[fi][0] == r && food[fi][1] == c;
        if (!eating) {
            long tailKey = body.removeLast();
            occupied.remove(tailKey);
        }
        long newKey = encode(r, c);
        if (occupied.contains(newKey)) {
            over = true;
            return -1;
        }
        body.addFirst(newKey);
        occupied.add(newKey);
        if (eating) {
            fi++;
        }
        return body.size() - 1;
    }
}
