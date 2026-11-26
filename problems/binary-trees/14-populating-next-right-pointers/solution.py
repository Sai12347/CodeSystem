class Solution:
    def connect(self, root: "Optional[Node]") -> "Optional[Node]":
        if root is None:
            return None
        leftmost = root
        while leftmost.left is not None:
            head = leftmost
            while head is not None:
                head.left.next = head.right
                if head.next is not None:
                    head.right.next = head.next.left
                head = head.next
            leftmost = leftmost.left
        return root
