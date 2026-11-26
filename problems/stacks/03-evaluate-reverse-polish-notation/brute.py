class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        arr = list(tokens)
        ops = {"+", "-", "*", "/"}
        while len(arr) > 1:
            for i in range(2, len(arr)):
                if arr[i] in ops:
                    a = int(arr[i - 2])
                    b = int(arr[i - 1])
                    op = arr[i]
                    if op == "+":
                        val = a + b
                    elif op == "-":
                        val = a - b
                    elif op == "*":
                        val = a * b
                    else:
                        val = int(a / b)
                    arr[i - 2 : i + 1] = [val]
                    break
        return int(arr[0])
