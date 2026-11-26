class _SongNode:
    __slots__ = ("song_id", "prev", "next")

    def __init__(self, song_id: int = 0):
        self.song_id = song_id
        self.prev: "_SongNode | None" = None
        self.next: "_SongNode | None" = None


class PlaylistManager:
    def __init__(self):
        self.head = _SongNode()
        self.tail = _SongNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes: dict[int, _SongNode] = {}
        self.curr: _SongNode | None = None

    def _unlink(self, node: _SongNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_after(self, ref: _SongNode, node: _SongNode) -> None:
        node.prev = ref
        node.next = ref.next
        ref.next.prev = node
        ref.next = node

    def addSong(self, songId: int) -> None:
        if songId in self.nodes:
            return
        node = _SongNode(songId)
        self._insert_after(self.tail.prev, node)
        self.nodes[songId] = node
        if self.curr is None:
            self.curr = node

    def playNext(self) -> None:
        if self.curr is not None and self.curr.next is not self.tail:
            self.curr = self.curr.next

    def playPrev(self) -> None:
        if self.curr is not None and self.curr.prev is not self.head:
            self.curr = self.curr.prev

    def removeSong(self, songId: int) -> None:
        node = self.nodes.pop(songId, None)
        if node is None:
            return
        if self.curr is node:
            if node.next is not self.tail:
                self.curr = node.next
            elif node.prev is not self.head:
                self.curr = node.prev
            else:
                self.curr = None
        self._unlink(node)

    def moveToFront(self, songId: int) -> None:
        node = self.nodes.get(songId)
        if node is None:
            return
        self._unlink(node)
        self._insert_after(self.head, node)

    def getCurrent(self) -> int:
        return self.curr.song_id if self.curr is not None else -1
