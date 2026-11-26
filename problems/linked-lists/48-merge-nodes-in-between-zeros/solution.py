class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        write = head
        read = head.next
        acc = 0
        while read is not None:
            if read.val == 0:
                write.val = acc
                acc = 0
                if read.next is not None:
                    write = write.next
                else:
                    write.next = None
            else:
                acc += read.val
            read = read.next
        return head
