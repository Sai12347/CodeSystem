class Solution:
    def simplifyPath(self, path: str) -> str:
        segs = [p for p in path.split("/") if p and p != "."]
        while True:
            changed = False
            for i, p in enumerate(segs):
                if p == "..":
                    if i > 0:
                        del segs[i - 1 : i + 1]
                    else:
                        del segs[0]
                    changed = True
                    break
            if not changed:
                break
        return "/" + "/".join(segs)
