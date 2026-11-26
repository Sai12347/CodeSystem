class Solution:
    def isSubPath(self, head: Optional[ListNode], root: Optional[TreeNode]) -> bool:
        pat = []
        curr = head
        while curr is not None:
            pat.append(curr.val)
            curr = curr.next
        m = len(pat)
        lps = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pat[i] != pat[j]:
                j = lps[j - 1]
            if pat[i] == pat[j]:
                j += 1
                lps[i] = j

        stack = [(root, 0)]
        while stack:
            node, matched = stack.pop()
            if node is None:
                continue
            k = matched
            while k > 0 and node.val != pat[k]:
                k = lps[k - 1]
            if node.val == pat[k]:
                k += 1
                if k == m:
                    return True
            if node.right is not None:
                stack.append((node.right, k))
            if node.left is not None:
                stack.append((node.left, k))
        return False
