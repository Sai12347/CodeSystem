class Twitter:
    def __init__(self):
        self.all_tweets = []
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.all_tweets.append((userId, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        allowed = self.following[userId] | {userId}
        feed = []
        for u, tid in reversed(self.all_tweets):
            if u in allowed:
                feed.append(tid)
                if len(feed) == 10:
                    break
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].discard(followeeId)
