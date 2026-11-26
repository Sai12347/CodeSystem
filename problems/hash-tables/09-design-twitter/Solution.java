class Twitter {
    private int clock = 0;
    private final Map<Integer, List<int[]>> tweets = new HashMap<>();
    private final Map<Integer, Set<Integer>> following = new HashMap<>();

    public Twitter() {
    }

    public void postTweet(int userId, int tweetId) {
        tweets.computeIfAbsent(userId, k -> new ArrayList<>()).add(new int[]{++clock, tweetId});
    }

    public List<Integer> getNewsFeed(int userId) {
        Set<Integer> users = new HashSet<>();
        users.add(userId);
        Set<Integer> followed = following.get(userId);
        if (followed != null) {
            users.addAll(followed);
        }
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        for (int u : users) {
            List<int[]> list = tweets.get(u);
            if (list != null && !list.isEmpty()) {
                int idx = list.size() - 1;
                int[] t = list.get(idx);
                pq.offer(new int[]{t[0], t[1], u, idx});
            }
        }
        List<Integer> feed = new ArrayList<>(10);
        while (!pq.isEmpty() && feed.size() < 10) {
            int[] top = pq.poll();
            feed.add(top[1]);
            int u = top[2];
            int idx = top[3] - 1;
            if (idx >= 0) {
                int[] prev = tweets.get(u).get(idx);
                pq.offer(new int[]{prev[0], prev[1], u, idx});
            }
        }
        return feed;
    }

    public void follow(int followerId, int followeeId) {
        if (followerId != followeeId) {
            following.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
        }
    }

    public void unfollow(int followerId, int followeeId) {
        if (followerId != followeeId) {
            Set<Integer> set = following.get(followerId);
            if (set != null) {
                set.remove(followeeId);
            }
        }
    }
}
