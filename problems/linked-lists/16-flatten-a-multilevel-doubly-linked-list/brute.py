class Solution:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None
        order = []

        def dfs(node):
            while node is not None:
                order.append(node)
                if node.child is not None:
                    dfs(node.child)
                node = node.next

        dfs(head)
        for i, node in enumerate(order):
            node.child = None
            node.prev = order[i - 1] if i > 0 else None
            node.next = order[i + 1] if i + 1 < len(order) else None
        return order[0]
