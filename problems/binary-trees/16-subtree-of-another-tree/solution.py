class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node: Optional[TreeNode], out: List[Optional[int]]) -> None:
            if node is None:
                out.append(None)
                return
            out.append(node.val)
            serialize(node.left, out)
            serialize(node.right, out)

        text: List[Optional[int]] = []
        pattern: List[Optional[int]] = []
        serialize(root, text)
        serialize(subRoot, pattern)

        # KMP search for pattern inside text
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length > 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

        j = 0
        for tok in text:
            while j > 0 and tok != pattern[j]:
                j = lps[j - 1]
            if tok == pattern[j]:
                j += 1
                if j == m:
                    return True
        return False
