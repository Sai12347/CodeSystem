class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        first = second = prev = None
        curr = root
        while curr is not None:
            if curr.left is None:
                if prev is not None and prev.val > curr.val:
                    if first is None:
                        first = prev
                    second = curr
                prev = curr
                curr = curr.right
            else:
                pred = curr.left
                while pred.right is not None and pred.right is not curr:
                    pred = pred.right
                if pred.right is None:
                    pred.right = curr
                    curr = curr.left
                else:
                    pred.right = None
                    if prev is not None and prev.val > curr.val:
                        if first is None:
                            first = prev
                        second = curr
                    prev = curr
                    curr = curr.right
        if first is not None and second is not None:
            first.val, second.val = second.val, first.val
