import random


def visible():
    return [
        {"in": {
            "ops": ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"],
            "args": [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
        }},
        {"in": {
            "ops": ["Twitter", "getNewsFeed", "postTweet", "follow", "getNewsFeed"],
            "args": [[], [1], [2, 100], [1, 2], [1]]
        }},
    ]


def hidden():
    rng = random.Random(355)

    # More than 10 tweets by a single user (must cap at 10 most recent)
    ops_cap = ["Twitter"] + ["postTweet"] * 15 + ["getNewsFeed"]
    args_cap = [[]] + [[1, i] for i in range(15)] + [[1]]

    # 15 followees each posting 3 interleaved tweets -> tests k-way merge with k > 10
    ops_many = ["Twitter"]
    args_many = [[]]
    tid = 0
    for u in range(2, 17):
        ops_many.append("follow")
        args_many.append([1, u])
    for round_idx in range(3):
        for u in range(1, 17):
            ops_many.append("postTweet")
            args_many.append([u, tid])
            tid += 1
    ops_many.extend(["getNewsFeed", "unfollow", "unfollow", "getNewsFeed"])
    args_many.extend([[1], [1, 16], [1, 15], [1]])

    # Stress test: 700 randomized ops across 30 users
    ops_stress = ["Twitter"]
    args_stress = [[]]
    next_tid = 1
    for _ in range(700):
        r = rng.random()
        if r < 0.45:
            u = rng.randint(1, 30)
            ops_stress.append("postTweet")
            args_stress.append([u, next_tid])
            next_tid += 1
        elif r < 0.65:
            a = rng.randint(1, 30)
            b = rng.randint(1, 29)
            if b >= a:
                b += 1
            ops_stress.append("follow")
            args_stress.append([a, b])
        elif r < 0.80:
            a = rng.randint(1, 30)
            b = rng.randint(1, 29)
            if b >= a:
                b += 1
            ops_stress.append("unfollow")
            args_stress.append([a, b])
        else:
            u = rng.randint(1, 30)
            ops_stress.append("getNewsFeed")
            args_stress.append([u])

    return [
        # Duplicate follow must NOT duplicate tweets in feed
        {"in": {
            "ops": ["Twitter", "postTweet", "follow", "follow", "follow", "getNewsFeed"],
            "args": [[], [2, 10], [1, 2], [1, 2], [1, 2], [1]]
        }},
        # Unfollow nonexistent relationship is a no-op
        {"in": {
            "ops": ["Twitter", "postTweet", "unfollow", "getNewsFeed", "follow", "unfollow", "unfollow", "getNewsFeed"],
            "args": [[], [1, 7], [1, 2], [1], [1, 2], [1, 2], [1, 2], [1]]
        }},
        # Tweets with tweetId = 0 and max userId = 500
        {"in": {
            "ops": ["Twitter", "postTweet", "postTweet", "follow", "getNewsFeed", "getNewsFeed"],
            "args": [[], [500, 0], [1, 10000], [500, 1], [500], [1]]
        }},
        # Mutual follow + interleaving timestamps + unfollow one direction only
        {"in": {
            "ops": ["Twitter", "follow", "follow", "postTweet", "postTweet", "postTweet", "postTweet",
                    "getNewsFeed", "getNewsFeed", "unfollow", "getNewsFeed", "getNewsFeed"],
            "args": [[], [1, 2], [2, 1], [1, 11], [2, 22], [1, 33], [2, 44], [1], [2], [1, 2], [1], [2]]
        }},
        # Followee has no tweets
        {"in": {
            "ops": ["Twitter", "follow", "follow", "postTweet", "getNewsFeed", "getNewsFeed"],
            "args": [[], [1, 2], [1, 3], [1, 99], [1], [2]]
        }},
        # Re-follow after unfollow brings old tweets back
        {"in": {
            "ops": ["Twitter", "postTweet", "postTweet", "follow", "getNewsFeed", "unfollow", "getNewsFeed", "follow", "getNewsFeed"],
            "args": [[], [2, 1], [1, 2], [1, 2], [1], [1, 2], [1], [1, 2], [1]]
        }},
        # Single user > 10 tweets
        {"in": {"ops": ops_cap, "args": args_cap}},
        # k-way merge with 16 users
        {"in": {"ops": ops_many, "args": args_many}},
        # Randomized stress test
        {"in": {"ops": ops_stress, "args": args_stress}},
    ]
