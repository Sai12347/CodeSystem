class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        seen = set()
        for e in emails:
            local, domain = e.split('@', 1)
            plus = local.find('+')
            if plus != -1:
                local = local[:plus]
            seen.add(local.replace('.', '') + '@' + domain)
        return len(seen)
