class Solution:
    def isAlmostPalindrome(self, head: Optional[ListNode]) -> bool:
        if head is None or head.next is None:
            return True
        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next
        is_odd = fast.next is None

        second = slow.next
        slow.next = None
        rev = None
        while second is not None:
            nxt = second.next
            second.next = rev
            rev = second
            second = nxt

        p1 = head
        p2 = rev
        while p2 is not None and p1.val == p2.val:
            p1 = p1.next
            p2 = p2.next
        if p2 is None:
            return True

        # Option 1: delete p1 from left half
        a, b = p1.next, p2
        ok1 = True
        while a is not None:
            if a.val != b.val:
                ok1 = False
                break
            a = a.next
            b = b.next
        if ok1:
            return True

        # Option 2: delete p2 from right half
        a, b = p1, p2.next
        while b is not None:
            if a.val != b.val:
                return False
            a = a.next
            b = b.next
        if is_odd:
            return a.val == a.next.val
        return True
