import solution


def run(inp):
    n = int(inp["n"])
    bad = int(inp["bad"])

    def isBadVersion(version: int) -> bool:
        return version >= bad

    solution.isBadVersion = isBadVersion
    res = solution.Solution().firstBadVersion(n)
    return None if res is None else int(res)
