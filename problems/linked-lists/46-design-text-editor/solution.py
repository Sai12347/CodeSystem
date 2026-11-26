class TextEditor:
    class _Node:
        __slots__ = ("ch", "prev", "next")

        def __init__(self, ch: str = ""):
            self.ch = ch
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cursor = self.head

    def _left_preview(self) -> str:
        chars = []
        p = self.cursor
        for _ in range(10):
            if p is self.head:
                break
            chars.append(p.ch)
            p = p.prev
        chars.reverse()
        return "".join(chars)

    def addText(self, text: str) -> None:
        for ch in text:
            node = self._Node(ch)
            nxt = self.cursor.next
            self.cursor.next = node
            node.prev = self.cursor
            node.next = nxt
            nxt.prev = node
            self.cursor = node

    def deleteText(self, k: int) -> int:
        deleted = 0
        while deleted < k and self.cursor is not self.head:
            prev = self.cursor.prev
            nxt = self.cursor.next
            prev.next = nxt
            nxt.prev = prev
            self.cursor = prev
            deleted += 1
        return deleted

    def cursorLeft(self, k: int) -> str:
        while k > 0 and self.cursor is not self.head:
            self.cursor = self.cursor.prev
            k -= 1
        return self._left_preview()

    def cursorRight(self, k: int) -> str:
        while k > 0 and self.cursor.next is not self.tail:
            self.cursor = self.cursor.next
            k -= 1
        return self._left_preview()
