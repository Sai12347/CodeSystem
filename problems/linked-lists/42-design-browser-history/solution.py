class BrowserHistory:
    class _Node:
        __slots__ = ("url", "prev", "next")

        def __init__(self, url: str):
            self.url = url
            self.prev = None
            self.next = None

    def __init__(self, homepage: str):
        self.curr = self._Node(homepage)

    def visit(self, url: str) -> None:
        node = self._Node(url)
        node.prev = self.curr
        self.curr.next = node
        self.curr = node

    def back(self, steps: int) -> str:
        while steps > 0 and self.curr.prev is not None:
            self.curr = self.curr.prev
            steps -= 1
        return self.curr.url

    def forward(self, steps: int) -> str:
        while steps > 0 and self.curr.next is not None:
            self.curr = self.curr.next
            steps -= 1
        return self.curr.url
