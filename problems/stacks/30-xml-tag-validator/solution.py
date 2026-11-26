class Solution:
    def isValidXml(self, code: str) -> bool:
        n = len(code)
        stack = []
        i = 0
        while i < n:
            if i > 0 and not stack:
                return False
            if code.startswith("<![CDATA[", i):
                if not stack:
                    return False
                end = code.find("]]>", i + 9)
                if end == -1:
                    return False
                i = end + 3
            elif code.startswith("</", i):
                end = code.find(">", i + 2)
                if end == -1:
                    return False
                tag = code[i + 2:end]
                if not stack or stack[-1] != tag:
                    return False
                stack.pop()
                i = end + 1
            elif code[i] == "<":
                end = code.find(">", i + 1)
                if end == -1:
                    return False
                tag = code[i + 1:end]
                if not (1 <= len(tag) <= 9) or not all('A' <= c <= 'Z' for c in tag):
                    return False
                stack.append(tag)
                i = end + 1
            else:
                if not stack:
                    return False
                i += 1
        return not stack
