import solution


def run(inp):
    orig = [int(v) for v in inp["nums"]]
    arr = list(orig)
    solution.Solution().wiggleSort(arr)
    if len(arr) != len(orig) or sorted(arr) != sorted(orig):
        return "Output array is not a permutation of the input array"
    for i in range(len(arr) - 1):
        if i % 2 == 0:
            if not (arr[i] < arr[i + 1]):
                return f"Wiggle condition failed at index {i}: {arr[i]} is not < {arr[i + 1]}"
        else:
            if not (arr[i] > arr[i + 1]):
                return f"Wiggle condition failed at index {i}: {arr[i]} is not > {arr[i + 1]}"
    return True
