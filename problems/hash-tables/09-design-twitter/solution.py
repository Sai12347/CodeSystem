class Twitter:
    def __init__(self):
        self.clock = 0
        self.tweets = defaultdict(list)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.clock += 1
        self.tweets[userId].append((self.clock, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []
        users = set(self.following[userId])
        users.add(userId)
        for u in users:
            tlist = self.tweets.get(u)
            if tlist:
                idx = len(tlist) - 1
                ts, tid = tlist[idx]
                heapq.heappush(heap, (-ts, tid, u, idx))
        feed = []
        while heap and len(feed) < 10:
            _, tid, u, idx = heapq.heappop(heap)
            feed.append(tid)
            if idx > 0:
                prev_ts, prev_tid = self.tweets[u][idx - 1]
                heapq.heappush(heap, (-prev_ts, prev_tid, u, idx - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].discard(followeeId)
